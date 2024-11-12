import textract
import PyPDF2
import os


class ContextManager:
    """
    ContextManager class is responsible for handling context files within a directory.
    It reads and extracts text from supported file types (PDF and DOC) and provides a function
    that returns a list of available context file names. It also defines a function to retrieve
    the content of a selected file based on its name.

    Attributes:
        context_functions (list): A list that defines a function for getting context from a file.
                                 This function is described in a structured format suitable for APIs or function calls.
    """

    def __init__(self):
        """
        Initializes the ContextManager class by scanning the specified directory for context files.
        It collects the file names (with extensions) as titles and stores them in a list for later use.

        Directory: 'context_files'
        """
        # Directory containing the context files
        conac_files_dir = 'context_files/conac'
        conac_files = []
        for filename in os.listdir(conac_files_dir):
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(os.path.join(conac_files_dir, filename)):
                # Append the filename (including extension) to the titles list
                conac_files.append(f"{filename}")

        forms_files_dir = 'context_files/forms'
        forms_files = []
        for filename in os.listdir(forms_files_dir):
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(os.path.join(forms_files_dir, filename)):
                # Append the filename (including extension) to the titles list
                forms_files.append(f"{filename}")

        presupuesto_files_dir = 'context_files/presupuesto'
        presupuesto_files = []
        for filename in os.listdir(presupuesto_files_dir):
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(os.path.join(presupuesto_files_dir, filename)):
                # Append the filename (including extension) to the titles list
                presupuesto_files.append(f"{filename}")


        # Store a function structure for getting context from a file
        self.context_functions = [{
            "type": "function",
            "function": {
                "name": "get_context_from_conac_files",
                "description": "Retorna el contenido del archivo de contexto del CONAC seleccionado por el asistente para poder generar respuestas al usuario",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "enum": conac_files,
                            "description": "Es el titluo del archivo del archivo que va a ser leido, siempre debe contener la extencion que se encontro con la funcion get_title_context_files()"},
                    },
                    "required": ["file_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_context_from_form_files",
                "description": "Retorna el contenido del archivo de especificaciones del formulario seleccionado por el asistente en base a la peticion del usuario para poder generar respuestas",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "enum": forms_files,
                            "description": "Es el titluo del archivo del archivo que va a ser leido, siempre debe contener la extencion que se encontro con la funcion get_title_context_files()"},
                    },
                    "required": ["file_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_context_from_presupuesto_files",
                "description": "Retorna el contenido del archivo del presupuesto del estado que fue seleccionado por el asistente en base a la peticion del usuario para poder generar respuestas",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "enum": presupuesto_files,
                            "description": "Es el titluo del archivo del archivo que va a ser leido, siempre debe contener la extencion que se encontro con la funcion get_title_context_files()"},
                    },
                    "required": ["file_name"]
                }
            }
        }]

    def get_context_functions(self):
        """
        Returns the defined context functions.

        Returns:
            list: A list containing the function definitions for retrieving context from files.
        """
        return self.context_functions

    @staticmethod
    def get_context_from_conac_files(file_name: str) -> str:
        """
        Reads and returns the content of the specified file. Supports both PDF and DOC formats.

        Args:
            file_name (str): The name of the file to read, including its extension.

        Returns:
            str: The content of the file as a string. If the file type is unsupported or an error occurs, an error message is returned.
        """
        # Directory containing the context files
        files_dir = 'context_files/conac'

        # Construct the full path to the file
        file_path = os.path.join(files_dir, file_name)

        # Get the file extension
        _, file_extension = os.path.splitext(file_path)

        # Read PDF files
        if file_extension.lower() == '.pdf':
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in range(len(reader.pages)):
                        text += reader.pages[page].extract_text()
                    return text
            except Exception as e:
                return f"Error reading PDF file: {str(e)}"

        # Read DOC files
        elif file_extension.lower() == '.doc':
            try:
                text = textract.process(file_path).decode('utf-8')
                return text
            except Exception as e:
                return f"Error reading DOC file: {str(e)}"

        # Unsupported file format
        else:
            return "Error: Unsupported file format."

    @staticmethod
    def get_context_from_form_files(file_name: str) -> str:
        """
        Reads and returns the content of the specified file. Supports both PDF and DOC formats.

        Args:
            file_name (str): The name of the file to read, including its extension.

        Returns:
            str: The content of the file as a string. If the file type is unsupported or an error occurs, an error message is returned.
        """
        # Directory containing the context files
        files_dir = 'context_files/forms'

        # Construct the full path to the file
        file_path = os.path.join(files_dir, file_name)

        # Get the file extension
        _, file_extension = os.path.splitext(file_path)

        # Read PDF files
        if file_extension.lower() == '.pdf':
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in range(len(reader.pages)):
                        text += reader.pages[page].extract_text()
                    return text
            except Exception as e:
                return f"Error reading PDF file: {str(e)}"

        # Read DOC files
        elif file_extension.lower() == '.doc':
            try:
                text = textract.process(file_path).decode('utf-8')
                return text
            except Exception as e:
                return f"Error reading DOC file: {str(e)}"

        # Unsupported file format
        else:
            return "Error: Unsupported file format."

    @staticmethod
    def get_context_from_presupuesto_files(file_name: str) -> str:
        """
        Reads and returns the content of the specified file. Supports both PDF and DOC formats.

        Args:
            file_name (str): The name of the file to read, including its extension.

        Returns:
            str: The content of the file as a string. If the file type is unsupported or an error occurs, an error message is returned.
        """
        # Directory containing the context files
        files_dir = 'context_files/presupuesto'

        # Construct the full path to the file
        file_path = os.path.join(files_dir, file_name)

        # Get the file extension
        _, file_extension = os.path.splitext(file_path)

        # Read PDF files
        if file_extension.lower() == '.pdf':
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in range(len(reader.pages)):
                        text += reader.pages[page].extract_text()
                    return text
            except Exception as e:
                return f"Error reading PDF file: {str(e)}"

        # Read DOC files
        elif file_extension.lower() == '.doc':
            try:
                text = textract.process(file_path).decode('utf-8')
                return text
            except Exception as e:
                return f"Error reading DOC file: {str(e)}"

        # Unsupported file format
        else:
            return "Error: Unsupported file format."