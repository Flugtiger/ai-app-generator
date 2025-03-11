import re
from typing import Dict, List, Optional

from src.model.value_objects.files_dictionary import FilesDictionary
from src.model.value_objects.message import Message


class MessageParser:
    """
    Domain service for parsing file contents and diffs from LLM responses.
    """
    
    @staticmethod
    def get_file_template() -> str:
        """
        Returns the template for how an LLM should output files.
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
    def get_diff_template() -> str:
        """
        Returns the template for how an LLM should output diffs.
        """
        return """
You will output unified diffs for each file that needs to be modified.
Represent diffs like so:

FILENAME
SOF```
@@ -line_number,number_of_lines +line_number,number_of_lines @@
 unchanged line
-removed line
+added line
 unchanged line
```EOF

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension

Example representation of a diff:

src/hello_world.py
SOF```
@@ -1,1 +1,1 @@
-print("Hello World")
+print("Hello, World!")
```EOF
"""

    @staticmethod
    def parse_files(response: Message) -> FilesDictionary:
        """
        Parses file contents from an LLM response message.
        
        Args:
            response: LLM response message
            
        Returns:
            FilesDictionary with the parsed files
        """
        files_dict = FilesDictionary()
        
        # Regular expression to match file blocks
        pattern = r'([^\n]+)\nSOF```\n(.*?)\n```EOF'
        matches = re.finditer(pattern, response.content, re.DOTALL)
        
        for match in matches:
            filename = match.group(1).strip()
            content = match.group(2)
            files_dict.add_file(filename, content)
        
        return files_dict

    @staticmethod
    def parse_diffs(response: Message) -> Dict[str, str]:
        """
        Parses unified diffs from an LLM response message.
        
        Args:
            response: LLM response message
            
        Returns:
            Dictionary mapping filenames to diff content
        """
        diffs = {}
        
        # Regular expression to match diff blocks
        pattern = r'([^\n]+)\nSOF```\n(.*?)\n```EOF'
        matches = re.finditer(pattern, response.content, re.DOTALL)
        
        for match in matches:
            filename = match.group(1).strip()
            diff_content = match.group(2)
            diffs[filename] = diff_content
        
        return diffs