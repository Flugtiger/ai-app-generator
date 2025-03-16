import os
from pathlib import Path
from typing import List, Optional

from src.model.value_objects.files_dictionary import FilesDictionary


class FilesDictionaryService:
    """
    Service for reading and writing FilesDictionary objects from/to a file system.
    """
    
    @staticmethod
    def read_from_directory(root_dir: str, ignore_patterns: Optional[List[str]] = None) -> FilesDictionary:
        """
        Reads all files from a directory into a FilesDictionary.
        
        Args:
            root_dir: The root directory to read files from.
            ignore_patterns: Optional list of patterns to ignore (e.g., '*.pyc', '__pycache__').
            
        Returns:
            A FilesDictionary containing all files from the directory.
        """
        if ignore_patterns is None:
            ignore_patterns = ['__pycache__', '*.pyc', '.git', '.vscode', '.idea']
            
        files_dict = FilesDictionary()
        root_path = Path(root_dir)
        
        if not root_path.exists() or not root_path.is_dir():
            raise ValueError(f"Directory does not exist or is not a directory: {root_dir}")
        
        for current_path, dirs, files in os.walk(root_path):
            # Skip directories that match ignore patterns
            dirs_to_remove = []
            for i, dir_name in enumerate(dirs):
                if any(Path(dir_name).match(pattern) for pattern in ignore_patterns):
                    dirs_to_remove.append(i)
            
            # Remove directories from bottom to top to avoid index issues
            for i in sorted(dirs_to_remove, reverse=True):
                del dirs[i]
            
            # Process files
            for file_name in files:
                file_path = Path(current_path) / file_name
                
                # Skip files that match ignore patterns
                if any(file_path.match(pattern) for pattern in ignore_patterns):
                    continue
                
                # Get relative path from root directory
                relative_path = file_path.relative_to(root_path)
                
                # Convert to forward slashes for consistency across platforms
                relative_path_str = str(relative_path).replace('\\', '/')
                
                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add to FilesDictionary
                    files_dict.add_file(relative_path_str, content)
                except UnicodeDecodeError:
                    # Skip binary files
                    continue
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
        
        return files_dict
    
    @staticmethod
    def write_to_directory(files_dict: FilesDictionary, root_dir: str, create_dirs: bool = True) -> None:
        """
        Writes a FilesDictionary to a directory, overwriting existing files.
        
        Args:
            files_dict: The FilesDictionary to write.
            root_dir: The root directory to write files to.
            create_dirs: Whether to create directories if they don't exist.
        """
        root_path = Path(root_dir)
        
        if not root_path.exists():
            if create_dirs:
                root_path.mkdir(parents=True)
            else:
                raise ValueError(f"Directory does not exist: {root_dir}")
        
        if not root_path.is_dir():
            raise ValueError(f"Path is not a directory: {root_dir}")
        
        # Write each file
        for file_path, content in files_dict.files.items():
            # Convert to OS-specific path
            os_path = file_path.replace('/', os.sep)
            full_path = root_path / os_path
            
            # Create parent directories if they don't exist
            if create_dirs:
                full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file content
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
