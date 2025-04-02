from pydantic import BaseModel


class CommandId(BaseModel):
    """
    Value object representing the unique identifier for a Command.
    """
    value: str

    def __str__(self) -> str:
        return self.value