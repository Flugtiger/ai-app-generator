from pydantic import BaseModel, validator


class InfraRequirementId(BaseModel):
    """
    Value object representing the ID of an InfraRequirement.
    Format: 'IR-' followed by a number.
    """
    value: str

    @validator('value')
    def validate_format(cls, v):
        """
        Validates that the ID follows the required format: 'IR-' followed by a number.
        """
        if not v.startswith('IR-'):
            raise ValueError(f"InfraRequirementId must start with 'IR-', got {v}")
        
        # Check that the part after 'IR-' is a number
        number_part = v[3:]
        if not number_part.isdigit():
            raise ValueError(f"InfraRequirementId must be in format 'IR-<number>', got {v}")
        
        return v

    def __str__(self):
        return self.value
