import os
from openai import OpenAI
import json
import queryFunctions as query


api_key = "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"
client = OpenAI(api_key=api_key)

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def temperaturaMedia(dia):
    print(dia)
    return query.obtener_temperaturas(dia)

def temperaturas(dia, avg):
    print(dia)
    return query.obtener_temperaturas(dia, avg)

functions = [
    {
        "name": "suma",
        "description": "Suma dos números",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "El primer número"},
                "b": {"type": "number", "description": "El segundo número"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "resta",
        "description": "Resta dos números",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "El primer número"},
                "b": {"type": "number", "description": "El segundo número"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "temperaturas",
        "description": "Obtiene las temperaturas que se registraron en un día específico",
        "parameters": {
            "type": "object",
            "properties": {
                "dia": {"type": "string", "description": "El día en formato 'YYYY-MM-DD' para el cual obtener las temperaturas"},
                "avg": {"type": "boolean", "description": "True si se desea obtener la temperatura media, False si se desea obtener todas las temperaturas registradas en el día."}
            },
            "required": ["dia"]
        }
    }
]
while True:

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
                     "content": "Eres un asistente super alegre y jovial, que le encanta utilizar emojis para ayudar a las personas. Siempre respondes en el idioma en el que te hablan "}]
        message = input("Escribe un mensaje: ")
        messages.append({"role": "user", "content": message})
    else:
        message = input("Escribe un mensaje: ")
        messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=functions,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response_message = completion.choices[0].message

    if response_message.function_call:
        function_name = response_message.function_call.name
        arguments = json.loads(response_message.function_call.arguments)
        if function_name == "suma":
            result = suma(arguments["a"], arguments["b"])
        elif function_name == "resta":
            result = resta(arguments["a"], arguments["b"])
        elif function_name == "temperaturas":
            result = temperaturas(arguments["dia"], arguments["avg"])
        result_message = f"Resultado de la función {function_name}: {result}"
        print(result_message)
        messages.append({"role": "assistant", "content": result_message})
    else:
        messages.append({"role": response_message.role, "content": response_message.content})

    print(response_message.content)
    print(completion)

    with open('messages.json', 'w') as f:
        json.dump(messages, f)
