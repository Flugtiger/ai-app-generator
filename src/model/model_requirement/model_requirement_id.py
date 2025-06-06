from pydantic import BaseModel


class ModelRequirementId(BaseModel):
    """
    Value object representing the unique identifier for a ModelRequirement.
    """
    value: str

    def __str__(self) -> str:
        return self.value