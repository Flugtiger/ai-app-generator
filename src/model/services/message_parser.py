from typing import Dict, List, Any
from src.model.value_objects.files_dictionary import FilesDictionary
import re


class MessageParser:
    """
    Domain service for parsing file contents and diffs from LLM responses.
    Provides templates for how a LLM should output files and diffs.
    """
    
    @staticmethod
    def get_file_template_with_example() -> str:
        """
        Returns the template for how a LLM should output files, along with an example.
        
        Returns:
            A string containing the template and example.
        """
        return """
You will output the content of each file necessary to achieve the goal, including ALL code.
Represent files like so:

FILENAME
SOF```
CODE
```EOF

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
CODE is the code in the file

Example representation of a file:

src/hello_world.py
SOF```
print("Hello World")
```EOF
"""
    
    @staticmethod
    def get_diff_template_with_example() -> str:
        """
        Returns the template for how a LLM should output diffs, along with an example.
        
        Returns:
            A string containing the template and example.
        """
        return """
You will output the changes needed as unified diffs.
Represent diffs like so:

FILENAME
SOF```
@@ -start_line,num_lines +start_line,num_lines @@
 unchanged line
-removed line
+added line
 unchanged line
```EOF

Example representation of a diff:

src/hello_world.py
SOF```
@@ -1,1 +1,2 @@
 print("Hello World")
+print("Goodbye World")
```EOF
"""
    
    @staticmethod
    def parse_files_from_message(message: Dict[str, Any]) -> FilesDictionary:
        """
        Parses file contents from a LLM response message.
        
        Args:
            message: The LLM response message.
            
        Returns:
            A FilesDictionary containing the parsed files.
        """
        assert message and 'content' in message, "Invalid message format"
        content = message['content']
        
        files_dict = FilesDictionary()
        
        # Regular expression to match file blocks
        pattern = r'([^\n]+)\nSOF```\n(.*?)\n```EOF'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            filename = match.group(1).strip()
            file_content = match.group(2)
            files_dict.add_file(filename, file_content)
        
        return files_dict
    
    @staticmethod
    def parse_diffs_from_message(message: Dict[str, Any]) -> Dict[str, str]:
        """
        Parses unified diffs from a LLM response message.
        
        Args:
            message: The LLM response message.
            
        Returns:
            A dictionary mapping filenames to their diff content.
        """
        assert message and 'content' in message, "Invalid message format"
        content = message['content']
        
        diffs = {}
        
        # Regular expression to match diff blocks
        pattern = r'([^\n]+)\nSOF```\n(.*?)\n```EOF'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            filename = match.group(1).strip()
            diff_content = match.group(2)
            diffs[filename] = diff_content
        
        return diffs