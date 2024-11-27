from message_manager import MessageManager
from assistant import Assistant
from datetime import datetime

class Chat:
    """
    Manages a conversation with an AI assistant, using MessageManager to store and manage the conversation,
    and Assistant to generate responses based on a system message related to governmental accounting in Mexico.

    Attributes:
        system_message (str): System message defining the assistant's role and behavior.
        conversation (MessageManager): An instance of MessageManager that handles storing and managing conversation messages.
        assistant (Assistant): An instance of Assistant responsible for generating AI responses.
        __is_renamed (bool): A flag indicating whether the conversation title has been automatically renamed after two messages.
    """

    def __init__(self, user: str = None, have_tools=False, conversation_file: str = None,
                 path: str = 'conversations/', timestamp: str | datetime = None):
        """
        Initializes the Chat instance with user-specific parameters, a system message, MessageManager, and Assistant.

        Args:
            user (str, optional): The user associated with the conversation (default is None).
            have_tools (bool, optional): Indicates whether the assistant has tools available (default is False).
            conversation_file (str , optional): Path to an existing conversation file (default is None).
            path (str, optional): Directory where conversation files are stored (default is 'conversations/').
            timestamp (str | datetime, optional): Timestamp of the message or conversation (default is None).

        Behavior:
            - If a user is specified, the path is customized for that user.50
            - Initializes MessageManager to manage conversation storage and Assistant to handle AI-based responses.
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
            message (str): The user's message that needs a response.
            timestamp (str | datetime, optional): The timestamp of the message (default is None).

        Behavior:
            - Adds the user's message to the conversation using MessageManager.
            - The assistant generates a response, which is also added to the conversation.
            - Automatically renames the conversation title after the second message using an AI-generated title.

        Returns:
            dict: The last message in the conversation (assistant's response).
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
        if not self.__is_renamed and self.conversation.title == 'New conversation' and self.conversation.get_message_count() >= 2:
            self.generate_and_set_title()
            print(f"\033[95mChat:response_to():\033[0m {self.conversation.get_header()}")

        return self.conversation.get_last_message()

    def generate_and_set_title(self):
        """
        Generates a new title for the conversation and sets it.

        Behavior:
            - Uses the Assistant to generate a short title based on the conversation.
            - Updates the conversation title if the conditions are met.
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
            have_tools=True
        )
        # Generate a new title and rename the conversation
        new_title = title_generator.response_to(self.conversation.get_messages())['content']
        print(f"\033[95mChat:generate_and_set_title():\033[0m \033[91m--{new_title}--\033[0m")
        self.conversation.set_title(new_title)
        self.__is_renamed = True
