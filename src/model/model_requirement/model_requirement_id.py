from pydantic import BaseModel, validator


class ModelRequirementId(BaseModel):
    """
    Value object representing the ID of a ModelRequirement.
    Format: 'MR-' followed by a number.
    """
    value: str

    @validator('value')
    def validate_format(cls, v):
        """
        Validates that the ID follows the required format: 'MR-' followed by a number.
        """
        if not v.startswith('MR-'):
            raise ValueError(f"ModelRequirementId must start with 'MR-', got {v}")
        
        # Check that the part after 'MR-' is a number
        number_part = v[3:]
        if not number_part.isdigit():
            raise ValueError(f"ModelRequirementId must be in format 'MR-<number>', got {v}")
        
        return v

    def __str__(self):
        return self.value