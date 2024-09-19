from assistant import Assistant
from datetime import datetime
import json
import os

system_message = f"Eres un asistente super alegre y jovial, que le encanta utilizar emojis para ayudar a las personas. Siempre respondes en el idioma en el que te hablan y no camias de idioma hasta que cambia el usuario. Si el usuario quiere salir del chat le debes decir que escriba la palabra exit, ya que eres una sistente en la linea de comandos. Hoy es {datetime.now().strftime('%Y-%m-%d')}"

assistant = Assistant(system_message=system_message, default_model="gpt-4o-mini", have_tools=True)

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
    messages.append(assistant.response_to(messages))

    print(messages[-1]['content'])

    with open('messages/messages.json', 'w') as f:
        json.dump(messages, f)
