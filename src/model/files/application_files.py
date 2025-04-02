from pydantic import field_validator

from src.model.files.files_dictionary import FilesDictionary


class ApplicationFiles(FilesDictionary):
    """
    A specific FilesDictionary that makes sure that all files have a path
    that starts with 'src/application'.
    """
    
    @field_validator('files')
    @classmethod
    def validate_file_paths(cls, files):
        """
        Validates that all file paths start with 'src/application'.
        """
        for path in files.keys():
            assert path.startswith('src/application'), f"File path '{path}' must start with 'src/application'"
        return files
    
    def add_file(self, path: str, content: str) -> None:
        """
        Adds a file to the dictionary, ensuring the path starts with 'src/application'.
        """
        assert path.startswith('src/application'), f"File path '{path}' must start with 'src/application'"
        super().add_file(path, content)