from src.model.value_objects.files_dictionary import FilesDictionary


class ApplicationServices(FilesDictionary):
    """
    A specialized FilesDictionary that represents application services code.
    All files in ApplicationServices must be inside the 'src/application' directory.
    """
    
    def add_file(self, path: str, content: str) -> None:
        """
        Add a file to the application services, ensuring it's inside the 'src/application' directory.
        
        Args:
            path: The path of the file relative to the project root.
            content: The content of the file.
            
        Raises:
            ValueError: If the path is not inside the 'src/application' directory.
        """
        if not path.startswith('src/application/'):
            raise ValueError(f"Application services files must be inside 'src/application' directory, got: {path}")
        
        super().add_file(path, content)
    
    def merge(self, other: 'FilesDictionary') -> None:
        """
        Merges another FilesDictionary into this one, ensuring all files are inside 'src/application'.
        Files in the other dictionary will overwrite files in this one if they have the same path.
        
        Args:
            other: The FilesDictionary to merge into this one.
            
        Raises:
            ValueError: If any file in the other dictionary is not inside 'src/application'.
        """
        # Check that all files in the other dictionary are inside 'src/application'
        for path in other.files.keys():
            if not path.startswith('src/application/'):
                raise ValueError(f"Cannot merge file outside 'src/application' directory: {path}")
        
        # Merge the files
        super().merge(other)
