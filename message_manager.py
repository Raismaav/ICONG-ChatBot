import json
import hashlib
import datetime
import os

class MessageManager:
    """
    Manages conversations and messages, storing them in JSON files with unique identifiers.
    It supports creating new conversations, adding messages, and resuming previous conversations.

    Attributes:
        path: Directory where the conversation files are stored.
        conversation_id: Unique identifier of the conversation (based on system message and timestamp).
        user: The user associated with the conversation.
        title: Title of the conversation.
        timestamp: Timestamp of when the conversation was created (in ISO 8601 format).
        system_message: Initial system message or context for the conversation.
        messages: List of messages in the conversation, each with role, content, timestamp, and a unique ID.
        filename: The JSON file where the conversation is stored.
    """

    def __init__(self, system_message: str = None, user: str = None, title: str = 'New conversation',
                 conversation_file: str = None, path: str = 'conversations/'):
        """
        Initializes a new conversation or loads an existing one from a JSON file.

        Args:
            system_message (str, optional): Initial message or context for the system. Required if creating a new conversation.
            user (str, optional): The user associated with the conversation (default is None).
            title (str, optional): The title of the conversation (default is 'Conversation').
            conversation_file (str, optional): Path to an existing JSON file to load a conversation (default is None).
            path (str, optional): Directory where conversation files are stored (default is 'conversations/').

        Raises:
            ValueError: If system_message is None when creating a new conversation.
        """
        if not os.path.exists(path):
            os.makedirs(path)  # Create directory if it does not exist

        self.path = path

        if conversation_file and os.path.exists(conversation_file):
            # Load existing conversation
            with open(conversation_file, 'r') as f:
                self.conversation = json.load(f)
            self.conversation_id = self.conversation['conversation']['id']
            self.user = self.conversation['conversation']['user']
            self.title = self.conversation['conversation']['title']
            self.timestamp = self.conversation['conversation']['timestamp']
            self.system_message = self.conversation['conversation']['system_message']
            self.messages = self.conversation['conversation']['messages']
            self.filename = conversation_file
        else:
            # Create a new conversation
            if system_message is None:
                raise ValueError("A 'system_message' is required to start a new conversation.")
            self.system_message = system_message
            self.user = user
            self.title = title
            self.timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
            # Generate a unique ID for the conversation using a hash of the system_message and timestamp
            hash_input = (system_message + self.timestamp).encode('utf-8')
            self.conversation_id = hashlib.sha256(hash_input).hexdigest()[:12]
            self.messages = []

            # Build the conversation object
            self.conversation = {
                "conversation": {
                    "id": self.conversation_id,
                    "user": self.user,
                    "title": self.title,
                    "timestamp": self.timestamp,
                    "system_message": self.system_message,
                    "messages": self.messages
                }
            }

            # Create the JSON file with the title and ID in the filename
            self.filename = os.path.join(self.path, f"{self.conversation_id}_{self.title.lower().replace(' ', '_')}.json")
            with open(self.filename, 'w') as f:
                json.dump(self.conversation, f, indent=2)

    def add_message(self, message_dict: dict, timestamp: str = None):
        """
        Adds a new message to the conversation.

        Args:
            message_dict (dict): Dictionary containing:
                - role (str): The role of the sender (e.g., 'user' or 'assistant').
                - content (str): The content of the message.
                - timestamp (str, optional): The timestamp of the message (default is None).
        """
        role = message_dict.get('role')
        content = message_dict.get('content')
        timestamp = timestamp or datetime.datetime.utcnow().isoformat() + 'Z'
        # Generate a unique ID for the message using a hash of the content and timestamp
        hash_input = (content + timestamp).encode('utf-8')
        message_id = hashlib.sha256(hash_input).hexdigest()[:12]

        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp,
            "id": message_id
        }
        self.messages.append(message)
        self.conversation['conversation']['messages'] = self.messages

        # Update the JSON file
        with open(self.filename, 'w') as f:
            json.dump(self.conversation, f, indent=2)

    def modify_system_message(self, new_system_message: str):
        """
        Modifies the system message (context) of the conversation.

        Args:
            new_system_message (str): The new system message or context.
        """
        self.system_message = new_system_message
        self.conversation['conversation']['system_message'] = new_system_message

        # Update the JSON file
        with open(self.filename, 'w') as f:
            json.dump(self.conversation, f, indent=2)

    def modify_title(self, new_title: str):
        """
        Modifies the title of the conversation.

        Args:
            new_title (str): The new title of the conversation.
        """
        self.title = new_title.replace('.', '')
        self.conversation['conversation']['title'] = new_title

        # Delete the old JSON file
        os.remove(self.filename)

        # Create the JSON file with the new title and ID in the filename
        self.filename = os.path.join(self.path, f"{self.conversation_id}_{self.title.lower().replace(' ', '_')}.json")
        with open(self.filename, 'w') as f:
            json.dump(self.conversation, f, indent=2)

    def get_system_message(self) -> str:
        """
        Retrieves the current system message of the conversation.

        Returns:
            str: The system message or context of the conversation.
        """
        return self.system_message

    def get_messages(self) -> list:
        """
        Returns the full list of messages in the conversation.

        Returns:
            list: A list of messages, each containing role, content, timestamp, and ID.
        """
        return self.messages

    def get_filtered_messages(self) -> list:
        """
        Returns a filtered list of messages containing only the role and content.

        Returns:
            list: A list of dictionaries, each with 'role' and 'content'.
        """
        return [{'role': msg['role'], 'content': msg['content']} for msg in self.messages]

    def get_last_message(self) -> dict:
        """
        Returns the last message added to the conversation.

        Returns:
            dict: The last message in the conversation, containing role, content, timestamp, and ID.
            If there are no messages, returns an empty dictionary.
        """
        if self.messages:
            return self.messages[-1]
        return {}

    def get_message_count(self) -> int:
        """
        Returns the number of messages in the conversation.

        Returns:
            int: The number of messages.
        """
        return len(self.messages)