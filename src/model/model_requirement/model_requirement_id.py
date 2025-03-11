import uuid
from pydantic import BaseModel


class ModelRequirementId(BaseModel):
    """
    Value object representing the ID of a ModelRequirement.
    """
    value: str

    def __str__(self) -> str:
        return f"REQ-{self.value}"

    @classmethod
    def generate(cls) -> 'ModelRequirementId':
        """
        Generates a new random ModelRequirementId.
        """
        return cls(value=str(uuid.uuid4()))