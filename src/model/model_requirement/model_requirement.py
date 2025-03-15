from pydantic import BaseModel, Field
from typing import ClassVar, Optional
import re
from src.model.model_requirement.model_requirement_id import ModelRequirementId


class ModelRequirement(BaseModel):
    """
    Represents a requirement for a DDD model.
    Contains arbitrary text that describes the requirement.
    """
    id: ModelRequirementId
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
            existing_requirements: List of existing ModelRequirement objects
        """
        if cls._initialized:
            return
            
        max_id = 0
        for req in existing_requirements:
            # Extract the number part from the ID
            match = re.match(r'MR-(\d+)', req.id.value)
            if match:
                id_num = int(match.group(1))
                max_id = max(max_id, id_num)
        
        cls._last_id_number = max_id
        cls._initialized = True

    def __init__(self, **data):
        """
        Initialize a new ModelRequirement.
        If no ID is provided, a new one will be generated.
        """
        if 'id' not in data:
            ModelRequirement._last_id_number += 1
            data['id'] = ModelRequirementId(value=f"MR-{ModelRequirement._last_id_number}")
        
        super().__init__(**data)

    class Config:
        arbitrary_types_allowed = True
