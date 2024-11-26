
tools = [
    {
        "type": "function",
        "function": {
            "name": "client_user",
            "description": "Manda a llamar una funcion del cliente del servicio que retorna el nombre del cliente y el id si el parametro esta en true",
            "parameters": {
                "type": "object",
                "properties": {
                    "get_id": {"type": "boolean", "description": "trae el nombre y el id del cliente si esta en true"}
                },
                "required": ["get_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "client_address",
            "description": "Manda a llamar una funcion del cliente del servicio que retorna la ip del cliente",
            "parameters": None
        }
    }
]

tool_names = [tool['function']['name'] for tool in tools]