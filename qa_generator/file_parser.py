"""
This module provides classes for file parsing and document representation.
"""

from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.schema import Document

# UnstructuredReader = download_loader("UnstructuredReader")


class File:
    """
    This class defines the interface for parsing files and representing documents.
    """

    def __init__(self, file_path: str):
        """
        Initialize the File object.

        Args:
            file_path (str): The path of the file to parse.
        """
        self.file_path = file_path
        self.documents: list[Document] = self._parse_file()

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
