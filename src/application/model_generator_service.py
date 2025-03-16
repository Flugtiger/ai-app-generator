from pydantic import BaseModel
from typing import Dict, List
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.services.model_generator.model_generator import ModelGenerator
from src.model.services.domain_model_service import DomainModelService


class GenerateModelInput(BaseModel):
    """Input data for generating a domain model"""
    project_path: str = "generated"


class GenerateModelOutput(BaseModel):
    """Output data after generating a domain model"""
    files_count: int


class ModelGeneratorCommands:
    """
    Application service for model generation commands
    """
    
    def __init__(
        self, 
        model_requirement_repository: ModelRequirementRepository,
        model_generator: ModelGenerator
    ):
        """
        Initialize the service with required dependencies
        
        Args:
            model_requirement_repository: Repository for model requirements
            model_generator: Service for generating domain models
        """
        self.model_requirement_repository = model_requirement_repository
        self.model_generator = model_generator
    
    def generate_model(self, input_data: GenerateModelInput) -> GenerateModelOutput:
        """
        Generates a domain model from all the model requirements and writes it to disk
        
        Args:
            input_data: The input data containing the project path
            
        Returns:
            Output containing the number of files written
        """
        # Get all model requirements
        requirements = self.model_requirement_repository.get_all()
        
        # Generate the domain model
        domain_model = self.model_generator.generate_model(requirements)
        
        # Write the domain model to disk using the domain model service
        DomainModelService.write_to_directory(domain_model, input_data.project_path)
        
        # Return the number of files written
        return GenerateModelOutput(files_count=len(domain_model.files))
