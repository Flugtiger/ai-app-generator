import uuid
from pydantic import BaseModel


class CommandId(BaseModel):
    """
    Value object representing the ID of a Command.
    """
    value: str

    def __str__(self) -> str:
        return f"CMD-{self.value}"

    @classmethod
    def generate(cls) -> 'CommandId':
        """
        Generates a new random CommandId.
        """
        return cls(value=str(uuid.uuid4()))