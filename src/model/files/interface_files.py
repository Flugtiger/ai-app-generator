from pydantic import field_validator

from src.model.files.files_dictionary import FilesDictionary


class InterfaceFiles(FilesDictionary):
    """
    A specific FilesDictionary that makes sure that all files have a path
    that starts with 'src/interface'.
    """
    
    @field_validator('files')
    @classmethod
    def validate_file_paths(cls, files):
        """
        Validates that all file paths start with 'src/interface'.
        """
        for path in files.keys():
            assert path.startswith('src/interface'), f"File path '{path}' must start with 'src/interface'"
        return files
    
    def add_file(self, path: str, content: str) -> None:
        """
        Adds a file to the dictionary, ensuring the path starts with 'src/interface'.
        """
        assert path.startswith('src/interface'), f"File path '{path}' must start with 'src/interface'"
        super().add_file(path, content)