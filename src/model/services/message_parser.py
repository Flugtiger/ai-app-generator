from typing import Dict, List
from src.model.value_objects.files_dictionary import FilesDictionary
from src.model.value_objects.message import Message
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
    def parse_files_from_message(message: Message) -> FilesDictionary:
        """
        Parses file contents from a LLM response message.
        Handles nested code blocks by counting SOF and EOF markers.
        
        Args:
            message: The LLM response message.
            
        Returns:
            A FilesDictionary containing the parsed files.
        """
        assert message and message.content, "Invalid message format"
        content = message.content
        
        files_dict = FilesDictionary()
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for a filename line followed by SOF marker
            if i + 1 < len(lines) and 'SOF```' in lines[i + 1]:
                filename = line
                i += 2  # Skip the SOF marker
                
                # Collect content until matching EOF marker
                file_content = []
                sof_count = 1  # We've already seen one SOF
                
                while i < len(lines):
                    if 'SOF```' in lines[i]:
                        sof_count += 1
                    elif '```EOF' in lines[i]:
                        sof_count -= 1
                        if sof_count == 0:  # Found matching EOF
                            break
                    file_content.append(lines[i])
                    i += 1
                
                if sof_count == 0:  # Successfully found matching EOF
                    files_dict.add_file(filename, '\n'.join(file_content))
            
            i += 1
        
        return files_dict
    
    @staticmethod
    def parse_diffs_from_message(message: Message) -> Dict[str, str]:
        """
        Parses unified diffs from a LLM response message.
        Handles nested code blocks by counting SOF and EOF markers.
        
        Args:
            message: The LLM response message.
            
        Returns:
            A dictionary mapping filenames to their diff content.
        """
        assert message and message.content, "Invalid message format"
        content = message.content
        
        diffs = {}
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for a filename line followed by SOF marker
            if i + 1 < len(lines) and 'SOF```' in lines[i + 1]:
                filename = line
                i += 2  # Skip the SOF marker
                
                # Collect content until matching EOF marker
                diff_content = []
                sof_count = 1  # We've already seen one SOF
                
                while i < len(lines):
                    if 'SOF```' in lines[i]:
                        sof_count += 1
                    elif '```EOF' in lines[i]:
                        sof_count -= 1
                        if sof_count == 0:  # Found matching EOF
                            break
                    diff_content.append(lines[i])
                    i += 1
                
                if sof_count == 0:  # Successfully found matching EOF
                    diffs[filename] = '\n'.join(diff_content)
            
            i += 1
        
        return diffs
