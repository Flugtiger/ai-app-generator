import re
from typing import List, Tuple

from src.model.files.files_dictionary import FilesDictionary
from src.model.message.message import Message
from src.model.services.message_parser import MessageParser


class MessageParserImpl(MessageParser):
    """
    Implementation of MessageParser that parses file contents from LLM response Messages.
    """
    
    def __init__(self, start_token: str = "SOF```", end_token: str = "```EOF"):
        """
        Initialize the message parser with start and end tokens.
        """
        self.start_token = start_token
        self.end_token = end_token
    
    def get_file_format_pattern(self) -> str:
        """
        Returns a pattern for how to define files, including an example, for use in system prompts.
        """
        pattern = (
            f"You will output the content of each file necessary to achieve the goal, including ALL code.\n"
            f"Represent files like so:\n\n"
            f"FILENAME\n"
            f"{self.start_token}\n"
            f"CODE\n"
            f"{self.end_token}\n\n"
            f"The following tokens must be replaced like so:\n"
            f"FILENAME is the lowercase combined path and file name including the file extension\n"
            f"CODE is the code in the file\n\n"
            f"Example representation of a file:\n\n"
            f"src/hello_world.py\n"
            f"{self.start_token}\n"
            f"print(\"Hello World\")\n"
            f"{self.end_token}"
        )
        return pattern
    
    def _extract_files(self, content: str) -> List[Tuple[str, str]]:
        """
        Extract files from the content.
        """
        lines = content.split('\n')
        files = []
        
        i = 0
        while i < len(lines):
            # Check if the next line is a start token
            if i + 1 < len(lines) and lines[i + 1].strip() == self.start_token:
                filename = lines[i].strip()
                file_content = []
                start_token_count = 1
                
                # Skip the filename and start token
                i += 2
                
                # Collect content until matching end token
                while i < len(lines):
                    line = lines[i]
                    
                    if line.strip() == self.start_token:
                        start_token_count += 1
                        file_content.append(line)
                    elif line.strip() == self.end_token:
                        start_token_count -= 1
                        if start_token_count == 0:
                            break
                        file_content.append(line)
                    else:
                        file_content.append(line)
                    
                    i += 1
                
                if start_token_count == 0:
                    files.append((filename, '\n'.join(file_content)))
                else:
                    raise ValueError(f"Unmatched start token for file: {filename}")
            
            i += 1
        
        return files
    
    def parse_files_from_message(self, message: Message) -> FilesDictionary:
        """
        Parses a LLM response message and returns a FilesDictionary with the parsed files.
        """
        files_dict = FilesDictionary()
        
        try:
            extracted_files = self._extract_files(message.content)
            
            for filename, content in extracted_files:
                files_dict.add_file(filename, content)
            
            return files_dict
        except Exception as e:
            raise ValueError(f"Failed to parse message: {str(e)}")