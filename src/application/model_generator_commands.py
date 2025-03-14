from pydantic import BaseModel
from typing import Dict, List
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.services.model_generator import ModelGenerator


class GenerateModelInput(BaseModel):
    """Input data for generating a domain model"""
    pass


class GenerateModelOutput(BaseModel):
    """Output data after generating a domain model"""
    files: Dict[str, str]


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
        Generates a domain model from all the model requirements
        
        Args:
            input_data: The input data (empty in this case)
            
        Returns:
            Output containing the generated model files
        """
        # Get all model requirements
        requirements = self.model_requirement_repository.get_all()
        
        # Generate the domain model
        domain_model = self.model_generator.generate_model(requirements)
        
        # Return the generated files
        return GenerateModelOutput(files=domain_model.files)