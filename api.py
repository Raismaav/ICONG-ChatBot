from fastapi import FastAPI, HTTPException
from message_manager import MessageManager
from pydantic import BaseModel
from typing import Optional
from dateutil import parser
from chat import Chat
import json

app = FastAPI()


# Data models for requests
class ChatRespondRequest(BaseModel):
    """
    Model for the /chat/respond request.

    Attributes:
        user (str): The user interacting with the chat.
        message (str): The message content sent by the user.
        have_tools (Optional[bool]): Whether the assistant has tools available (default is False).
        conversation_file (Optional[str]): File path to an existing conversation (default is None).
        timestamp (Optional[str]): Timestamp of the message in ISO format (default is None).
    """
    user: str
    message: str
    have_tools: Optional[bool] = False
    conversation_file: Optional[str] = None
    timestamp: Optional[str] = None


class ChatSetTitleRequest(BaseModel):
    """
    Model for the /chat/set_title request.

    Attributes:
        user (str): The user interacting with the chat.
        new_title (str): The new title to set for the conversation.
        conversation_file (str): File path to an existing conversation.
    """
    user: str
    new_title: str
    conversation_file: str


# Endpoint for /chat/respond
@app.post('/chat/respond')
async def chat_respond(request: ChatRespondRequest):
    """
    Handles the /chat/respond endpoint, processing a user message and generating a response from the assistant.

    Args:
        request (ChatRespondRequest): Request object containing user, message, tools, conversation file, and timestamp.

    Returns:
        dict: The assistant's response.

    Raises:
        HTTPException: If the conversation file is not found, or if there are JSON or general processing errors.
    """
    try:
        # Process and validate the timestamp if provided
        if request.timestamp:
            try:
                # Parse and convert the timestamp to a valid date-time format
                parsed_timestamp = parser.isoparse(request.timestamp).isoformat()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format")
        else:
            parsed_timestamp = None

        # Create or load a Chat instance
        chat = Chat(
            user=request.user,
            have_tools=request.have_tools,
            conversation_file=request.conversation_file,
            timestamp=parsed_timestamp  # Use parsed timestamp or None
        )

        # Process the message and obtain the response
        response = chat.response_to(request.message, parsed_timestamp)

        return response

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for /chat/set_title
@app.post('/chat/set_title')
async def chat_set_title(request: ChatSetTitleRequest):
    """
    Handles the /chat/set_title endpoint, allowing users to change the conversation's title.

    Args:
        request (ChatSetTitleRequest): Request object containing user, new title, and conversation file.

    Returns:
        dict: A success message if the title was updated.

    Raises:
        HTTPException: If the conversation file is missing, not found, or contains errors.
    """
    try:
        if not request.conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file is required')

        # Load the Chat instance
        chat = Chat(
            user=request.user,
            conversation_file=request.conversation_file
        )

        # Set the new title
        chat.set_title(request.new_title)

        return {'message': 'Title updated successfully'}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for /chat/last_message
@app.get('/chat/last_message')
async def chat_last_message(user: str, conversation_file: str):
    """
    Handles the /chat/last_message endpoint, retrieving the last message from a conversation.

    Args:
        user (str): The user interacting with the chat.
        conversation_file (str): File path to the conversation.

    Returns:
        dict: The last message in the conversation.

    Raises:
        HTTPException: If the conversation file or user information is missing, not found, or contains errors.
    """
    try:
        if not conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file is required')
        if not user:
            raise HTTPException(status_code=400, detail='user is required')

        # Load the Chat instance
        chat = Chat(
            user=user,
            conversation_file=conversation_file
        )

        # Get the last message
        last_message = chat.conversation.get_last_message()

        return last_message

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for /chat/messages
@app.get('/chat/messages')
async def chat_messages(user: str, conversation_file: str):
    """
    Handles the /chat/messages endpoint, retrieving all messages from a conversation.

    Args:
        user (str): The user interacting with the chat.
        conversation_file (str): File path to the conversation.

    Returns:
        list: A list of messages in the conversation.

    Raises:
        HTTPException: If the conversation file or user information is missing, not found, or contains errors.
    """
    try:
        if not conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file is required')
        if not user:
            raise HTTPException(status_code=400, detail='user is required')

        # Load the Chat instance
        chat = Chat(
            user=user,
            conversation_file=conversation_file
        )

        # Get all messages
        messages = chat.conversation.get_messages()

        return messages

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for /chat/conversation
@app.get('/chat/conversation')
async def chat_conversation(user: str, conversation_file: str):
    """
    Handles the /chat/conversation endpoint, retrieving the entire conversation object.

    Args:
        user (str): The user interacting with the chat.
        conversation_file (str): File path to the conversation.

    Returns:
        dict: The full conversation object.

    Raises:
        HTTPException: If the conversation file or user information is missing, not found, or contains errors.
    """
    try:
        if not conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file is required')
        if not user:
            raise HTTPException(status_code=400, detail='user is required')

        # Load the Chat instance
        chat = Chat(
            user=user,
            conversation_file=conversation_file
        )

        # Get the conversation
        conversation = chat.conversation.get_conversation()

        return conversation

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for /chat/headers
@app.get('/chat/headers')
async def chat_headers(user: str):
    """
    Handles the /chat/headers endpoint, retrieving the headers of all conversations for a user.

    Args:
        user (str): The user whose conversation headers should be retrieved.

    Returns:
        dict: A list of conversation headers for the user.

    Raises:
        HTTPException: If the user information is missing or if there are errors in processing the headers.
    """
    try:
        if not user:
            raise HTTPException(status_code=400, detail='user is required')

        # Get conversation headers
        headers = MessageManager.get_headers_from_user(user)

        return {'headers': headers}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))