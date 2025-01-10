tools = [
    {
        "type": "function",
        "function": {
            "name": "get_temperatures",
            "description": "Obtiene las temperaturas que se registraron en un día específico",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {"type": "string", "description": "El día en formato 'YYYY-MM-DD' para el cual obtener las temperaturas"},
                    "avg": {"type": "boolean", "description": "True si se desea obtener la temperatura media, False si se desea obtener todas las temperaturas registradas en el día."}
                },
                "required": ["day", "avg"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "temperature_distribution",
            "description": "Obtiene las temperaturas que se registraron en un día específico para generar un grafico de la distribucion de las temperaturas",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {"type": "string", "description": "El día en formato 'YYYY-MM-DD' para el cual obtener la distribucion de las temperaturas"}
                },
                "required": ["day"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
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
            "name": "subtract_numbers",
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
    }
]


def add(a, b):
    """
    Adds two numbers and returns the result as a string.

    Args:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        str: The sum of a and b as a string.
    """
    return f"{a + b}"


def subtract(a, b):
    """
    Subtracts the second number from the first and returns the result as a string.

    Args:
        a (int or float): The number to subtract from.
        b (int or float): The number to be subtracted.

    Returns:
        str: The result of the subtraction as a string.
    """
    return f"{a - b}"

class ToolManager:
    """
    Manages the available tools that can be invoked by the assistant.
    Each tool corresponds to a specific function that can be called dynamically.
    """

    def __init__(self):
        """
        Initializes the ToolManager by storing the list of tool definitions.
        """
        self.tools = tools

    def call_function(self, name: str, arguments: dict):
        """
        Calls the appropriate function based on the provided function name and arguments.

        Args:
            name (str): The name of the function to call.
            arguments (dict): A dictionary containing the arguments required by the function.

        Returns:
            str: The result of the called function or an error message if the function is not found.
        """
        if name == "add_numbers":
            result = add(arguments["num1"], arguments["num2"])
        elif name == "subtract":
            result = subtract(arguments["num1"], arguments["num2"])
        else:
            result = "The requested function was not found."
        return result

    def get_tools(self):
        """
        Returns the list of defined tools.

        Returns:
            list: A list containing the definitions of available tools.
        """
        return self.tools
