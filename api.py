from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import json
from chat import Chat

app = FastAPI()

# Modelos de datos para las solicitudes
class ChatRespondRequest(BaseModel):
    user: str
    message: str
    have_tools: Optional[bool] = False
    conversation_file: Optional[str] = None

class ChatSetTitleRequest(BaseModel):
    user: str
    new_title: str
    conversation_file: str

# Endpoint para /chat/respond
@app.post('/chat/respond')
async def chat_respond(request: ChatRespondRequest):
    try:
        # Crear o cargar la instancia de Chat
        chat = Chat(
            user=request.user,
            have_tools=request.have_tools,
            conversation_file=request.conversation_file
        )

        # Procesar el mensaje y obtener la respuesta
        response = chat.response_to(request.message)

        return response

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Archivo de conversación no encontrado')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Formato de archivo de conversación inválido')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para /chat/set_title
@app.post('/chat/set_title')
async def chat_set_title(request: ChatSetTitleRequest):
    try:
        if not request.conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file es obligatorio')

        # Cargar la instancia de Chat
        chat = Chat(
            user=request.user,
            conversation_file=request.conversation_file
        )

        # Modificar el título
        chat.conversation.set_title(request.new_title)

        return {'message': 'Título actualizado exitosamente'}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Archivo de conversación no encontrado')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Formato de archivo de conversación inválido')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para /chat/last_message
@app.get('/chat/last_message')
async def chat_last_message(user: str, conversation_file: str):
    try:
        if not conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file es obligatorio')
        if not user:
            raise HTTPException(status_code=400, detail='user es obligatorio')

        # Cargar la instancia de Chat
        chat = Chat(
            user=user,
            conversation_file=conversation_file
        )

        # Obtener el último mensaje
        last_message = chat.conversation.get_last_message()

        return last_message

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Archivo de conversación no encontrado')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Formato de archivo de conversación inválido')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para /chat/messages
@app.get('/chat/messages')
async def chat_messages(user: str, conversation_file: str):
    try:
        if not conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file es obligatorio')
        if not user:
            raise HTTPException(status_code=400, detail='user es obligatorio')

        # Cargar la instancia de Chat
        chat = Chat(
            user=user,
            conversation_file=conversation_file
        )

        # Obtener los mensajes
        messages = chat.conversation.get_messages()

        return messages

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Archivo de conversación no encontrado')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Formato de archivo de conversación inválido')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/chat/conversation')
async def chat_messages(user: str, conversation_file: str):
    try:
        if not conversation_file:
            raise HTTPException(status_code=400, detail='conversation_file es obligatorio')
        if not user:
            raise HTTPException(status_code=400, detail='user es obligatorio')

        # Cargar la instancia de Chat
        chat = Chat(
            user=user,
            conversation_file=conversation_file
        )

        # Obtener los mensajes
        messages = chat.conversation.get_conversation()

        return messages

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Archivo de conversación no encontrado')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Formato de archivo de conversación inválido')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))