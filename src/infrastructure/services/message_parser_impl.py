import re
from typing import Dict, List, Tuple

from src.model.files.files_dictionary import FilesDictionary
from src.model.message.message import Message
from src.model.model_requirement.model_requirement_id import ModelRequirementId
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
            f"FILENAME [IMPLEMENTS: REQ_ID1, REQ_ID2, ...]\n"
            f"{self.start_token}\n"
            f"CODE\n"
            f"{self.end_token}\n\n"
            f"The following tokens must be replaced like so:\n"
            f"FILENAME is the lowercase combined path and file name including the file extension\n"
            f"REQ_ID1, REQ_ID2, ... are the IDs of the requirements implemented in this file\n"
            f"CODE is the code in the file\n\n"
            f"Example representation of a file:\n\n"
            f"src/hello_world.py [IMPLEMENTS: REQ001, REQ002]\n"
            f"{self.start_token}\n"
            f"print(\"Hello World\")\n"
            f"{self.end_token}"
        )
        return pattern

    def get_edit_format_pattern(self) -> str:
        """
        Returns a pattern for how to define file edits, including an example, for use in system prompts.
        """
        pattern = (
            f"To edit existing files or create new ones, use the SEARCH/REPLACE format:\n\n"
            f"FILEPATH\n"
            f"```LANGUAGE\n"
            f"<<<<<<< SEARCH\n"
            f"EXISTING_CODE_TO_REPLACE\n"
            f"=======\n"
            f"NEW_CODE\n"
            f">>>>>>> REPLACE\n"
            f"```\n\n"
            f"The following tokens must be replaced like so:\n"
            f"- FILEPATH is the full path to the file\n"
            f"- LANGUAGE is the programming language (e.g., python, java, etc.)\n"
            f"- EXISTING_CODE_TO_REPLACE is the exact code to be replaced (leave empty for new files)\n"
            f"- NEW_CODE is the code that will replace the search block\n\n"
            f"Example for editing an existing file:\n\n"
            f"src/example.py\n"
            f"```python\n"
            f"<<<<<<< SEARCH\n"
            f"def hello():\n"
            f"    print(\"Hello\")\n"
            f"=======\n"
            f"def hello():\n"
            f"    print(\"Hello, World!\")\n"
            f">>>>>>> REPLACE\n"
            f"```\n\n"
            f"Example for creating a new file:\n\n"
            f"src/new_file.py\n"
            f"```python\n"
            f"<<<<<<< SEARCH\n"
            f"=======\n"
            f"def new_function():\n"
            f"    print(\"This is a new file\")\n"
            f">>>>>>> REPLACE\n"
            f"```"
        )
        return pattern

    def _extract_files(self, content: str) -> List[Tuple[str, List[str], str]]:
        """
        Extract files from the content.
        Returns a list of tuples (filename, requirement_ids, content).
        """
        lines = content.split('\n')
        files = []

        i = 0
        while i < len(lines):
            # Check if the next line is a start token
            if i + 1 < len(lines) and lines[i + 1].strip() == self.start_token:
                file_line = lines[i].strip()
                
                # Extract filename and requirement IDs
                filename = file_line
                requirement_ids = []
                
                # Check if the line contains requirement IDs
                implements_match = re.search(r'\[IMPLEMENTS:\s*(.*?)\]', file_line)
                if implements_match:
                    # Extract the filename without the [IMPLEMENTS: ...] part
                    filename = file_line[:file_line.find('[')].strip()
                    
                    # Extract the requirement IDs
                    req_ids_str = implements_match.group(1)
                    requirement_ids = [req_id.strip() for req_id in req_ids_str.split(',') if req_id.strip()]
                
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
                    files.append((filename, requirement_ids, '\n'.join(file_content)))
                else:
                    raise ValueError(f"Unmatched start token for file: {filename}")

            i += 1

        return files

    def _extract_search_replace_blocks(self, content: str) -> List[Tuple[str, str, str]]:
        """
        Extract search/replace blocks from the content.
        Returns a list of tuples (filepath, search_block, replace_block).
        """
        pattern = r'([^\n]+)\n```[^\n]*\n<<<<<<< SEARCH\n(.*?)=======\n(.*?)>>>>>>> REPLACE\n```'
        matches = re.findall(pattern, content, re.DOTALL)

        result = []
        for filepath, search_block, replace_block in matches:
            result.append((filepath.strip(), search_block.strip(), replace_block.strip()))

        return result

    def parse_files_from_message(self, message: Message) -> Tuple[FilesDictionary, Dict[str, List[str]]]:
        """
        Parses a LLM response message and returns a tuple containing:
        1. A FilesDictionary with the parsed files
        2. A dictionary mapping requirement IDs to lists of file paths that implement them
        """
        files_dict = FilesDictionary()
        requirement_to_files: Dict[str, List[str]] = {}

        try:
            extracted_files = self._extract_files(message.content)

            for filename, requirement_ids, content in extracted_files:
                files_dict.add_file(filename, content)
                
                # Map each requirement ID to this file
                for req_id in requirement_ids:
                    if req_id not in requirement_to_files:
                        requirement_to_files[req_id] = []
                    requirement_to_files[req_id].append(filename)

            return files_dict, requirement_to_files
        except Exception as e:
            raise ValueError(f"Failed to parse message: {str(e)}")

    def _extract_requirement_ids_from_message(self, message: Message) -> Dict[str, List[str]]:
        """
        Extract requirement IDs from the message content.
        Returns a dictionary mapping requirement IDs to lists of file paths.
        """
        requirement_to_files: Dict[str, List[str]] = {}
        
        # Look for patterns like "File X implements requirements REQ001, REQ002"
        pattern = r'(?:file|File)\s+([^\s]+)\s+implements\s+requirements?\s+((?:[A-Za-z0-9]+(?:,\s*)?)+)'
        matches = re.findall(pattern, message.content, re.IGNORECASE)
        
        for filepath, req_ids_str in matches:
            req_ids = [req_id.strip() for req_id in req_ids_str.split(',')]
            for req_id in req_ids:
                if req_id not in requirement_to_files:
                    requirement_to_files[req_id] = []
                requirement_to_files[req_id].append(filepath)
        
        return requirement_to_files

    def apply_edits_from_message(self, message: Message, files_dict: FilesDictionary) -> Tuple[FilesDictionary, Dict[str, List[str]]]:
        """
        Parses a LLM response message for file edits and applies them to the provided FilesDictionary.
        Returns a tuple containing:
        1. The updated FilesDictionary
        2. A dictionary mapping requirement IDs to lists of file paths that implement them
        """
        try:
            # Create a new files dictionary to avoid modifying the original
            updated_files_dict = FilesDictionary()
            
            # Copy all existing files to the new dictionary
            for path, content in files_dict.get_all_files().items():
                updated_files_dict.add_file(path, content)

            # Extract search/replace blocks
            edits = self._extract_search_replace_blocks(message.content)

            # Track modified files
            modified_files = set()

            for filepath, search_block, replace_block in edits:
                # For new files (empty search block)
                if not search_block.strip():
                    updated_files_dict.add_file(filepath, replace_block + "\n")
                    modified_files.add(filepath)
                    continue

                # For existing files
                existing_content = updated_files_dict.get_file(filepath)

                # If file doesn't exist in the dictionary but has a search block, raise an error
                if existing_content is None:
                    raise ValueError(f"Cannot edit non-existent file: {filepath}")

                # Replace the search block with the replace block
                if search_block in existing_content:
                    # this should keep the trailing newline in place:
                    new_content = existing_content.replace(search_block, replace_block)
                    updated_files_dict.add_file(filepath, new_content)
                    modified_files.add(filepath)
                else:
                    raise ValueError(f"Search block not found in file: {filepath}")

            # Extract requirement IDs from the message
            requirement_to_files = self._extract_requirement_ids_from_message(message)
            
            return updated_files_dict, requirement_to_files
        except Exception as e:
            raise ValueError(f"Failed to apply edits from message: {str(e)}")
