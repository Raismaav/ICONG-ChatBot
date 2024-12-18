from tool_manager import ToolManager
from context_manager import ContextManager
from dotenv import load_dotenv
from openai import OpenAI
import client_tools
import json
import os

class Assistant:
    """
    Represents an AI assistant that interacts with OpenAI's API to generate responses and execute tools if needed.

    Attributes:
        client: Instance of the OpenAI client used for generating responses.
        system_message: Initial system message providing context for the conversation.
        model: Default OpenAI model used for generating responses.
        temperature: Controls randomness in the model's responses.
        max_tokens: Maximum number of tokens the model can return in a response.
        tools: A collection of tools or functions the assistant can use during the conversation.
    """
    def __init__(self, system_message: str, default_model: str, temperature: float = 1, max_tokens: int = 1024,
                 have_tools: bool = False, have_context: bool = True):
        """
        Initializes the assistant instance with the given parameters.

        Args:
            system_message (str): Initial system message providing the assistant's context and behavior.
            default_model (str): OpenAI model to use for generating responses.
            temperature (float, optional): Controls randomness in the model's output (default is 1).
            max_tokens (int, optional): Maximum token limit for the model's responses (default is 1024).
            have_tools (bool, optional): Indicates whether the assistant has access to tools (default is False).
            have_context (bool, optional): Indicates whether the assistant uses contextual tools (default is True).
        """
        load_dotenv()  # Load environment variables, such as the OpenAI API key.

        self.tool_manager = ToolManager()  # Initialize the tool manager.
        self.context_manager = ContextManager()  # Initialize the context manager.
        self.client = OpenAI(api_key=os.getenv('openai_key'))  # Sets up the OpenAI client with the API key.
        self.system_message = [{"role": "system", "content": system_message}]  # Initial system context message.
        self.model = default_model  # Default OpenAI model to be used.
        self.temperature = temperature  # Controls randomness.
        self.max_tokens = max_tokens  # Maximum token limit for the responses.
        self.tools = self.context_manager.get_context_functions() if have_context else None
        if have_tools:
            self.tools += (self.tool_manager.get_tools() or []) + (client_tools.tools or [])

    def __call_function(self, tool_calls, messages):
        """
        Executes tools requested during the conversation.

        Args:
            tool_calls (list): List of tool call requests, each containing a tool's name and arguments.
            messages (list): List of previous messages in the conversation.

        Returns:
            dict or list: The generated response from the assistant or a list of tool call details if applicable.

        Raises:
            Exception: If an error occurs while executing tools or generating responses.
        """
        calls = []  # List to store the responses from the tools.
        tools_called = []  # List to track which tools have been called.
        client_call = False

        print("\033[95mAssistant:__call_function():\033[0m \033[92mSeleccionando herramienta\033[0m")
        # Iterate over each tool call and execute the corresponding function.
        for tool_call in tool_calls:
            name = tool_call.function.name  # Name of the function to be executed.
            arguments = json.loads(tool_call.function.arguments)  # Function arguments in JSON format.

            # Store the record of the tool call.
            tools_called.append({
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": f"{arguments}"
                }
            })

            if name in client_tools.tool_names:
                client_call = True

        if client_call:
            return tools_called

        for tool_call in tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\033[95mAssistant:__call_function():\033[0m Llamando a la función {name}, con el parámetro {arguments}")
            if name == "get_context_from_conac_files":
                result = self.context_manager.get_context_from_conac_files(arguments['file_name'])  # Call the function and get the result.
            elif name == "get_context_from_form_files":
                result = self.context_manager.get_context_from_form_files(arguments['file_name'])  # Call the function and get the result.
            elif name == "get_context_from_presupuesto_files":
                result = self.context_manager.get_context_from_presupuesto_files(arguments['file_name'])  # Call the function and get the result.
            else:
                result = self.tool_manager.call_function(name, arguments)  # Call the function and get the result.

            # Store the result in the calls list.
            calls.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id,
            })
        print("\033[95mAssistant:__call_function():\033[0m \033[92mHerramienta seleccionada\033[0m")
        # Prepare the tool call messages for the response.
        messege_call = [{
            "role": "assistant",
            "content": "",
            "tool_calls": tools_called
        }] + calls

        print("\033[95mAssistant:__call_function():\033[0m \033[92mSolicitando nueva respuesta\033[0m")
        # Generate a response using the tool calls and previous messages.
        response = self.__response_to(messages + messege_call)

        # If the response contains content, return it; otherwise, call the tools again.
        if response.content:
            print("\033[95mAssistant:__call_function():\033[0m \033[92mRetornando nueva respuesta\033[0m")
            return response
        else:
            print("\033[95mAssistant:__call_function():\033[0m \033[93mLlamando nueva función\033[0m")
            return self.__call_function(response.tool_calls, messages + messege_call)

    def __response_to(self, messages: list | str, model: str = None):
        """
        Generates a response based on the provided messages and model.

        Args:
            messages (list | str): Messages from the conversation or a single string message.
            model (str, optional): Specific OpenAI model to use. Defaults to the assistant's model.

        Returns:
            dict: Generated response from OpenAI, including possible tool calls or assistant replies.

        Raises:
            Exception: If an error occurs while generating the response.
        """
        model = model or self.model  # Use the provided model or the default model.

        print("\033[95mAssistant:__response_to():\033[0m \033[94mPreprocesado del asistente\033[0m")
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        print("\033[95mAssistant:__response_to():\033[0m \033[94mPetición de respuesta al asistente\033[0m")
        # Create the chat completion request to OpenAI's API.

        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=self.system_message + messages,
                tools=self.tools,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        except Exception as e:
            print("\033[95mAssistant:__response_to():\033[0m \033[91mError al solicitar respuesta\033[0m")
            print("\033[91m{}\033[0m".format(e))
            return {"role": "assistant", "content": "Lo siento, no puedo responder a eso."}

        print("\033[95mAssistant:__response_to():\033[0m \033[94mRecuperando respuesta\033[0m")
        response = completion.choices[0].message  # Get the first message from the response.

        # If the response includes tool calls, execute them.
        if response.tool_calls:
            print("\033[95mAssistant:__response_to():\033[0m \033[92mSolicitando herramientas\033[0m")
            try:
                call_response = self.__call_function(response.tool_calls, messages)
                print(call_response)
            except Exception as e:
                print("\033[95mAssistant:__response_to():\033[0m \033[91mError al solicitar herramientas\033[0m")
                print("\033[91m{}\033[0m".format(e))
                return {"role": "assistant", "content": "Lo siento, ocurrio un error al solicitar herramientas."}
            return call_response
        else:
            print("\033[95mAssistant:__response_to():\033[0m \033[94mRetornando respuesta\033[0m")
            return response

    def response_to(self, messages: list, model: str = None):
        """
        Public method to generate a response for the given messages.

        Args:
            messages (list): List of messages in the conversation.
            model (str, optional): OpenAI model to use. Defaults to the assistant's model.

        Returns:
            dict: Contains the role (e.g., 'assistant') and the content of the response.
        """
        response = self.__response_to(messages, model)  # Generate the response.
        if hasattr(response, 'role'):
            return {"role": response.role, "content": response.content}  # Return the formatted response.
        else:
            return response

    def continue_call(self, messages: list, calls: list, tools_called: list):
        """
        Continues processing a previous conversation by handling tool calls that were not yet executed.

        Args:
            messages (list): List of previous messages in the conversation.
            calls (list): List of tool call results already processed.
            tools_called (list): List of tools requested by the assistant but not yet executed.

        Returns:
            dict: Contains the role ('assistant') and content of the assistant's response, or the result of executed tools.

        Raises:
            Exception: If an error occurs while continuing the conversation or executing tools.
        """
        print(f"calls: {calls}")
        print(f"tools_called: {tools_called}")
        try:
            # Crear un conjunto de IDs de llamadas de herramientas ya ejecutadas.
            executed_ids = set(call['tool_call_id'] for call in calls)
            # Iterar sobre las herramientas solicitadas que aún no se han ejecutado.
            for tool_call in tools_called:
                if tool_call['id'] not in executed_ids:
                    name = tool_call['function']['name']
                    arguments = json.loads(tool_call['function']['arguments'])  # Convertir de cadena JSON a dict

                    print(f"Assistant:continue_call(): Llamando a la función {name} con argumentos {arguments}")

                    # Ejecutar la función correspondiente.
                    if name == "get_context_from_conac_files":
                        result = self.context_manager.get_context_from_conac_files(arguments['file_name'])
                    elif name == "get_context_from_form_files":
                        result = self.context_manager.get_context_from_form_files(arguments['file_name'])
                    elif name == "get_context_from_presupuesto_files":
                        result = self.context_manager.get_context_from_presupuesto_files(arguments['file_name'])
                    else:
                        result = self.tool_manager.call_function(name, arguments)

                    # Registrar el resultado en la lista de llamadas.
                    calls.append({
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tool_call['id'],
                    })

            # Construir la nueva llamada con los mensajes y las llamadas realizadas.
            messege_call = [{
                "role": "assistant",
                "content": "",
                "tool_calls": tools_called
            }] + calls
            # Generar la respuesta del asistente.
            response = self.__response_to(messages + messege_call)
            if hasattr(response, 'role'):
                print("\033[95mAssistant:continue_call():\033[0m \033[92mRetornando nueva respuesta\033[0m")
                return {"role": response.role, "content": response.content}
            else:
                print("\033[95mAssistant:continue_call():\033[0m \033[93mLlamando nueva función\033[0m")
                return self.__call_function(response['tool_calls'], messages + messege_call)
        except Exception as e:
            print("\033[95mAssistant:continue_call():\033[0m \033[91mError al continuar la solicitud\033[0m")
            print("\033[91m{}\033[0m".format(e))
            return {"role": "assistant", "content": "Lo siento, no puedo responder a eso."}