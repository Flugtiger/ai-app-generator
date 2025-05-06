import os
import unittest
from pathlib import Path

from src.model.files.files_dictionary import FilesDictionary
from src.model.message.message import Message, MessageRole
from src.infrastructure.services.message_parser_impl import MessageParserImpl


class TestMessageParserImpl(unittest.TestCase):
    """Test cases for the MessageParserImpl class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = MessageParserImpl()
        
        # Get the path to the test message file
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        message_path = current_dir / "message.txt"
        
        # Read the test message content
        with open(message_path, "r", encoding="utf-8") as f:
            self.message_content = f.read()
        
        self.test_message = Message(
            role=MessageRole.ASSISTANT,
            content=self.message_content
        )

    def test_apply_edits_from_message(self):
        """Test applying edits from a message with search/replace blocks."""
        # Create an empty files dictionary
        files_dict = FilesDictionary()
        
        # Apply edits from the message
        updated_files = self.parser.apply_edits_from_message(self.test_message, files_dict)
        
        # Check that the expected files were created
        self.assertIn("src/model/requirement/requirement_id.py", updated_files.get_all_files())
        self.assertIn("src/model/requirement/requirement.py", updated_files.get_all_files())
        self.assertIn("src/model/requirement/requirement_repository.py", updated_files.get_all_files())
        self.assertIn("src/model/requirement/__init__.py", updated_files.get_all_files())
        
        # Check the content of one of the files
        requirement_id_content = updated_files.get_file("src/model/requirement/requirement_id.py")
        self.assertIn("class RequirementId(BaseModel):", requirement_id_content)
        self.assertIn("value: str | None = None", requirement_id_content)
        
        # Check the content of another file
        requirement_content = updated_files.get_file("src/model/requirement/requirement.py")
        self.assertIn("class Requirement(BaseModel):", requirement_content)
        self.assertIn("requirement_text: str", requirement_content)
