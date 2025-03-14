from pydantic import BaseModel
from typing import Dict, Optional


class FilesDictionary(BaseModel):
    """
    Value object which contains repository-relative paths of source code files
    mapped to their content.
    """
    files: Dict[str, str] = {}
    
    def add_file(self, path: str, content: str) -> None:
        """
        Adds a file to the dictionary.
        
        Args:
            path: The repository-relative path of the file.
            content: The content of the file.
        """
        assert path, "File path cannot be empty"
        self.files[path] = content
    
    def get_file_content(self, path: str) -> Optional[str]:
        """
        Gets the content of a file by its path.
        
        Args:
            path: The repository-relative path of the file.
            
        Returns:
            The content of the file if found, None otherwise.
        """
        return self.files.get(path)
    
    def remove_file(self, path: str) -> bool:
        """
        Removes a file from the dictionary.
        
        Args:
            path: The repository-relative path of the file.
            
        Returns:
            True if the file was removed, False if it wasn't in the dictionary.
        """
        if path in self.files:
            del self.files[path]
            return True
        return False
    
    def get_all_paths(self) -> list[str]:
        """
        Gets all file paths in the dictionary.
        
        Returns:
            A list of all file paths.
        """
        return list(self.files.keys())
    
    def merge(self, other: 'FilesDictionary') -> None:
        """
        Merges another FilesDictionary into this one.
        Files in the other dictionary will overwrite files in this one if they have the same path.
        
        Args:
            other: The FilesDictionary to merge into this one.
        """
        self.files.update(other.files)