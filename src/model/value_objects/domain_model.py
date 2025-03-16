import re
from src.model.value_objects.files_dictionary import FilesDictionary


class DomainModel(FilesDictionary):
    """
    A specialized FilesDictionary that represents a domain model's source code.
    """
    
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
    
    def validate(self) -> bool:
        """
        Validates that the domain model is well-formed.
        
        Returns:
            True if the domain model is valid, False otherwise.
        """
        # This is a simplified implementation. In a real-world scenario,
        # you would perform more sophisticated validation.
        return len(self.files) > 0
