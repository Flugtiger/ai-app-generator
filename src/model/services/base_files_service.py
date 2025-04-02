import os
from abc import ABC, abstractmethod
from typing import Type

from src.model.files.files_dictionary import FilesDictionary


class BaseFilesService(ABC):
    """
    Base service for reading and writing files from/to a specific subfolder.
    """

    def __init__(self, subfolder: str, files_dictionary_class: Type[FilesDictionary]):
        """
        Initializes the service with a subfolder and a FilesDictionary subclass.
        """
        self.subfolder = subfolder
        self.files_dictionary_class = files_dictionary_class

    def read_files(self, project_root_path: str) -> FilesDictionary:
        """
        Reads all files inside the subfolder into the FilesDictionary subclass
        but with paths relative to the project root path.
        """
        files_dict = self.files_dictionary_class()
        subfolder_path = os.path.join(project_root_path, self.subfolder)

        if not os.path.exists(subfolder_path):
            return files_dict

        for root, _, files in os.walk(subfolder_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Convert to repository-relative path
                relative_path = os.path.relpath(file_path, project_root_path).replace('\\', '/')
                files_dict.add_file(relative_path, content)

        return files_dict

    def write_files(self, project_root_path: str, files_dict: FilesDictionary) -> None:
        """
        Writes the files from the FilesDictionary to the subfolder.
        """
        for path, content in files_dict.get_all_files().items():
            full_path = os.path.join(project_root_path, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
