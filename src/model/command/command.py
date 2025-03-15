from pydantic import BaseModel
from typing import ClassVar
import re
from src.model.command.command_id import CommandId


class Command(BaseModel):
    """
    Represents a specific type of interaction in the software system.
    Has a name and description that can be modified after creation.
    """
    id: CommandId
    name: str
    description: str

    # Class variable to track the last used number for auto-incrementing IDs
    _last_id_number: ClassVar[int] = 0
    _initialized: ClassVar[bool] = False

    @classmethod
    def initialize_last_id(cls, existing_commands):
        """
        Initialize the _last_id_number based on existing commands.
        This should be called when the repository is initialized.
        
        Args:
            existing_commands: List of existing Command objects
        """
        if cls._initialized:
            return
            
        max_id = 0
        for cmd in existing_commands:
            # Extract the number part from the ID
            match = re.match(r'CMD-(\d+)', cmd.id.value)
            if match:
                id_num = int(match.group(1))
                max_id = max(max_id, id_num)
        
        cls._last_id_number = max_id
        cls._initialized = True

    def __init__(self, **data):
        """
        Initialize a new Command.
        If no ID is provided, a new one will be generated.
        """
        if 'id' not in data:
            Command._last_id_number += 1
            data['id'] = CommandId(value=f"CMD-{Command._last_id_number}")
        
        super().__init__(**data)
    
    def update_name(self, new_name: str) -> None:
        """
        Updates the name of the command.
        
        Args:
            new_name: The new name for the command.
        """
        assert new_name, "Command name cannot be empty"
        self.name = new_name
    
    def update_description(self, new_description: str) -> None:
        """
        Updates the description of the command.
        
        Args:
            new_description: The new description for the command.
        """
        assert new_description, "Command description cannot be empty"
        self.description = new_description

    class Config:
        arbitrary_types_allowed = True
