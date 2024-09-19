import query_functions as qf

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

def call_function(name: str, arguments: dict):
    if name == "suma":
        result = suma(arguments["num1"], arguments["num2"])
    elif name == "resta":
        result = resta(arguments["num1"], arguments["num2"])
    elif name == "temperaturas":
        result = qf.obtener_temperaturas(arguments["dia"], arguments["avg"])
    elif name == "distribucion_temperaturas":
        result = qf.distribucion_temperaturas(arguments["dia"])
    else:
        result = "No se encontro la función solicitada"
    return result