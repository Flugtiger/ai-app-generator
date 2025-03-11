from pydantic import BaseModel

from src.model.bounded_context.bounded_context_id import BoundedContextId
from src.model.bounded_context.bounded_context_repository import BoundedContextRepository
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository


class CreateModelRequirementInput(BaseModel):
    """Input data for creating a model requirement"""
    bounded_context_id: str
    requirement_text: str


class CreateModelRequirementOutput(BaseModel):
    """Output data after creating a model requirement"""
    id: str
    bounded_context_id: str
    requirement_text: str


class ModelRequirementCommands:
    """
    Application service for model requirement commands
    """
    
    def __init__(
        self, 
        model_requirement_repository: ModelRequirementRepository,
        bounded_context_repository: BoundedContextRepository
    ):
        """Initialize with required repositories"""
        self.model_requirement_repository = model_requirement_repository
        self.bounded_context_repository = bounded_context_repository
    
    def create_model_requirement(self, input_data: CreateModelRequirementInput) -> CreateModelRequirementOutput:
        """
        Creates a new model requirement for a bounded context
        """
        # Create the ID value object
        bounded_context_id = BoundedContextId(value=input_data.bounded_context_id)
        
        # Get the bounded context from the repository
        bounded_context = self.bounded_context_repository.get_by_id(bounded_context_id)
        if not bounded_context:
            raise ValueError(f"Bounded context with ID {bounded_context_id} not found")
        
        # Create a new model requirement
        model_requirement = bounded_context.create_model_requirement(
            requirement_text=input_data.requirement_text
        )
        
        # Save it to the repository
        self.model_requirement_repository.save(model_requirement)
        
        # Return the output DTO
        return CreateModelRequirementOutput(
            id=str(model_requirement.id),
            bounded_context_id=str(model_requirement.bounded_context_id),
            requirement_text=model_requirement.requirement_text
        )