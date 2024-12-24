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

Este proyecto utiliza las siguientes bibliotecas:

```plaintext
aiohappyeyeballs==2.4.3
aiohttp==3.10.10
aiosignal==1.3.1
annotated-types==0.7.0
anyio==4.6.0
argcomplete==1.10.3
attrs==24.2.0
beautifulsoup4==4.8.2
certifi==2024.8.30
chardet==3.0.4
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
compressed-rtf==1.0.6
contourpy==1.3.0
cycler==0.12.1
distro==1.9.0
docx2txt==0.8
ebcdic==1.1.1
extract-msg==0.28.7
fastapi==0.115.0
fonttools==4.54.1
frozenlist==1.5.0
h11==0.14.0
httpcore==1.0.6
httpx==0.27.2
idna==3.10
IMAPClient==2.1.0
jiter==0.5.0
kiwisolver==1.4.7
lxml==5.3.0
matplotlib==3.9.2
multidict==6.1.0
mysql-connector-python==9.0.0
numpy==2.1.1
olefile==0.47
openai==1.51.0
packaging==24.1
pdfminer.six==20191110
pillow==10.4.0
propcache==0.2.0
pycryptodome==3.21.0
pydantic==2.9.2
pydantic_core==2.23.4
pyparsing==3.1.4
PyPDF2==3.0.1
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
python-pptx==0.6.23
requests==2.32.3
six==1.12.0
sniffio==1.3.1
sortedcontainers==2.4.0
soupsieve==2.6
SpeechRecognition==3.8.1
starlette==0.38.6
textract==1.6.5
tqdm==4.66.5
typing_extensions==4.12.2
tzdata==2024.2
tzlocal==5.2
urllib3==2.2.3
uvicorn==0.31.0
xlrd==1.2.0
XlsxWriter==3.2.0
yarl==1.17.1
```

## Uso

1. Configura las variables de entorno en el archivo `.env`.
2. Ejecuta el servidor FastAPI en modo desarrollo:

    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8080 --reload
    ```

3. Para un despliegue en producción, utiliza el siguiente comando:

    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
    ```

4. Accede a la documentación interactiva en:

    ```plaintext
    http://127.0.0.1:8080/docs
    ```

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
