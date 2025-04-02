from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional


class FilesDictionary(BaseModel):
    """
    Value object which contains the repository-relative paths of source code files
    mapped to their content.
    """
    files: Dict[str, str] = Field(default_factory=dict)
    
    def add_file(self, path: str, content: str) -> None:
        """
        Adds a file to the dictionary.
        """
        self.files[path] = content
    
    def get_file(self, path: str) -> Optional[str]:
        """
        Gets a file from the dictionary.
        """
        return self.files.get(path)
    
    def get_all_files(self) -> Dict[str, str]:
        """
        Gets all files from the dictionary.
        """
        return self.files