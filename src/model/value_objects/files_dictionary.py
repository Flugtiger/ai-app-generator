from typing import Dict, Optional
from pydantic import BaseModel


class FilesDictionary(BaseModel):
    """
    Value object representing a dictionary of files.
    Maps repository-relative file paths to their content.
    """
    files: Dict[str, str] = {}

    def add_file(self, path: str, content: str) -> None:
        """
        Adds a file to the dictionary.
        """
        assert path, "File path cannot be empty"
        self.files[path] = content

    def get_file(self, path: str) -> Optional[str]:
        """
        Gets the content of a file from the dictionary.
        Returns None if the file does not exist.
        """
        return self.files.get(path)

    def remove_file(self, path: str) -> None:
        """
        Removes a file from the dictionary.
        """
        if path in self.files:
            del self.files[path]

    def get_paths(self) -> list[str]:
        """
        Returns a list of all file paths in the dictionary.
        """
        return list(self.files.keys())

    def __len__(self) -> int:
        """
        Returns the number of files in the dictionary.
        """
        return len(self.files)