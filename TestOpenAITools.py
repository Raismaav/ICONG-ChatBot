import mysql.connector
import os
from datetime import datetime

from numpy import number
from openai import OpenAI
import json

from torch.ao.nn.quantized import PReLU

import queryFunctions as query

def obtener_temperaturas(fecha, avg: bool = True):
    conn = mysql.connector.connect(
        host='localhost',
        port=33,
        user='root',
        password='',
        database='iot'
    )
    cursor = conn.cursor()
    query = "SELECT temperature FROM information WHERE date = %s"
    cursor.execute(query, (fecha,))
    temperaturas = [fila[0] for fila in cursor.fetchall()]
    conn.close()

    if avg:
        if temperaturas:
            media = sum(temperaturas) / len(temperaturas)
        else:
            return None  # or handle the case when there are no temperatures
        return "{:.2f}".format(media)
    return number(temperaturas)

api_key = "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"
client = OpenAI(api_key=api_key)

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
                "required": ["dia"]
            }
        }
    }
]

system_message = [{"role": "system",
                   "content": f"Eres un asistente super alegre y jovial, que le encanta utilizar emojis para ayudar a las personas. Siempre respondes en el idioma en el que te hablan. Hoy es {datetime.now().strftime('%Y-%m-%d')}"}]

messages = []
message = input("Escribe un mensaje: ")
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
tool_call = response_message.tool_calls[0]
if tool_call:
    name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    if name == "temperaturas":
        result = obtener_temperaturas(arguments["dia"], arguments["avg"])
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
        print(response_message.content)
        print(completion)
        print(messege_call)

