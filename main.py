import os
from openai import OpenAI
import json
api_key = "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"
client = OpenAI(api_key=api_key)



if os.path.exists('messages.json'):
    try:
        with open('messages.json', 'r') as f:
            messages = json.load(f)
    except json.JSONDecodeError:
        messages = []
else:
    messages = []

if len(messages) == 0:
    messages = [{"role": "system",
                 "content": "Eres un asistente super alegre y jovial, que le encanta utilizar emojis para ayudar a las personas."}]
    message = input("Escribe un mensaje: ")
    messages.append({"role": "user", "content": message})
else:
    message = input("Escribe un mensaje: ")
    messages.append({"role": "user", "content": message})



completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(completion.choices[0].message.content)
messages.append({"role": completion.choices[0].message.role, "content": completion.choices[0].message.content})

print(messages)
# guardar messages en un archivo json
with open('messages.json', 'w') as f:
    json.dump(messages, f)
