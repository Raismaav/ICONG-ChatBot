import textract
import PyPDF2
import os

class ContextManager:
    def __init__(self):
        # Directory containing the context files
        context_files_dir = 'context_files'

        # List to store the titles
        titles = []

        # Iterate over each file in the directory
        for filename in os.listdir(context_files_dir):
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(os.path.join(context_files_dir, filename)):
                # Extract the title (assuming the title is the filename without extension)
                titles.append(f"{filename}")

        self.context_function = [{
            "type": "function",
            "function": {
                "name": "get_context_from",
                "description": "Retorna el contenido del archivo de contexto seleccionado por el asistente para poder generar respuestas al usuario",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "enum": titles,
                            "description": "Es el titluo del archivo del archivo que va a ser leido, siempre debe contener la extencion que se encontro con la funcion get_title_context_files()"},
                    },
                    "required": ["file_name"]
                }
            }
        }]

    def get_context_functions(self):
        return self.context_function

    @staticmethod
    def get_context_from(file_name: str) -> str:
        # Directory containing the context files
        context_files_dir = 'context_files'

        # Construct the full path to the file
        file_path = os.path.join(context_files_dir, file_name)

        # Obtener la extensión del archivo
        _, file_extension = os.path.splitext(file_path)

        # Leer archivos PDF
        if file_extension.lower() == '.pdf':
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in range(len(reader.pages)):
                        text += reader.pages[page].extract_text()
                    return text
            except Exception as e:
                return f"Error leyendo archivo PDF: {str(e)}"

        # Leer archivos DOC
        elif file_extension.lower() == '.doc':
            try:
                text = textract.process(file_path).decode('utf-8')
                return text
            except Exception as e:
                return f"Error leyendo archivo DOC: {str(e)}"

        # Extensión no soportada
        else:
            return "Error: Formato de archivo no soportado."