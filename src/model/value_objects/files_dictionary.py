import re
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

    def copy(self) -> 'FilesDictionary':
        """
        Creates a deep copy of this FilesDictionary.

        Returns:
            A new FilesDictionary with the same files.
        """
        new_dict = FilesDictionary()
        for path, content in self.files.items():
            new_dict.add_file(path, content)
        return new_dict

    def apply_diff(self, diff_content: str) -> None:
        """
        Applies a unified diff to the domain model.

        Args:
            diff_content: The unified diff content to apply.
        """
        assert diff_content, "Diff content cannot be empty"

        # Extract the filename from the diff
        filename_match = re.search(r'^File: (.+)$', diff_content, re.MULTILINE)
        if not filename_match:
            raise ValueError("Could not find filename in diff content")

        filename = filename_match.group(1).strip()

        # Get the current content of the file, or empty string if it doesn't exist
        current_content = self.get_file_content(filename) or ""

        # Extract the changes from the diff
        changes_match = re.search(r'```diff\n([\s\S]+?)\n```', diff_content)
        if not changes_match:
            raise ValueError("Could not find diff changes in content")

        diff_lines = changes_match.group(1).split('\n')

        # Process the diff lines
        new_content = self._apply_diff_lines(current_content, diff_lines)

        # Update or add the file
        self.add_file(filename, new_content)

    def _apply_diff_lines(self, current_content: str, diff_lines: list[str]) -> str:
        """
        Applies diff lines to the current content.

        Args:
            current_content: The current content of the file.
            diff_lines: The diff lines to apply.

        Returns:
            The new content after applying the diff.
        """
        current_lines = current_content.split('\n')
        result_lines = []

        i = 0
        while i < len(diff_lines):
            line = diff_lines[i]

            # Skip diff header lines
            if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
                i += 1
                continue

            # Handle added lines
            if line.startswith('+') and not line.startswith('+++'):
                result_lines.append(line[1:])  # Remove the '+' prefix

            # Handle removed lines - skip them
            elif line.startswith('-') and not line.startswith('---'):
                pass  # Skip removed lines

            # Handle context lines
            else:
                result_lines.append(line)

            i += 1

        return '\n'.join(result_lines)
