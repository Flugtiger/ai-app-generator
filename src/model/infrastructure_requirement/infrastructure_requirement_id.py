from pydantic import BaseModel


class InfrastructureRequirementId(BaseModel):
    """
    Value object representing the unique identifier for an InfrastructureRequirement.
    """
    value: str

    def __str__(self) -> str:
        return self.value