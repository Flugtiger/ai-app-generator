from pydantic import field_validator

from src.model.files.files_dictionary import FilesDictionary


class DomainModelFiles(FilesDictionary):
    """
    A special type of FilesDictionary that constraints all contained files
    to have a path prefixed by 'src/model'.
    """
    
    @field_validator('files')
    @classmethod
    def validate_file_paths(cls, files):
        """
        Validates that all file paths start with 'src/model'.
        """
        for path in files.keys():
            assert path.startswith('src/model'), f"File path '{path}' must start with 'src/model'"
        return files
    
    def add_file(self, path: str, content: str) -> None:
        """
        Adds a file to the dictionary, ensuring the path starts with 'src/model'.
        """
        assert path.startswith('src/model'), f"File path '{path}' must start with 'src/model'"
        super().add_file(path, content)