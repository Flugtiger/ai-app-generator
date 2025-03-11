import random
import string
from pydantic import BaseModel, validator


class BoundedContextId(BaseModel):
    """
    Value object representing the ID of a BoundedContext.
    The ID is a string with a maximum length of 4 characters.
    """
    value: str

    @validator('value')
    def validate_id(cls, v):
        """
        Validates that the ID is not empty and has a maximum length of 4 characters.
        """
        if not v:
            raise ValueError("BoundedContextId cannot be empty")
        if len(v) > 4:
            raise ValueError("BoundedContextId cannot be longer than 4 characters")
        return v

    def __str__(self) -> str:
        return f"BC-{self.value}"

    @classmethod
    def generate(cls) -> 'BoundedContextId':
        """
        Generates a new random BoundedContextId.
        """
        # Generate a random string of 4 characters
        id_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return cls(value=id_value)