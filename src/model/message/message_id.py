from pydantic import BaseModel


class MessageId(BaseModel):
    """
    Value object representing the unique identifier for a Message.
    """
    value: str

    def __str__(self) -> str:
        return self.value