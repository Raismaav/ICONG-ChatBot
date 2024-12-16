from system_message import system_message
from datetime import datetime, timezone
import hashlib
import json
import os


class MessageManager:
    """
    Manages conversations and messages, storing them in JSON files with unique identifiers.
    It supports creating new conversations, adding messages, updating conversation details, and resuming previous conversations.

    Attributes:
        path (str): Directory where the conversation files are stored.
        conversation_id (str): Unique identifier of the conversation (based on system message and timestamp).
        user (str): The user associated with the conversation.
        title (str): Title of the conversation.
        timestamp (str): Timestamp of when the conversation was created (in ISO 8601 format).
        last_modified (str): Timestamp of the last modification to the conversation (in ISO 8601 format).
        system_message (str): Initial system message or context for the conversation.
        messages (list): List of messages in the conversation, each with role, content, timestamp, and a unique ID.
        filename (str): The JSON file where the conversation is stored.
    """
    def __init__(self, system_message: str = system_message, user: str = None, title: str = 'New conversation',
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
        if user is not None:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        if not os.path.exists(path):
            os.makedirs(path)  # Create directory if it does not exist

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
                self.last_modified = self.conversation['conversation']['header']['last_modified']
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
            self.last_modified = self.timestamp
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
                        "last_modified": self.last_modified,
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
        Adds a new message to the conversation and updates the last_modified timestamp.

        Args:
            message_dict (dict): Dictionary containing:
                - role (str): The role of the sender (e.g., 'user' or 'assistant').
                - content (str): The content of the message.
                - timestamp (str, optional): The timestamp of the message (default is current UTC time).

        Raises:
            ValueError: If 'role' or 'content' are missing or not strings.
        """
        timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        role = message_dict.get('role')
        content = message_dict.get('content')

        if not isinstance(role, str):
            raise ValueError("'role' must be a string.")
        if not isinstance(content, str):
            raise ValueError("'content' must be a string.")

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
        self.last_modified = timestamp
        self.conversation['conversation']['header']['last_modified'] = self.last_modified

        # Update the JSON file
        try:
            with open(self.full_filepath, 'w') as f:
                json.dump(self.conversation, f, indent=2)
        except IOError as e:
            print(f"Error writing file {self.full_filepath}: {e}")

    def set_system_message(self, new_system_message: str):
        """
        Updates the system message (context) of the conversation and the last_modified timestamp.

        Args:
            new_system_message (str): The new system message or context.
        """
        self.last_modified = datetime.now(timezone.utc).isoformat()
        self.system_message = new_system_message
        self.conversation['conversation']['system_message'] = new_system_message
        self.conversation['conversation']['header']['last_modified'] = self.last_modified

        # Update the JSON file
        try:
            with open(self.full_filepath, 'w') as f:
                json.dump(self.conversation, f, indent=2)
        except IOError as e:
            print(f"Error writing file {self.full_filepath}: {e}")

    def set_title(self, new_title: str):
        """
        Modifies the title of the conversation and updates the last_modified timestamp.

        Args:
            new_title (str): The new title of the conversation.

        Raises:
            OSError: If there is an error renaming the file.
        """
        self.last_modified = datetime.now(timezone.utc).isoformat()
        old_full_filepath = self.full_filepath
        self.title = ''.join(c for c in new_title if c.isalnum() or c in (' ', '_')).strip()
        self.filename = f"{self.conversation_id}_{self.title.lower().replace(' ', '_').replace('.', '').replace('/', '')}.json"
        self.full_filepath = os.path.join(self.path, self.filename)
        self.conversation['conversation']['header']['title'] = self.title
        self.conversation['conversation']['header']['filename'] = self.filename
        self.conversation['conversation']['header']['last_modified'] = self.last_modified

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
        Retrieves the current system message of the conversation, appending the current date.

        Returns:
            str: The system message of the conversation, followed by a note with the current date.
                 This date is included as a reminder for time-sensitive processes or database queries.
        """
        return self.system_message + f" Debes tomar en cuenta la fecha de hoy para posibles consultas en la base de datos o cuando tengas que hacer algún proceso con cierta temporalidad, la fecha del día de hoy es {datetime.now().strftime('%Y-%m-%d')}"

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
            dict: The header containing id, user, title, timestamp, last_modified, and filename of the conversation.
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
            list: A list of dictionaries, where each dictionary contains:
                - 'role' (str): The role of the sender (e.g., 'user', 'assistant').
                - 'content' (str): The content of the message.
        """
        return [{'role': msg['role'], 'content': msg['content']} for msg in self.messages]

    def get_last_message(self) -> dict:
        """
        Returns the last message added to the conversation.

        Returns:
            dict: The last message in the conversation, containing:
                - 'role' (str): The role of the sender.
                - 'content' (str): The content of the message.
                - 'timestamp' (str): The timestamp when the message was added.
                - 'id' (str): The unique identifier for the message.
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

    @staticmethod
    def delete_conversation(user: str, conversation_file: str, path: str = 'conversations/') -> bool:
        """
        Deletes a specific conversation associated with a user.

        Args:
            user (str): The user whose conversation is being deleted.
            conversation_file (str): The filename of the conversation to be deleted.
            path (str, optional): The directory where conversation files are stored (default is 'conversations/').

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if user:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        full_conversation_file = os.path.join(path, conversation_file)

        if os.path.exists(full_conversation_file) and os.path.isfile(full_conversation_file):
            try:
                os.remove(full_conversation_file)
                return True
            except (OSError, IOError) as e:
                print(f"Error deleting conversation file '{conversation_file}': {e}")
                return False
        return False

    @staticmethod
    def delete_all_conversations(user: str, path: str = 'conversations/') -> bool:
        """
        Deletes all conversations associated with a specific user, but keeps the user's directory.

        Args:
            user (str): The user whose conversations are being deleted.
            path (str, optional): The directory where conversation files are stored (default is 'conversations/').

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if user:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        if os.path.exists(path) and os.path.isdir(path):
            try:
                # Delete all files in the user's directory
                for file in os.listdir(path):
                    full_path = os.path.join(path, file)
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                return True
            except (OSError, IOError) as e:
                print(f"Error deleting conversation files: {e}")
                return False
        return False
