# ICONG ChatBot

**ICONG ChatBot** es un proyecto diseñado para facilitar la interacción con los usuarios a través de un asistente virtual que asume el rol de Fray Luca Pacioli, un asesor experto y tutor en contabilidad gubernamental en México, especializado en la Normatividad emitida por el Consejo Nacional de Armonización Contable (CONAC), con un enfoque específico en el marco del estado de Jalisco y las normativas federales.

## Características principales

- Gestión eficiente de conversaciones.
- Manejo de datos estructurados mediante JSON.
- Interfaz personalizable para herramientas cliente.
- Especialización en normatividad gubernamental y generación de gráficos basados en datos contables.

## Requisitos previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación

Para configurar el entorno de desarrollo del proyecto, sigue estos pasos:

1. **Clona este repositorio en tu máquina local:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd ICONG-ChatBot
    ```

2. **Crea un entorno virtual:**

    ```bash
    python -m venv venv
    ```

3. **Activa el entorno virtual:**

    - En sistemas Unix/MacOS:
      ```bash
      source venv/bin/activate
      ```
    - En Windows:
      ```bash
      venv\Scripts\activate
      ```

4. **Instala las dependencias del proyecto:**

    ```bash
    pip install -r requirements.txt
    ```

## Dependencias

Las dependencias del proyecto se encuentran listadas en el archivo `requirements.txt`. Para instalar todas las bibliotecas necesarias, utiliza el siguiente comando:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye dependencias clave como:
- `fastapi`: Framework para construir APIs web rápidas y escalables.
- `uvicorn`: Servidor ASGI para ejecutar aplicaciones FastAPI.
- `openai`: Biblioteca para interactuar con la API de OpenAI.
- `matplotlib`, `numpy`: Herramientas para la generación y manipulación de gráficos y datos.
- `SpeechRecognition`, `pydantic`: Utilidades para reconocimiento de voz y validación de datos.

Para más detalles, consulta el contenido completo del archivo `requirements.txt`.

## Uso

Para más información sobre aspectos específicos del proyecto, consulta el archivo [CONSIDERACIONES.md](docs/CONSIDERACIONES.md). Este archivo contiene las consideraciones para mejoras futuras en el ámbito de mantenibilidad, escalabilidad y nuevas funcionalidades.

1. Configura las variables de entorno en el archivo `.env`.
2. Ejecuta el servidor FastAPI en modo desarrollo:

    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8080 --reload
    ```

3. Para un despliegue en producción, utiliza el siguiente comando:

    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
    ```

4. Accede a la documentación interactiva [aquí](http://127.0.0.1:8080/docs) una vez que el servidor esté en funcionamiento.

## Estructura del proyecto

- `api.py`: Define los endpoints del servidor y actúa como punto de entrada para la ejecución del servidor.
- `assistant.py`: Contiene la lógica principal para la interacción con el asistente virtual.
- `chat.py`: Se encarga de la gestión y seguimiento de las conversaciones.
- `client_tools.py`: Proporciona herramientas que se ejecutan en el cliente para ampliar las capacidades del chatbot.
- `context_manager.py`: Maneja los archivos y datos relacionados con el contexto conversacional.
- `main.py`: Archivo principal que inicia la ejecución de la aplicación en modo terminal.
- `message_manager.py`: Administra la creación, almacenamiento y organización de los mensajes del chatbot.
- `system_message.py`: Define el mensaje inicial del sistema, utilizado como base para las interacciones del asistente.
- `tool_manager.py`: Contiene herramientas adicionales que se ejecutan en el servidor para ampliar las capacidades del chatbot.

[![](https://mermaid.ink/img/pako:eNq1WFFu3DYQvQohIIAMry-wHwWMDYoEiJEgaX9aBwIrze6yoUiBpNwYsXupHqEX6wwpaUmJyrqIvR_rFTkzfDN8fEP5W1HrBoptUUtu7WvBD4a3t4rh59UrdvXjnynWDhcAyzojVC06LvG3AclroRVvuGW1Vgwk28v-T80aYJIz3klRo8W__6jnhxS-fdpsd-SOfQsj9LkiNHdgLHcIj23ZDVjLD3DDFX6b2BDdhXVcObS6Hn_HBlUlbGVA8RYatPlDa3mavqRpJVxVlb0Fs2XWmQ078juoHBraYL9J4FR7IWGw7Lg7Dj-daAEXb7sta7gDenzAiYt4MQO208pS8LINKZ3xRsSNqF0cBLE4oXqoxmhlzSVBlZg8RiLcFQ1BE8ZyQQ6gwOBCFVdNZcFVTjgJJZneadEE08dbFe_SVN50q2jBqg07g-6_4GNmnwg1fHWR4S6M5GylAL-h7ztQ12_jKXtvHbTVUDwWEvydsvscm7V4qCTztU2gQttR2r0h173UPKFKy7_iznwBZXFWpDTyZR3WY6Xu_LmRF1kqpSCHHW5gz3uJBSBo466f8AxwNhEIjyHHRj8yFDSMXaSMp92v9r2qia-l3yDPEYweMNmREw-UT-qcIelArgcP-pRAjljr3uc8J14T1IXv_-L4jLipeqTspRO8JMpMfn7updxFQzeUSGy_76ngqAu5cOeYESmPP4VLScDnh1EWniBGCSt504zrjUWtqFKhXqvLpEoQQpFOpBmUCv6qMkmteQeVIadTpjnbQ6JIs2oeljBWrKg4JPxr83Ely7xMuuoIvAGzOj0S1Rukp2kC4cBAc94SyeqSlL6zHmLvlfNWiVJdsr-RbjZohi9Amd0Mh0nXUX622hvdxl3wRKcM3MEfjwE4SOsYhTjP1ExHTkOTksVh7CrEU5zp-D_zFcofe21Z-eG-wTYo6gtEYDhdm7CtwXRvGvG-0M0piFpWk2Jtu5yrWGz9mjue1cq5URoxcGUW640fTLZw3qVnZ288CWP_HgWaUvh8FlZYLwUmmuUqRJQwutKwvcIs_SZFXE6FE6obsReQWXHUm3hmpRctd8voHBjf5v1l6Oko02K81GkYXiiQ8kcw-NZCdzZ8j7gfr3r6pZgf3TCXN1GbEaup_Sa7n16SaNsGVeHm0LeYjA0CvNI7_GIzKV-SNrrhLl5w_H14BPB03EPjSr3L74h04oAiTw-89npsS_qupuQzua4F2WvT_miMDm-Lfdcjj_X5UC_F44_-LRiVmqhce1I__zr-Dffq6qf5XXTLbotfLQ99hMuW1yggBg8RqiNtLP4-dROtEFoxC3gdvQBHscILnvH3cSownzxPDuQeHyYKsNMt3t8hbzwj9Fn78P7m7T5hbXXbK1H7_kht8vrD29FtVhXyzfe3sCT2Xjitmbcc8KbNLOe-MJp7vhmb3hN9E4knr3dUEmQXeRWbogXTctEU28Irwm3hjtDiJJk23Hwhs0e0473Tn-5VXWyd6WFTGN0fjsV2z6XFp76jq_rwH6NptOPqN61Pz9AIp83N8D8m-vP4H_1sn7I?type=png)](https://mermaid.live/edit#pako:eNq1WFFu3DYQvQohIIAMry-wHwWMDYoEiJEgaX9aBwIrze6yoUiBpNwYsXupHqEX6wwpaUmJyrqIvR_rFTkzfDN8fEP5W1HrBoptUUtu7WvBD4a3t4rh59UrdvXjnynWDhcAyzojVC06LvG3AclroRVvuGW1Vgwk28v-T80aYJIz3klRo8W__6jnhxS-fdpsd-SOfQsj9LkiNHdgLHcIj23ZDVjLD3DDFX6b2BDdhXVcObS6Hn_HBlUlbGVA8RYatPlDa3mavqRpJVxVlb0Fs2XWmQ078juoHBraYL9J4FR7IWGw7Lg7Dj-daAEXb7sta7gDenzAiYt4MQO208pS8LINKZ3xRsSNqF0cBLE4oXqoxmhlzSVBlZg8RiLcFQ1BE8ZyQQ6gwOBCFVdNZcFVTjgJJZneadEE08dbFe_SVN50q2jBqg07g-6_4GNmnwg1fHWR4S6M5GylAL-h7ztQ12_jKXtvHbTVUDwWEvydsvscm7V4qCTztU2gQttR2r0h173UPKFKy7_iznwBZXFWpDTyZR3WY6Xu_LmRF1kqpSCHHW5gz3uJBSBo466f8AxwNhEIjyHHRj8yFDSMXaSMp92v9r2qia-l3yDPEYweMNmREw-UT-qcIelArgcP-pRAjljr3uc8J14T1IXv_-L4jLipeqTspRO8JMpMfn7updxFQzeUSGy_76ngqAu5cOeYESmPP4VLScDnh1EWniBGCSt504zrjUWtqFKhXqvLpEoQQpFOpBmUCv6qMkmteQeVIadTpjnbQ6JIs2oeljBWrKg4JPxr83Ely7xMuuoIvAGzOj0S1Rukp2kC4cBAc94SyeqSlL6zHmLvlfNWiVJdsr-RbjZohi9Amd0Mh0nXUX622hvdxl3wRKcM3MEfjwE4SOsYhTjP1ExHTkOTksVh7CrEU5zp-D_zFcofe21Z-eG-wTYo6gtEYDhdm7CtwXRvGvG-0M0piFpWk2Jtu5yrWGz9mjue1cq5URoxcGUW640fTLZw3qVnZ288CWP_HgWaUvh8FlZYLwUmmuUqRJQwutKwvcIs_SZFXE6FE6obsReQWXHUm3hmpRctd8voHBjf5v1l6Oko02K81GkYXiiQ8kcw-NZCdzZ8j7gfr3r6pZgf3TCXN1GbEaup_Sa7n16SaNsGVeHm0LeYjA0CvNI7_GIzKV-SNrrhLl5w_H14BPB03EPjSr3L74h04oAiTw-89npsS_qupuQzua4F2WvT_miMDm-Lfdcjj_X5UC_F44_-LRiVmqhce1I__zr-Dffq6qf5XXTLbotfLQ99hMuW1yggBg8RqiNtLP4-dROtEFoxC3gdvQBHscILnvH3cSownzxPDuQeHyYKsNMt3t8hbzwj9Fn78P7m7T5hbXXbK1H7_kht8vrD29FtVhXyzfe3sCT2Xjitmbcc8KbNLOe-MJp7vhmb3hN9E4knr3dUEmQXeRWbogXTctEU28Irwm3hjtDiJJk23Hwhs0e0473Tn-5VXWyd6WFTGN0fjsV2z6XFp76jq_rwH6NptOPqN61Pz9AIp83N8D8m-vP4H_1sn7I)