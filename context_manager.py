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
        context_function (list): A list that defines a function for getting context from a file.
                                 This function is described in a structured format suitable for APIs or function calls.
    """

    def __init__(self):
        """
        Initializes the ContextManager class by scanning the specified directory for context files.
        It collects the file names (with extensions) as titles and stores them in a list for later use.

        Directory: 'context_files'
        """
        # Directory containing the context files
        context_files_dir = 'context_files'

        # List to store the titles (file names with extension)
        titles = []

        # Iterate over each file in the directory
        for filename in os.listdir(context_files_dir):
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(os.path.join(context_files_dir, filename)):
                # Append the filename (including extension) to the titles list
                titles.append(f"{filename}")

        # Store a function structure for getting context from a file
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
        """
        Returns the defined context functions.

        Returns:
            list: A list containing the function definitions for retrieving context from files.
        """
        return self.context_function

    @staticmethod
    def get_context_from(file_name: str) -> str:
        """
        Reads and returns the content of the specified file. Supports both PDF and DOC formats.

        Args:
            file_name (str): The name of the file to read, including its extension.

        Returns:
            str: The content of the file as a string. If the file type is unsupported or an error occurs, an error message is returned.
        """
        # Directory containing the context files
        context_files_dir = 'context_files'

        # Construct the full path to the file
        file_path = os.path.join(context_files_dir, file_name)

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