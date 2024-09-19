import query_functions as qf
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('openai_key'))

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

def suma(a, b):
    return f"{a + b}"

def resta(a, b):
    return f"{a - b}"

def distribucion_temperaturas(dia):
    resultados = qf.distribucion_temperaturas(dia)

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

def call_function(tool_calls, system_message, messages):
    tool_call = tool_calls[0]
    name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    result = ""
    if name == "suma":
        result = suma(arguments["num1"], arguments["num2"])
    elif name == "resta":
        result = resta(arguments["num1"], arguments["num2"])
    elif name == "temperaturas":
        result = qf.obtener_temperaturas(arguments["dia"], arguments["avg"])
    elif name == "distribucion_temperaturas":
        result = distribucion_temperaturas(arguments["dia"])

    messege_call = [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": f"{arguments}"
                }
            }
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
    if response_message.content:
        return {"role": response_message.role, "content": response_message.content}
    else:
        return ""