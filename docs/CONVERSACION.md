# Esquema General de una Conversación

Este archivo describe la estructura de una conversación y las acciones que realiza él `MessageManager` para su manipulación.

## Esquema General

```json
{
  "conversation": {
    "header": {
      "id": "string",
      "user": "string",
      "title": "string",
      "timestamp": "string",
      "last_modified": "string",
      "filename": "string"
    },
    "system_message": "string",
    "messages": [
      {
        "role": "string",
        "content": "string",
        "timestamp": "string",
        "id": "string"
      }
    ]
  }
}
```

### Descripción de los campos

#### `header`
- **id**: Identificador único de la conversación.
- **user**: Usuario asociado a la conversación.
- **title**: Título descriptivo de la conversación.
- **timestamp**: Marca temporal de creación de la conversación.
- **last_modified**: Marca temporal de la última modificación.
- **filename**: Nombre del archivo donde se guarda la conversación.

#### `system_message`
- Mensaje del sistema que establece el contexto o reglas para la interacción.

#### `messages`
- Lista de mensajes intercambiados en la conversación.
  - **role**: Rol del autor del mensaje (`user` o `assistant`).
  - **content**: Contenido textual del mensaje.
  - **timestamp**: Marca temporal del mensaje.
  - **id**: Identificador único del mensaje.

## Acciones del `MessageManager`

### 1. Crear Conversación
- Genera una nueva conversación con un encabezado inicial, un mensaje del sistema y una lista vacía de mensajes.
- Asigna un ID único utilizando un hash basado en el contenido inicial.

### 2. Agregar Mensaje
- Añade un nuevo mensaje a la lista `messages`.
- Actualiza el campo `last_modified` del encabezado.
- Genera un ID único para el mensaje utilizando un hash basado en su contenido y marca temporal.

### 3. Guardar Conversación
- Guarda la conversación completa en un archivo JSON.
- Utiliza el campo `filename` para determinar la ruta y nombre del archivo.

### 4. Cargar Conversación
- Carga una conversación desde un archivo JSON.
- Verifica la estructura y la integridad de los datos antes de procesarlos.

### 5. Modificar Título
- Cambia el título de la conversación.
- Actualiza el campo `last_modified` y renombra el archivo correspondiente.

### 6. Eliminar Mensaje
- Elimina un mensaje específico de la lista `messages` utilizando su ID.
- Actualiza el campo `last_modified`.

## Ejemplo

```json
{
  "conversation": {
    "header": {
      "id": "e5bc72a6b5a5",
      "user": "rafael",
      "title": "Lo siento no puedo responder a eso",
      "timestamp": "2024-12-26T19:39:01.393128+00:00",
      "last_modified": "2024-12-26T19:39:21.479629+00:00",
      "filename": "e5bc72a6b5a5_lo_siento_no_puedo_responder_a_eso.json"
    },
    "system_message": "Rol: un asesor experto y tutor en contabilidad gubernamental en México, especializado en...",
    "messages": [
      {
        "role": "user",
        "content": "Hola",
        "timestamp": "2024-12-26T19:39:11.210349+00:00",
        "id": "e05f5ffddede"
      },
      {
        "role": "assistant",
        "content": "Lo siento, no puedo responder a eso.",
        "timestamp": "2024-12-26T19:39:11.678781+00:00",
        "id": "b427ee2bd6cf"
      }
    ]
  }
}
```
