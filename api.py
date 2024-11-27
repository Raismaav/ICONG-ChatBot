from datetime import datetime
from fastapi import FastAPI, HTTPException
from message_manager import MessageManager
from pydantic import BaseModel
from typing import List, Dict, Optional
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


class ChatDeleteRequest(BaseModel):
    """
    Model for the /chat/delete_conversation request.

    Attributes:
        user (str): The user whose conversation is being deleted.
        conversation_file (str): The filename of the conversation to be deleted.
    """
    user: str
    conversation_file: str

# Endpoint for /chat/respond
@app.post('/chat/respond')
async def chat_respond(request: ChatRespondRequest):
    """
    Handles the /chat/respond endpoint, processing a user message and generating a response from the assistant.

    Args:
        request (ChatRespondRequest): Request object containing user information, the message content, optional tool access,
                                      conversation file path, and an optional timestamp.

    Returns:
        dict: A dictionary containing the assistant's response and the conversation header.

    Raises:
        HTTPException: Raised under the following conditions:
            - If the conversation file is not found, with a 404 status code.
            - If the conversation file format is invalid JSON, with a 400 status code.
            - If there is an invalid date format in the timestamp, with a 400 status code.
            - For any other exceptions, with a 500 status code.
    """
    try:
        print("\033[95m/chat/respond:\033[0m \033[93mMensaje recibido\033[0m")
        # Process and validate the timestamp if provided
        if request.timestamp:
            try:
                # Attempt to parse the timestamp in ISO format or fallback format "%Y%m%d%H%M%S%f"
                try:
                    parsed_timestamp = parser.isoparse(request.timestamp).isoformat()
                except ValueError:
                    parsed_timestamp = datetime.strptime(request.timestamp, "%Y%m%d%H%M%S%f").isoformat()
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
        print("\033[95m/chat/respond:\033[0m \033[93mChat iniciado\033[0m")
        message = chat.response_to(request.message, parsed_timestamp)
        return {"header": chat.conversation.get_header(), "message": message}

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
        dict: A success message and the updated conversation header.

    Raises:
        HTTPException: If the conversation file is missing, not found, or contains errors.
    """
    try:
        if not request.conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file is required')

        # Load the Chat instance
        conversation = MessageManager(
            user=request.user,
            conversation_file=request.conversation_file
        )

        # Set the new title
        conversation.set_title(request.new_title)

        return {'detail': 'Title updated successfully', "header": conversation.get_header()}

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
        conversation = MessageManager(
            user=user,
            conversation_file=conversation_file
        )

        # Get the last message
        return conversation.get_last_message()

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
        conversation = MessageManager(
            user=user,
            conversation_file=conversation_file
        )

        # Get all messages
        return conversation.get_messages()

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
        conversation = MessageManager(
            user=user,
            conversation_file=conversation_file
        )

        # Get the conversation
        return conversation.get_conversation()

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/chat/headers')
async def chat_headers(user: str):
    """
    Handles the /chat/headers endpoint, retrieving the headers of all conversations for a user.

    Args:
        user (str): The user whose conversation headers should be retrieved.

    Returns:
        list: A list of conversation headers for the user.

    Raises:
        HTTPException: If the user information is missing or if there are errors in processing the headers.
    """
    try:
        if not user:
            raise HTTPException(status_code=400, detail='user is required')

        # Get conversation headers
        return MessageManager.get_headers_from(user)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid conversation file format')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint for /chat/delete_conversation
@app.delete('/chat/delete')
async def delete(request: ChatDeleteRequest):
    """
    Handles the /chat/delete_conversation endpoint, deleting a specific conversation for a user.

    Args:
        request (ChatDeleteRequest): Request object containing user and conversation file.

    Returns:
        dict: A success message if the conversation was deleted successfully.

    Raises:
        HTTPException: If the conversation file is not found or if there are errors during deletion.
    """
    try:
        if not request.conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file is required')
        if not request.user:
            raise HTTPException(status_code=400, detail='user is required')

        # Delete the conversation
        if MessageManager.delete_conversation(request.user, request.conversation_file):
            return {'detail': 'Conversation deleted successfully'}
        else:
            raise HTTPException(status_code=500, detail='Failed to delete the conversation')

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Conversation file not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
