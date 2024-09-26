from message_manager import MessageManager
from assistant import Assistant
from datetime import datetime


class Chat:
    """
    Manages a conversation with an AI assistant, using MessageManager to store and manage the conversation
    and Assistant to generate responses based on a system message related to governmental accounting in Mexico.

    Attributes:
        system_message: System message defining the assistant's role and behavior.
        conversation: An instance of MessageManager that handles storing and managing conversation messages.
        assistant: An instance of Assistant responsible for generating AI responses.
        __is_renamed: A flag indicating whether the conversation title has been automatically renamed after two messages.
    """

    def __init__(self, user: str = None, have_tools=False, conversation_file: str = None, path: str = 'conversations/'):
        """
        Initializes the Chat instance with user-specific parameters, a system message, MessageManager, and Assistant.

        Args:
            user (str, optional): The user associated with the conversation (default is None).
            have_tools (bool, optional): Indicates whether the assistant has tools available (default is False).
            conversation_file (str, optional): Path to an existing conversation file (default is None).
            path (str, optional): Directory where conversation files are stored (default is 'conversations/').

        Behavior:
            - If a user is specified, the path is customized for that user.
            - The system message defines the assistant as an expert in governmental accounting, focusing on the laws and regulations in Mexico, with an emphasis on Jalisco's local laws.
            - Initializes MessageManager to manage conversation storage and Assistant to handle AI-based responses.
        """
        if user is not None:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        # Define the system message with details about the assistant's role and focus
        system_message = f"""
            ... # (The full system message explaining the assistant's role, omitted here for brevity)
            the date today is {datetime.now().strftime('%Y-%m-%d')}"""

        # Initialize MessageManager and Assistant
        self.conversation = MessageManager(
            system_message=system_message,
            user=user,
            conversation_file=conversation_file,
            path=path
        )
        self.assistant = Assistant(
            system_message=self.conversation.get_system_message(),
            default_model="gpt-4o-mini",
            have_tools=have_tools
        )
        self.__is_renamed = False

    def response_to(self, message: str, timestamp: str = None) -> dict:
        """
        Processes a user message and generates a response using the assistant.

        Args:
            message (str): The user's message that needs a response.
            timestamp (str, optional): The timestamp of the message (default is None).

        Behavior:
            - Adds the user's message to the conversation using MessageManager.
            - The assistant generates a response, which is also added to the conversation.
            - Automatically renames the conversation title after the second message using an AI-generated title.

        Returns:
            dict: The last message in the conversation (assistant's response).
        """
        # Add the user's message to the conversation
        self.conversation.add_message({"role": "user", "content": message}, timestamp)
        # Generate the assistant's response and add it to the conversation
        self.conversation.add_message(self.assistant.response_to(self.conversation.get_filtered_messages()))

        # Automatically rename the conversation title after the second message
        if not self.__is_renamed and self.conversation.title == 'New conversation' and self.conversation.get_message_count() >= 2:
            self.generate_and_set_title()

        return self.conversation.get_last_message()

    def generate_and_set_title(self):
        """
        Generates a new title for the conversation and sets it.
        """
        title_generator = Assistant(
            system_message=(
                "You generate a small title of the previous conversation no longer than "
                "15 letters automatically in each query, even if the user doesn't tell you "
                "anything, you don't ask them, you just generate it in the language of the conversation."
            ),
            temperature=1,
            max_tokens=15,
            default_model="gpt-4o-mini",
            have_tools=True
        )
        # Generate a new title and rename the conversation
        new_title = title_generator.response_to(self.conversation.get_messages())['content']
        self.conversation.set_title(new_title)
        self.__is_renamed = True