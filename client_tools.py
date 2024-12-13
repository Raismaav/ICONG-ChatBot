
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
            "description": "Manda a llamar una funcion del cliente que retorna la ip del cliente",
            "parameters": None
        }
    },
{
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Determine weather in my location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state e.g. San Francisco, CA"
            },
            "unit": {
              "type": "string",
              "enum": [
                "c",
                "f"
              ]
            }
          },
          "additionalProperties": False,
          "required": [
            "location",
            "unit"
          ]
        },
        "strict": True
      }
    },
{
      "type": "function",
      "function": {
        "name": "request_parameters",
        "description": "Preuba de envio de parametros, para despues retornarlos de igual manera",
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