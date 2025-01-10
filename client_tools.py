tools = [
    {
        "type": "function",
        "function": {
            "name": "client_user",
            "description": "Manda a llamar una función del cliente del servicio que retorna el nombre del cliente y el ID si el parámetro está en true",
            "parameters": {
                "type": "object",
                "properties": {
                    "get_id": {
                        "type": "boolean",
                        "description": "Trae el nombre y el ID del cliente si está en true"
                    }
                },
                "required": ["get_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "getIP",
            "description": "Manda a llamar una función del cliente que retorna la IP del cliente",
            "parameters": None
        }
    },
    {
        "type": "function",
        "function": {
            "name": "requestParameters",
            "description": "Prueba de envío de parámetros, para después retornarlos de igual manera",
            "parameters": {
                "type": "object",
                "required": [
                    "string_param",
                    "float_param",
                    "int_param",
                    "boolean_param"
                ],
                "properties": {
                    "string_param": {
                        "type": "string",
                        "description": "Un parámetro de tipo string"
                    },
                    "float_param": {
                        "type": "number",
                        "description": "Un parámetro de tipo float"
                    },
                    "int_param": {
                        "type": "integer",
                        "description": "Un parámetro de tipo int"
                    },
                    "boolean_param": {
                        "type": "boolean",
                        "description": "Un parámetro de tipo booleano"
                    }
                },
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

tool_names = [tool['function']['name'] for tool in tools]
