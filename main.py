from dotenv import load_dotenv
from function_calling import call_function, tools
import os
from datetime import datetime

from openai import OpenAI
import json

load_dotenv()
client = OpenAI(api_key=os.getenv('openai_key'))

system_message = [{"role": "system",
                   "content": f"Eres un asistente super alegre y jovial, que le encanta utilizar emojis para ayudar a las personas. Siempre respondes en el idioma en el que te hablan y no camias de idioma hasta que cambia el usuario. Si el usuario quiere salir del chat le debes decir que escriba la palabra exit, ya que eres una sistente en la linea de comandos. Hoy es {datetime.now().strftime('%Y-%m-%d')}"}]

while True:
    if os.path.exists('messages/messages.json'):
        try:
            with open('messages/messages.json', 'r') as f:
                messages = json.load(f)
        except json.JSONDecodeError:
            messages = []
    else:
        messages = []

    message = input("Escribe un mensaje: ")
    if message == "exit":
        print("Hasta luego! 👋")
        break
    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=system_message + messages,
        tools=tools,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response_message = completion.choices[0].message
    if response_message.tool_calls:
        messages.append(call_function(response_message.tool_calls, system_message, messages))
    else:
        messages.append({"role": response_message.role, "content": response_message.content})

    print(messages[-1]['content'])

    with open('messages/messages.json', 'w') as f:
        json.dump(messages, f)
