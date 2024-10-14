from datetime import datetime, timezone
import hashlib
import json
import os


class MessageManager:
    """
    Manages conversations and messages, storing them in JSON files with unique identifiers.
    It supports creating new conversations, adding messages, updating conversation details, and resuming previous conversations.

    Attributes:
        path: Directory where the conversation files are stored.
        conversation_id: Unique identifier of the conversation (based on system message and timestamp).
        user: The user associated with the conversation.
        title: Title of the conversation.
        timestamp: Timestamp of when the conversation was created (in ISO 8601 format).
        system_message: Initial system message or context for the conversation.
        messages: List of messages in the conversation, each with role, content, timestamp, and a unique ID.
        filename: The JSON file where the conversation is stored.
        full_filepath: Full path of the JSON file storing the conversation.
    """

    def __init__(self, system_message: str = None, user: str = None, title: str = 'New conversation',
                 timestamp: str | datetime = None, conversation_file: str = None, path: str = 'conversations/'):
        """
        Initializes a new conversation or loads an existing one from a JSON file.

        Args:
            system_message (str, optional): Initial message or context for the system. Required if creating a new conversation.
            user (str, optional): The user associated with the conversation (default is None).
            title (str, optional): The title of the conversation (default is 'New conversation').
            timestamp (str | datetime, optional): Timestamp of the conversation (default is current UTC time).
            conversation_file (str, optional): Path to an existing JSON file to load a conversation (default is None).
            path (str, optional): Directory where conversation files are stored (default is 'conversations/').

        Raises:
            ValueError: If system_message is None when creating a new conversation.
            ValueError: If conversation_file is not a valid JSON file or is missing.
            FileNotFoundError: If the specified conversation file does not exist.
        """
        if not os.path.exists(path):
            os.makedirs(path)  # Create directory if it does not exist

        if user is not None:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        self.path = path

        # Load an existing conversation or create a new one
        if conversation_file:
            # Validate that conversation_file is a JSON file
            if not conversation_file.endswith('.json'):
                raise ValueError("The conversation_file must be a valid JSON file with the '.json' extension.")

            full_conversation_file = os.path.join(self.path, conversation_file)

            if os.path.exists(full_conversation_file):
                # Load existing conversation
                try:
                    with open(full_conversation_file, 'r') as f:
                        self.conversation = json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Error decoding JSON from file '{conversation_file}': {e}")

                self.conversation_id = self.conversation['conversation']['header']['id']
                self.user = self.conversation['conversation']['header']['user']
                self.title = self.conversation['conversation']['header']['title']
                self.timestamp = self.conversation['conversation']['header']['timestamp']
                self.system_message = system_message or self.conversation['conversation']['system_message']
                self.messages = self.conversation['conversation']['messages']
                self.filename = self.conversation['conversation']['header']['filename']
                self.full_filepath = os.path.join(self.path, self.filename)
            else:
                raise FileNotFoundError(f"The file '{conversation_file}' does not exist.")
        else:
            # Create a new conversation
            if system_message is None:
                raise ValueError("A 'system_message' is required to start a new conversation.")

            self.system_message = system_message
            self.user = user
            self.title = title.replace('.', '')
            self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
            # Generate a unique ID for the conversation using a hash of the system_message and timestamp
            hash_input = (system_message + self.timestamp).encode('utf-8')
            self.conversation_id = hashlib.md5(hash_input).hexdigest()[:12]
            self.filename = f"{self.conversation_id}_{self.title.lower().replace(' ', '_')}.json"
            self.full_filepath = os.path.join(self.path, self.filename)
            self.messages = []

            # Build the conversation object
            self.conversation = {
                "conversation": {
                    "header": {
                        "id": self.conversation_id,
                        "user": self.user,
                        "title": self.title,
                        "timestamp": self.timestamp,
                        "filename": self.filename
                    },
                    "system_message": self.system_message,
                    "messages": self.messages
                }
            }

            # Create the JSON file with the title and ID in the filename
            try:
                with open(self.full_filepath, 'w') as f:
                    json.dump(self.conversation, f, indent=2)
            except IOError as e:
                print(f"Error writing file {self.full_filepath}: {e}")

    def add_message(self, message_dict: dict, timestamp: str | datetime = None):
        """
        Adds a new message to the conversation.

        Args:
            message_dict (dict): Dictionary containing:
                - role (str): The role of the sender (e.g., 'user' or 'assistant').
                - content (str): The content of the message.
                - timestamp (str, optional): The timestamp of the message (default is current UTC time).

        Raises:
            ValueError: If 'role' or 'content' are missing or not strings.
        """
        role = message_dict.get('role')
        content = message_dict.get('content')

        if not isinstance(role, str):
            raise ValueError("'role' must be a string.")
        if not isinstance(content, str):
            raise ValueError("'content' must be a string.")

        timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        # Generate a unique ID for the message using a hash of the content and timestamp
        hash_input = (content + timestamp).encode('utf-8')
        message_id = hashlib.md5(hash_input).hexdigest()[:12]

        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp,
            "id": message_id
        }
        self.messages.append(message)
        self.conversation['conversation']['messages'] = self.messages

        # Update the JSON file
        try:
            with open(self.full_filepath, 'w') as f:
                json.dump(self.conversation, f, indent=2)
        except IOError as e:
            print(f"Error writing file {self.full_filepath}: {e}")

    def set_system_message(self, new_system_message: str):
        """
        Updates the system message (context) of the conversation.

        Args:
            new_system_message (str): The new system message or context.
        """
        self.system_message = new_system_message
        self.conversation['conversation']['system_message'] = new_system_message

        # Update the JSON file
        try:
            with open(self.full_filepath, 'w') as f:
                json.dump(self.conversation, f, indent=2)
        except IOError as e:
            print(f"Error writing file {self.full_filepath}: {e}")

    def set_title(self, new_title: str):
        """
        Modifies the title of the conversation.

        Args:
            new_title (str): The new title of the conversation.

        Raises:
            OSError: If there is an error renaming the file.
        """
        old_full_filepath = self.full_filepath
        self.title = new_title.replace('.', '')
        self.filename = f"{self.conversation_id}_{self.title.lower().replace(' ', '_')}.json"
        self.full_filepath = os.path.join(self.path, self.filename)
        self.conversation['conversation']['header']['title'] = self.title
        self.conversation['conversation']['header']['filename'] = self.filename

        # Rename the file
        try:
            os.rename(old_full_filepath, self.full_filepath)
        except OSError as e:
            print(f"Error renaming file from {old_full_filepath} to {self.full_filepath}: {e}")

        # Update the JSON file
        try:
            with open(self.full_filepath, 'w') as f:
                json.dump(self.conversation, f, indent=2)
        except IOError as e:
            print(f"Error writing file {self.full_filepath}: {e}")

    def get_system_message(self) -> str:
        """
        Retrieves the current system message of the conversation.

        Returns:
            str: The system message or context of the conversation.
        """
        return self.system_message + datetime.now().strftime('%Y-%m-%d')

    def get_filename(self) -> str:
        """
        Returns the filename where the conversation is stored.

        Returns:
            str: The filename of the JSON file.
        """
        return self.filename

    def get_conversation(self) -> dict:
        """
        Returns the entire conversation object.

        Returns:
            dict: The full conversation object containing header, system_message, and messages.
        """
        return self.conversation

    def get_header(self) -> dict:
        """
        Returns the header information of the current conversation.

        Returns:
            dict: The header containing id, user, title, timestamp, and filename of the conversation.
        """
        return self.conversation['conversation']['header']

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

    @staticmethod
    def get_headers_from(user: str, path: str = 'conversations/') -> list:
        """
        Retrieves the headers of all conversations associated with a specific user.

        Args:
            user (str): The user whose conversations are being queried.
            path (str, optional): The directory where conversations are stored (default is 'conversations/').

        Returns:
            list: A list of headers from the user's conversations.
        """
        if user:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        # Check if the directory exists
        if os.path.exists(path) and os.path.isdir(path):
            headers = []
            # Iterate over the JSON files in the directory
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path) and file.endswith('.json'):
                    # Load the JSON file and extract the header
                    try:
                        with open(full_path, 'r') as f:
                            conversation = json.load(f)
                            header = conversation.get('conversation', {}).get('header', {})
                            headers.append(header)
                    except (json.JSONDecodeError, IOError):
                        # Skip files with errors
                        continue
            return headers
        return []
