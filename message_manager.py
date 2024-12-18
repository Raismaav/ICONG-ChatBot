import os
import json
import hashlib
from datetime import datetime, timezone
from pydantic import ValidationError

from system_message import system_message
from pydantic import BaseModel
from typing import Optional, List


class ConversationHeader(BaseModel):
    """Defines the metadata for a conversation."""
    id: str
    user: Optional[str] = None
    title: str
    timestamp: str
    last_modified: str
    filename: str


class MessageModel(BaseModel):
    """Defines the structure of an individual message."""
    role: str
    content: str
    timestamp: str
    id: str


class ConversationData(BaseModel):
    """Defines the data structure for a conversation."""
    header: ConversationHeader
    system_message: str
    messages: List[MessageModel] = []


class FullConversationModel(BaseModel):
    """Defines the full structure of a conversation, including metadata and messages."""
    conversation: ConversationData


class MessageManager:
    """
    Manages conversations and messages, storing them in JSON files with unique identifiers.
    Supports creating, updating, and retrieving conversations and messages.

    Attributes:
        path (str): Directory where conversation files are stored.
        conversation (FullConversationModel): Pydantic object containing all conversation data.
        full_filepath (str): Full path to the current JSON file.
    """
    def __init__(self, system_message: str = system_message, user: str = None, title: str = 'New conversation',
                 timestamp: str | datetime = None, conversation_file: str = None, path: str = 'conversations/'):
        """
        Initializes a new conversation or loads an existing one from a JSON file.

        Args:
            system_message (str, optional): The initial system message or context for the conversation.
            user (str, optional): The user associated with the conversation (default is None).
            title (str, optional): The title of the conversation (default is 'New conversation').
            timestamp (str | datetime, optional): The timestamp of the conversation (default is current UTC time).
            conversation_file (str, optional): The path to an existing JSON file to load the conversation (default is None).
            path (str, optional): The directory where conversation files are stored (default is 'conversations/').

        Raises:
            ValueError: If `system_message` is None when creating a new conversation.
            ValueError: If `conversation_file` is invalid or missing.
            FileNotFoundError: If the specified conversation file does not exist.
        """
        if user is not None:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        if not os.path.exists(path):
            os.makedirs(path)

        self.path = path

        if conversation_file:
            # Carga una conversación existente desde JSON
            if not conversation_file.endswith('.json'):
                raise ValueError("The conversation_file must be a valid JSON file with the '.json' extension.")

            full_conversation_file = os.path.join(self.path, conversation_file)
            if not os.path.exists(full_conversation_file):
                raise FileNotFoundError(f"The file '{conversation_file}' does not exist.")

            # Cargar el JSON y parsearlo con Pydantic
            with open(full_conversation_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Error decoding JSON from file '{conversation_file}': {e}")

            try:
                self.conversation = FullConversationModel(**data)
            except ValidationError as e:
                raise ValueError(f"Error validating conversation data: {e}")

            # Si el usuario pasa un system_message nuevo, lo sobreescribimos
            if system_message is not None:
                self.conversation.conversation.system_message = system_message

            self.full_filepath = os.path.join(self.path, self.conversation.conversation.header.filename)

        else:
            # Crear una conversación nueva
            if system_message is None:
                raise ValueError("A 'system_message' is required to start a new conversation.")

            current_timestamp = (
                timestamp if isinstance(timestamp, str)
                else (timestamp or datetime.now(timezone.utc)).isoformat()
                if isinstance(timestamp, datetime) else datetime.now(timezone.utc).isoformat()
            )

            last_modified = current_timestamp
            # Generamos un ID único con el hash del system_message + timestamp
            hash_input = (system_message + current_timestamp).encode('utf-8')
            conversation_id = hashlib.md5(hash_input).hexdigest()[:12]

            sanitized_title = title.replace('.', '')
            filename = f"{conversation_id}_{sanitized_title.lower().replace(' ', '_')}.json"
            full_filepath = os.path.join(self.path, filename)

            header = ConversationHeader(
                id=conversation_id,
                user=user,
                title=sanitized_title,
                timestamp=current_timestamp,
                last_modified=last_modified,
                filename=filename
            )

            conversation_data = ConversationData(
                header=header,
                system_message=system_message,
                messages=[]
            )

            self.conversation = FullConversationModel(conversation=conversation_data)
            self.full_filepath = full_filepath

            # Guardar el archivo inicial
            self._save_to_file()

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
        current_timestamp = (
            timestamp if isinstance(timestamp, str)
            else (timestamp or datetime.now(timezone.utc)).isoformat()
            if isinstance(timestamp, datetime) else datetime.now(timezone.utc).isoformat()
        )
        role = message_dict.get('role')
        content = message_dict.get('content')

        if not isinstance(role, str):
            raise ValueError("'role' must be a string.")
        if not isinstance(content, str):
            raise ValueError("'content' must be a string.")

        hash_input = (content + current_timestamp).encode('utf-8')
        message_id = hashlib.md5(hash_input).hexdigest()[:12]

        new_message = MessageModel(
            role=role,
            content=content,
            timestamp=current_timestamp,
            id=message_id
        )

        self.conversation.conversation.messages.append(new_message)
        # Actualizar last_modified en el header
        self.conversation.conversation.header.last_modified = current_timestamp

        # Guardar en disco
        self._save_to_file()

    def set_system_message(self, new_system_message: str):
        """
        Updates the system message (context) of the conversation and the last_modified timestamp.

        Args:
            new_system_message (str): The new system message or context.
        """
        current_timestamp = datetime.now(timezone.utc).isoformat()
        self.conversation.conversation.system_message = new_system_message
        self.conversation.conversation.header.last_modified = current_timestamp

        self._save_to_file()

    def set_title(self, new_title: str):
        """
        Modifies the title of the conversation and updates the last_modified timestamp.

        Args:
            new_title (str): The new title of the conversation.

        Raises:
            OSError: If there is an error renaming the file.
        """
        current_timestamp = datetime.now(timezone.utc).isoformat()
        old_full_filepath = self.full_filepath

        # Sanitizar el título (solo letras, números, espacios y guiones bajos)
        sanitized_title = ''.join(c for c in new_title if c.isalnum() or c in (' ', '_')).strip()

        # Generar nuevo filename
        conversation_id = self.conversation.conversation.header.id
        filename = f"{conversation_id}_{sanitized_title.lower().replace(' ', '_')}.json"

        # Actualizar Pydantic model
        self.conversation.conversation.header.title = sanitized_title
        self.conversation.conversation.header.filename = filename
        self.conversation.conversation.header.last_modified = current_timestamp

        self.full_filepath = os.path.join(self.path, filename)

        # Renombrar archivo
        try:
            os.rename(old_full_filepath, self.full_filepath)
        except OSError as e:
            print(f"Error renaming file from {old_full_filepath} to {self.full_filepath}: {e}")

        self._save_to_file()

    def get_title(self) -> str:
        """Retorna el titulo de la conversacion."""
        return self.conversation.conversation.header.title

    def get_system_message(self) -> str:
        """
        Retrieves the current system message of the conversation, appending the current date.

        Returns:
            str: The system message of the conversation, followed by a note with the current date.
                 This date is included as a reminder for time-sensitive processes or database queries.
        """
        base_msg = self.conversation.conversation.system_message
        today = datetime.now().strftime('%Y-%m-%d')
        return base_msg + f" Debes tomar en cuenta la fecha de hoy: {today}"

    def get_filename(self) -> str:
        """
        Returns the filename where the conversation is stored.

        Returns:
            str: The filename of the JSON file.
        """
        return self.conversation.conversation.header.filename

    def get_conversation(self) -> dict:
        """
        Returns the entire conversation object.

        Returns:
            dict: The full conversation object containing header, system_message, and messages.
        """
        return self.conversation.dict()

    def get_header(self) -> dict:
        """
        Returns the header of the current conversation.

        Returns:
            dict: The header containing id, user, title, timestamp, last_modified, and filename.
        """
        return self.conversation.conversation.header.dict()

    def get_messages(self) -> list:
        """
        Returns the full list of messages in the conversation.

        Returns:
            list: A list of messages, each containing role, content, timestamp, and ID.
        """
        return [msg.dict() for msg in self.conversation.conversation.messages]

    def get_filtered_messages(self) -> list:
        """
        Returns a filtered list of messages containing only the role and content.

        Returns:
            list: A list of dictionaries with:
                - role (str): The role of the sender (e.g., 'user', 'assistant').
                - content (str): The content of the message.
        """
        return [
            {'role': msg.role, 'content': msg.content}
            for msg in self.conversation.conversation.messages
        ]

    def get_last_message(self) -> dict:
        """
        Returns the last message in the conversation.

        Returns:
            dict: The last message, containing role, content, timestamp, and ID.
                If there are no messages, returns an empty dictionary.
        """
        if self.conversation.conversation.messages:
            return self.conversation.conversation.messages[-1].dict()
        return {}

    def get_message_count(self) -> int:
        """
        Returns the total number of messages in the conversation.

        Returns:
            int: The number of messages in the conversation.
        """
        return len(self.conversation.conversation.messages)

    @staticmethod
    def get_headers_from(user: str, path: str = 'conversations/') -> list:
        """
        Retrieves the headers of all conversations associated with a specific user.

        Args:
            user (str): The user whose conversations are being queried.
            path (str, optional): The directory where conversation files are stored (default is 'conversations/').

        Returns:
            list: A list of headers for the user's conversations.
        """
        if user:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        if not os.path.exists(path) or not os.path.isdir(path):
            return []

        headers = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path) and file.endswith('.json'):
                try:
                    with open(full_path, 'r') as f:
                        data = json.load(f)
                    conv = FullConversationModel(**data)  # validación con Pydantic
                    headers.append(conv.conversation.header.dict())
                except (json.JSONDecodeError, ValidationError, IOError):
                    # Ignorar archivos corruptos o que no cumplan con la estructura
                    continue
        return headers

    @staticmethod
    def delete_conversation(user: str, conversation_file: str, path: str = 'conversations/') -> bool:
        """
        Deletes a specific conversation associated with a user.

        Args:
            user (str): The user whose conversation is being deleted.
            conversation_file (str): The filename of the conversation to delete.
            path (str, optional): Directory where conversation files are stored (default is 'conversations/').

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
        Deletes all conversations for a specific user while keeping the user's directory.

        Args:
            user (str): The user whose conversations are being deleted.
            path (str, optional): Directory where conversation files are stored (default is 'conversations/').

        Returns:
            bool: True if all conversations were successfully deleted, False otherwise.
        """
        if user:
            path = f"{path}{user.lower().replace(' ', '_')}/"

        if not os.path.exists(path) or not os.path.isdir(path):
            return False

        try:
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    os.remove(full_path)
            return True
        except (OSError, IOError) as e:
            print(f"Error deleting conversation files: {e}")
            return False

    def __save_to_file(self):
        """
        Saves the current state of the conversation to its JSON file.

        Raises:
            IOError: If there is an error writing to the file.
        """
        try:
            with open(self.full_filepath, 'w') as f:
                json.dump(self.conversation.dict(), f, indent=2)
        except IOError as e:
            print(f"Error writing file {self.full_filepath}: {e}")