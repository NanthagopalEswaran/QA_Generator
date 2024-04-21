"""
This module provides classes for file parsing and document representation.
"""

import os

from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.schema import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile

# UnstructuredReader = download_loader("UnstructuredReader")


def save_to_temp_file(file_obj: UploadedFile):
    """
    Save the contents of an uploaded file to a temporary file.

    Args:
        file_obj (UploadedFile): The uploaded file object.

    Returns:
        str: The path of the temporary file where the contents are saved.
    """
    file_path = os.path.join(os.environ["DATA_DIR"], f"{file_obj.file_id}.{file_obj.name}")
    with open(file_path, "wb") as temp_file:
        content = file_obj.read()
        temp_file.write(content)
        print(f"file saved to {file_path}")
    return file_path


class File:
    """
    This class defines the interface for parsing files and representing documents.
    """

    def __init__(self, file: UploadedFile):
        self.file_path = save_to_temp_file(file)
        self.documents: list[Document] = self._parse_file()

    def __del__(self):
        """
        Delete the temporary file.
        """

        os.remove(self.file_path)

    def _parse_file(self):
        """
        Load the documents from the file.
        """

        return SimpleDirectoryReader(
            input_files=[self.file_path],
            # file_extractor={
            #     ".pdf": UnstructuredReader(),
            #     ".docx": UnstructuredReader(),
            #     ".md": UnstructuredReader(),
            #     ".txt": UnstructuredReader(),
            #     ".rst": UnstructuredReader(),
            # },
        ).load_data()
