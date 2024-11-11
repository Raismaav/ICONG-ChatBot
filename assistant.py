from tool_manager import ToolManager
from context_manager import ContextManager
from dotenv import load_dotenv
from openai import OpenAI
import json
import os

class Assistant:
    """
    This class represents an assistant that interacts with OpenAI's API to generate responses.
    It also has the ability to call tools (functions) if necessary.

    Attributes:
        client: Instance of the OpenAI client.
        system_message: System message to initialize the conversation with a specific context.
        model: Default model used for API completions.
        temperature: Parameter controlling randomness in the model's responses.
        max_tokens: Maximum number of tokens that OpenAI can return in a response.
        tools: Tools (functions) that the assistant can use if enabled.
    """

    def __init__(self, system_message: str, default_model: str, temperature: float = 1, max_tokens: int = 1024,
                 have_tools: bool = False, have_context: bool = True):
        """
        Initializes the assistant instance with the given parameters.

        Args:
            system_message (str): Initial system message.
            default_model (str): Name of the OpenAI model to be used.
            temperature (float): Controls randomness in text generation.
            max_tokens (int): Token limit for the responses.
            have_tools (bool): Indicates if the assistant has tools available to use.
        """
        load_dotenv()  # Load environment variables, such as the OpenAI API key.

        self.tool_manager = ToolManager()  # Initialize the tool manager.
        self.context_manager = ContextManager()  # Initialize the context manager.
        self.client = OpenAI(api_key=os.getenv('openai_key'))  # Sets up the OpenAI client with the API key.
        self.system_message = [{"role": "system", "content": system_message}]  # Initial system context message.
        self.model = default_model  # Default OpenAI model to be used.
        self.temperature = temperature  # Controls randomness.
        self.max_tokens = max_tokens  # Maximum token limit for the responses.
        self.tools = self.context_manager.get_context_functions()  if have_context else None
        self.tools = self.tools + self.tool_manager.get_tools() if have_tools else self.tools # Initializes tools if they are enabled.

    def __call_function(self, tool_calls, messages):
        """
        Executes the requested tools (functions) in the context of the conversation.

        Args:
            tool_calls (list): List of requested tool calls to execute.
            messages (list): List of previous messages in the conversation.

        Returns:
            Generated response after executing the tools.
        """
        calls = []  # List to store the responses from the tools.
        tools_called = []  # List to track which tools have been called.

        print("\033[95mAssistant:__call_function():\033[0m \033[92mSeleccionando herramienta\033[0m")
        # Iterate over each tool call and execute the corresponding function.
        for tool_call in tool_calls:
            name = tool_call.function.name  # Name of the function to be executed.
            arguments = json.loads(tool_call.function.arguments)  # Function arguments in JSON format.
            print(f"\033[95mAssistant:__call_function():\033[0m Llamando a la funcion {name}, con el parametro {arguments}")
            if name == "get_context_from_conac_files":
                result = self.context_manager.get_context_from_conac_files(arguments['file_name'])  # Call the function and get the result.
            elif name == "get_context_from_form_files":
                result = self.context_manager.get_context_from_form_files(arguments['file_name'])  # Call the function and get the result.
            elif name == "get_context_from_presupuesto_files":
                result = self.context_manager.get_context_from_presupuesto_files(arguments['file_name'])  # Call the function and get the result.
            else:
                result = self.tool_manager.call_function(name, arguments)  # Call the function and get the result.

            # Store the record of the tool call.
            tools_called.append({
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": f"{arguments}"
                }
            })

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
            print("\033[95mAssistant:__call_function():\033[0m \033[93mLlamando nueva funcion\033[0m")
            return self.__call_function(response.tool_calls, messages + messege_call)

    def __response_to(self, messages: list | str, model: str = None):
        """
        Generates a response based on the provided messages and model.

        Args:
            messages (list | str): List of messages in the conversation or a single message as a string.
            model (str, optional): Model to use for generating the response. Defaults to the assistant's model.

        Returns:
            dict: The response generated by OpenAI, with possible tool calls.
        """
        model = model or self.model  # Use the provided model or the default model.

        print("\033[95mAssistant:__response_to():\033[0m \033[94mPreprocesado del asistente\033[0m")
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        print("\033[95mAssistant:__response_to():\033[0m \033[94mPeticion de respuesta al asistente\033[0m")
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
                return {"role": "assistant", "content": "Lo siento, no puedo responder a eso."}
            return call_response
        else:
            print("\033[95mAssistant:__response_to():\033[0m \033[94mRetornando respuesta\033[0m")
            return response

    def response_to(self, messages: list, model: str = None):
        """
        Public method to generate a response to the given messages.

        Args:
            messages (list): List of messages that the assistant should respond to.
            model (str, optional): Model to use for generating the response. Defaults to the assistant's model.

        Returns:
            A dictionary with the role of the sender (assistant) and the content of the response.
        """
        response = self.__response_to(messages, model)  # Generate the response.
        return {"role": response.role, "content": response.content}  # Return the formatted response.
