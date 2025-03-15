from pydantic import BaseModel, validator


class CommandId(BaseModel):
    """
    Value object representing the ID of a Command.
    Format: 'CMD-' followed by a number.
    """
    value: str

    @validator('value')
    def validate_format(cls, v):
        """
        Validates that the ID follows the required format: 'CMD-' followed by a number.
        """
        if not v.startswith('CMD-'):
            raise ValueError(f"CommandId must start with 'CMD-', got {v}")
        
        # Check that the part after 'CMD-' is a number
        number_part = v[4:]
        if not number_part.isdigit():
            raise ValueError(f"CommandId must be in format 'CMD-<number>', got {v}")
        
        return v

    def __str__(self):
        return self.value
