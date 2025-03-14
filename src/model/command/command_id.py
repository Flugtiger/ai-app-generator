from pydantic import BaseModel
import uuid


class CommandId(BaseModel):
    """
    Value object representing the ID of a Command.
    """
    value: str

    def __init__(self, value: str):
        """
        Initialize a new CommandId.
        Validates that the value is a valid UUID string.
        """
        # Validate that the value is a valid UUID
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(f"CommandId must be a valid UUID, got {value}")
        
        super().__init__(value=value)
    
    def __str__(self):
        return self.value