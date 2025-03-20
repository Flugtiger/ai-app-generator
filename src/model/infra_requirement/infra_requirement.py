from pydantic import BaseModel, Field
from typing import ClassVar, Optional
import re
from src.model.infra_requirement.infra_requirement_id import InfraRequirementId


class InfraRequirement(BaseModel):
    """
    Represents a requirement for infrastructure code.
    Contains arbitrary text that describes the requirement.
    """
    id: InfraRequirementId
    requirement_text: str

    # Class variable to track the last used number for auto-incrementing IDs
    _last_id_number: ClassVar[int] = 0
    _initialized: ClassVar[bool] = False

    @classmethod
    def initialize_last_id(cls, existing_requirements):
        """
        Initialize the _last_id_number based on existing requirements.
        This should be called when the repository is initialized.
        
        Args:
            existing_requirements: List of existing InfraRequirement objects
        """
        if cls._initialized:
            return
            
        max_id = 0
        for req in existing_requirements:
            # Extract the number part from the ID
            match = re.match(r'IR-(\d+)', req.id.value)
            if match:
                id_num = int(match.group(1))
                max_id = max(max_id, id_num)
        
        cls._last_id_number = max_id
        cls._initialized = True

    def __init__(self, **data):
        """
        Initialize a new InfraRequirement.
        If no ID is provided, a new one will be generated.
        """
        if 'id' not in data:
            InfraRequirement._last_id_number += 1
            data['id'] = InfraRequirementId(value=f"IR-{InfraRequirement._last_id_number}")
        
        super().__init__(**data)

    class Config:
        arbitrary_types_allowed = True
