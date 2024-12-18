from message_manager import MessageManager
from assistant import Assistant
from datetime import datetime

class Chat:
    """
    Manages a conversation with an AI assistant, using MessageManager to store and manage the conversation,
    and Assistant to generate responses based on a system message.

    Attributes:
        conversation (MessageManager): Handles storing and managing conversation messages.
        assistant (Assistant): Generates AI-based responses.
        __is_renamed (bool): Indicates whether the conversation title has been automatically renamed.
    """
    def __init__(self, user: str = None, have_tools=False, conversation_file: str = None,
                 path: str = 'conversations/', timestamp: str | datetime = None):
        """
        Initializes the Chat instance with user-specific parameters, MessageManager, and Assistant.

        Args:
            user (str, optional): The user associated with the conversation (default is None).
            have_tools (bool, optional): Specifies if the assistant has tools available (default is False).
            conversation_file (str, optional): Path to an existing conversation file (default is None).
            path (str, optional): Directory for storing conversation files (default is 'conversations/').
            timestamp (str | datetime, optional): Timestamp of the conversation or message (default is None).

        Behavior:
            - Initializes a MessageManager instance to manage conversation storage.
            - Creates an Assistant instance for generating AI responses.
            - Customizes the storage path if a user is specified.
        """
        # Initialize MessageManager and Assistant
        self.conversation = MessageManager(
            user=user,
            conversation_file=conversation_file,
            path=path,
            timestamp=timestamp
        )
        self.assistant = Assistant(
            system_message=self.conversation.get_system_message(),
            default_model="gpt-4o-mini",
            have_tools=have_tools
        )
        self.__is_renamed = False

    def response_to(self, message: str, timestamp: str | datetime = None) -> dict:
        """
        Processes a user message and generates a response using the assistant.

        Args:
            message (str): The user's message.
            timestamp (str | datetime, optional): Timestamp of the message (default is None).

        Behavior:
            - Adds the user's message to the conversation using MessageManager.
            - Generates a response from the assistant and adds it to the conversation.
            - Automatically generates and sets a new conversation title after two messages.

        Returns:
            dict: The assistant's response, including the role and content.
        """
        print("\033[95mChat:response_to():\033[0m \033[91mMensaje indexado\033[0m")
        # Add the user's message to the conversation
        self.conversation.add_message({"role": "user", "content": message}, timestamp)
        # Generate the assistant's response and add it to the conversation
        print("\033[95mChat:response_to():\033[0m \033[91mMensaje enviado al asistente\033[0m")

        response = self.assistant.response_to(self.conversation.get_filtered_messages())

        if not 'role' in response:
            return response

        self.conversation.add_message(response)
        print(f"\033[95mChat:response_to():\033[0m {self.conversation.get_header()}")

        # Automatically rename the conversation title after the second message
        if not self.__is_renamed and self.conversation.get_title() == 'New conversation' and self.conversation.get_message_count() >= 2:
            self.generate_and_set_title()
            print(f"\033[95mChat:response_to():\033[0m {self.conversation.get_header()}")

        return self.conversation.get_last_message()

    def continue_response(self, calls: list, tools_called: list) -> dict:
        """
        Continues processing a conversation with tool calls that need to be executed.

        Args:
            calls (list): Previously executed tool calls.
            tools_called (list): List of tools requested but not yet executed.

        Behavior:
            - Executes the remaining tool calls using the assistant.
            - Adds the assistant's response to the conversation.
            - Automatically generates and sets a new title if applicable.

        Returns:
            dict: The assistant's response, including the role and content.
        """
        response = self.assistant.continue_call(self.conversation.get_filtered_messages(), calls, tools_called)

        if 'role' not in response:
            return response

        self.conversation.add_message(response)
        print(f"\033[95mChat:continue_response:\033[0m {self.conversation.get_header()}")

        # Automatically rename the conversation title after the second message
        if not self.__is_renamed and self.conversation.get_title() == 'New conversation' and self.conversation.get_message_count() >= 2:
            self.generate_and_set_title()
            print(f"\033[95mChat:continue_response:\033[0m {self.conversation.get_header()}")

        return self.conversation.get_last_message()

    def generate_and_set_title(self):
        """
        Generates and sets a new title for the conversation.

        Behavior:
            - Uses an Assistant instance to generate a short title (maximum 15 characters).
            - Ensures the title is plain text, without unsupported characters or formatting.
            - Updates the title in MessageManager and marks the title as renamed.
        """
        print(f"\033[95mChat:generate_and_set_title():\033[0m \033[91mProceso de seteo de titulo\033[0m")
        title_generator = Assistant(
            system_message=(
                """Tú generas un título pequeño de la conversación anterior de no más de 
                15 letras automáticamente en cada consulta, incluso si el usuario no te dice 
                nada, no les preguntas, solo lo generas en el idioma de la conversación.
                
                Debes tambien de entragar el titulo en texto plano sin ningun tipo de adorno o formato.
                Tampoco uses formato markdown o html, solo texto plano.
                Omite cualquier tipo de salto de linea.
                No uses caractereres que no sean soportados por los sistemas de archivos.
                """
            ),
            temperature=1,
            max_tokens=15,
            default_model="gpt-4o-mini",
            have_context=False
        )
        # Generate a new title and rename the conversation
        new_title = title_generator.response_to(self.conversation.get_messages())['content']
        print(f"\033[95mChat:generate_and_set_title():\033[0m \033[91m--{new_title}--\033[0m")
        self.conversation.set_title(new_title)
        self.__is_renamed = True