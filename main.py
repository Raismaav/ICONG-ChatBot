from dotenv import load_dotenv

import os
from datetime import datetime

from openai import OpenAI
import json
import queryFunctions as query

import matplotlib.pyplot as plt

debug = False

load_dotenv()
client = OpenAI(api_key=os.getenv('openai_key'))

def suma(a, b):
    return f"{a + b}"

def resta(a, b):
    return f"{a - b}"

def temperaturas(dia, avg = True):
    return f"{query.obtener_temperaturas(dia, avg)}"


def distribucion_temperaturas(dia):
    resultados = query.distribucion_temperaturas(dia)

    # Extract temperatures and hours
    temperaturas = [registro[0] for registro in resultados]
    horas = [registro[1] for registro in resultados]

    if len(temperaturas) == 0:
        return "No hay datos para mostrar"

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(horas, temperaturas, marker='o')
    plt.title(f'Distribución de Temperaturas para {dia}')
    plt.xlabel('Hora')
    plt.ylabel('Temperatura')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(f'images/distribucion_temperaturas_{dia}.png')
    plt.show()

    return "Imagen creada con la distribución de las temperaturas"

tools = [
    {
        "type": "function",
        "function": {
            "name": "temperaturas",
            "description": "Obtiene las temperaturas que se registraron en un día específico",
            "parameters": {
                "type": "object",
                "properties": {
                    "dia": {"type": "string", "description": "El día en formato 'YYYY-MM-DD' para el cual obtener las temperaturas"},
                    "avg": {"type": "boolean", "description": "True si se desea obtener la temperatura media, False si se desea obtener todas las temperaturas registradas en el día."}
                },
                "required": ["dia", "avg"]
            }
        }
    },
{
        "type": "function",
        "function": {
            "name": "distribucion_temperaturas",
            "description": "Obtiene las temperaturas que se registraron en un día específico para generar un grafico de la distribucion de las temperaturas",
            "parameters": {
                "type": "object",
                "properties": {
                    "dia": {"type": "string", "description": "El día en formato 'YYYY-MM-DD' para el cual obtener la distribucion de las temperaturas"}
                },
                "required": ["dia"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suma",
            "description": "Suma dos números que entrega el usuario cuando lo pide explicitamente, el usuario debe mencionar que quiere sumar los números, si no menciona nada acerca de sumar no debe realizar la accion.",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "El primer número de la suma"},
                    "num2": {"type": "number", "description": "El segundo número de la suma"}
                },
                "required": ["num1", "num2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "resta",
            "description": "Resta dos números que entrega el usuario cuando lo pide explicitamente, el usuario debe mencionar que quiere restar los números, si no menciona nada acerca de restar no debe realizar la accion.",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "El primer número de la resta"},
                    "num2": {"type": "number", "description": "El segundo número de la resta"}
                },
                "required": ["num1", "num2"]
            }
        }
    },
]

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
        # max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response_message = completion.choices[0].message
    if response_message.tool_calls:
        if debug: print("😛")
        tool_call = response_message.tool_calls[0]
        name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        result = ""
        if name == "suma":
            result = suma(arguments["num1"], arguments["num2"])
        elif name == "resta":
            result = resta(arguments["num1"], arguments["num2"])
        elif name == "temperaturas":
            result = temperaturas(arguments["dia"], arguments["avg"])
        elif name == "distribucion_temperaturas":
            if debug: print(f"🤪\n{arguments['dia']}")
            result = distribucion_temperaturas(arguments["dia"])

        messege_call = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": name,
                            "arguments": f"{arguments}"
                        }
                    }
                ]
            },
            {
                "role": "tool",
                "content": [{
                    "type": "text",
                    "text": result
                }],
                "tool_call_id": tool_call.id,
            }
        ]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=system_message + messages + messege_call,
            tools=tools,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_message = completion.choices[0].message

        messages.append({"role": response_message.role, "content": response_message.content})
    else:
        messages.append({"role": response_message.role, "content": response_message.content})

    print(response_message.content)
    # print(completion)

    with open('messages/messages.json', 'w') as f:
        json.dump(messages, f)
