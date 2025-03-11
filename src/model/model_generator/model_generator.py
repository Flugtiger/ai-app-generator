from typing import List

from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.services.llm_service import LlmService
from src.model.services.message_parser import MessageParser
from src.model.value_objects.domain_model import DomainModel
from src.model.value_objects.message import Message


class ModelGenerator:
    """
    Domain service for generating DDD models using an LLM.
    """
    
    def __init__(self, llm_service: LlmService):
        """
        Initializes the ModelGenerator with an LLM service.
        """
        self._llm_service = llm_service
        self._message_parser = MessageParser()
    
    def generate_model(self, requirements: List[ModelRequirement]) -> DomainModel:
        """
        Generates a DDD model from scratch based on the given requirements.
        
        Args:
            requirements: List of model requirements
            
        Returns:
            Generated domain model
        """
        # Create the system prompt
        system_prompt = self._create_system_prompt(requirements)
        system_message = Message.system(system_prompt)
        
        # Generate the model using the LLM
        response = self._llm_service.generate_response([system_message])
        
        # Parse the response to extract the files
        files_dict = self._message_parser.parse_files(response)
        
        # Convert to DomainModel
        return DomainModel(files=files_dict.files)
    
    def modify_model(self, current_model: DomainModel, requirements: List[ModelRequirement]) -> DomainModel:
        """
        Modifies an existing domain model based on the given requirements.
        
        Args:
            current_model: Current domain model
            requirements: List of model requirements
            
        Returns:
            Modified domain model
        """
        # Create the system prompt for modification
        system_prompt = self._create_modification_prompt(current_model, requirements)
        system_message = Message.system(system_prompt)
        
        # Generate the diffs using the LLM
        response = self._llm_service.generate_response([system_message])
        
        # Parse the response to extract the diffs
        diffs = self._message_parser.parse_diffs(response)
        
        # Create a copy of the current model
        modified_model = DomainModel(files=current_model.files.copy())
        
        # Apply the diffs to the model
        modified_model.apply_diffs(diffs)
        
        return modified_model
    
    def _create_system_prompt(self, requirements: List[ModelRequirement]) -> str:
        """
        Creates a system prompt for generating a DDD model from scratch.
        
        Args:
            requirements: List of model requirements
            
        Returns:
            System prompt
        """
        # Combine all requirement texts
        requirements_text = "\n".join([req.requirement_text for req in requirements])
        
        # Create the system prompt
        prompt = f"""
You are an expert in Domain-Driven Design (DDD) and clean code.
You will create a clean DDD model based on the following requirements:

{requirements_text}

{self._message_parser.get_file_template()}

Please follow these guidelines for a clean DDD model:
- Use proper aggregates, entities, value objects, and domain services
- IDs should have their own value object class
- Aggregates must only reference other aggregates via the ID of the aggregate root
- Make assertions about the model state in methods
- Use enums to restrict values
- Aggregates and value objects must not depend on or call domain services
"""
        return prompt
    
    def _create_modification_prompt(self, current_model: DomainModel, requirements: List[ModelRequirement]) -> str:
        """
        Creates a system prompt for modifying an existing DDD model.
        
        Args:
            current_model: Current domain model
            requirements: List of model requirements
            
        Returns:
            System prompt
        """
        # Combine all requirement texts
        requirements_text = "\n".join([req.requirement_text for req in requirements])
        
        # Create a representation of the current model
        model_files = ""
        for path, content in current_model.files.items():
            model_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"
        
        # Create the system prompt
        prompt = f"""
You are an expert in Domain-Driven Design (DDD) and clean code.
You will modify an existing DDD model based on the following requirements:

{requirements_text}

Here is the current model:
{model_files}

{self._message_parser.get_diff_template()}

Please follow these guidelines for a clean DDD model:
- Use proper aggregates, entities, value objects, and domain services
- IDs should have their own value object class
- Aggregates must only reference other aggregates via the ID of the aggregate root
- Make assertions about the model state in methods
- Use enums to restrict values
- Aggregates and value objects must not depend on or call domain services

Only output diffs for files that need to be modified. If a file needs to be created, include the entire file content in the diff.
"""
        return prompt