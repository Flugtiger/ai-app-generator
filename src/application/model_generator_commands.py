from pydantic import BaseModel
from typing import List, Dict

from src.model.bounded_context.bounded_context_id import BoundedContextId
from src.model.bounded_context.bounded_context_repository import BoundedContextRepository
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.model_generator.model_generator import ModelGenerator


class GenerateModelInput(BaseModel):
    """Input data for generating a domain model"""
    bounded_context_id: str


class FileContent(BaseModel):
    """Represents a file with its content"""
    path: str
    content: str


class GenerateModelOutput(BaseModel):
    """Output data after generating a domain model"""
    files: List[FileContent]


class ModelGeneratorCommands:
    """
    Application service for model generation commands
    """
    
    def __init__(
        self,
        model_generator: ModelGenerator,
        model_requirement_repository: ModelRequirementRepository,
        bounded_context_repository: BoundedContextRepository
    ):
        """Initialize with required services and repositories"""
        self.model_generator = model_generator
        self.model_requirement_repository = model_requirement_repository
        self.bounded_context_repository = bounded_context_repository
    
    def generate_model(self, input_data: GenerateModelInput) -> GenerateModelOutput:
        """
        Generates a domain model from all the model requirements for a bounded context
        """
        # Create the ID value object
        bounded_context_id = BoundedContextId(value=input_data.bounded_context_id)
        
        # Get the bounded context from the repository
        bounded_context = self.bounded_context_repository.get_by_id(bounded_context_id)
        if not bounded_context:
            raise ValueError(f"Bounded context with ID {bounded_context_id} not found")
        
        # Get all model requirements for the bounded context
        requirements = self.model_requirement_repository.get_by_bounded_context_id(bounded_context_id)
        
        if not requirements:
            raise ValueError(f"No model requirements found for bounded context {bounded_context_id}")
        
        # Generate the domain model
        domain_model = self.model_generator.generate_model(requirements)
        
        # Convert the domain model to the output format
        files = []
        for path, content in domain_model.files.items():
            files.append(FileContent(path=path, content=content))
        
        # Return the output DTO
        return GenerateModelOutput(files=files)