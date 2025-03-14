from typing import List
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.value_objects.domain_model import DomainModel
from src.model.services.llm_service import LlmService
from src.model.services.message_parser import MessageParser
from src.model.value_objects.message import Message


class ModelGenerator:
    """
    Domain service that generates DDD model code using a LLM.
    """
    
    def __init__(self, llm_service: LlmService):
        """
        Initialize the ModelGenerator with a LLM service.
        
        Args:
            llm_service: The LLM service to use for generating the model.
        """
        self.llm_service = llm_service
        self.message_parser = MessageParser()
    
    def generate_model(self, requirements: List[ModelRequirement]) -> DomainModel:
        """
        Generates a DDD model from scratch based on the provided requirements.
        
        Args:
            requirements: The requirements for the DDD model.
            
        Returns:
            A DomainModel containing the generated code.
        """
        assert requirements, "Requirements cannot be empty"
        
        # Prepare the requirements text
        requirements_text = "\n".join([f"{req.id}: {req.requirement_text}" for req in requirements])
        
        # Prepare the system prompt
        system_prompt = f"""
You are a Domain-Driven Design expert. You will create a clean DDD model based on the following requirements:

{requirements_text}

{self.message_parser.get_file_template_with_example()}

Follow these guidelines for a clean DDD model:
- IDs should have their own value object class
- IDs of aggregates and entities are auto generated when a fresh object is created
- Aggregates must only reference other aggregates via the ID of the aggregate root
- Generate a Repository for each Aggregate that needs to be persisted
- A Repository MUST be abstract (the implementation is not part of the model)
- A Repository MUST have at least a function `get_by_id` and a function `save`
- Private methods must be prefixed with an underscore
- Make assertions about the model state before the actual code in the model methods
- Use enums to restrict values
- Aggregates and value objects must not depend on or call domain services
"""
        
        # Generate the model using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content="Please generate a clean DDD model based on the requirements.")
        ]
        
        response = self.llm_service.generate_response(messages)
        
        # Parse the files from the response
        files_dict = self.message_parser.parse_files_from_message(response)
        
        # Convert to DomainModel
        domain_model = DomainModel(files=files_dict.files)
        
        return domain_model
    
    def modify_model(self, requirements: List[ModelRequirement], current_model: DomainModel) -> DomainModel:
        """
        Modifies an existing DDD model based on the provided requirements.
        
        Args:
            requirements: The requirements for the DDD model.
            current_model: The current domain model to modify.
            
        Returns:
            A DomainModel containing the modified code.
        """
        assert requirements, "Requirements cannot be empty"
        assert current_model, "Current model cannot be empty"
        
        # Prepare the requirements text
        requirements_text = "\n".join([f"{req.id}: {req.requirement_text}" for req in requirements])
        
        # Prepare the current model files
        current_files = ""
        for path, content in current_model.files.items():
            current_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"
        
        # Prepare the system prompt
        system_prompt = f"""
You are a Domain-Driven Design expert. You will modify an existing DDD model based on the following requirements:

{requirements_text}

Here is the current model:
{current_files}

{self.message_parser.get_diff_template_with_example()}

Follow these guidelines for a clean DDD model:
- IDs should have their own value object class
- IDs of aggregates and entities are auto generated when a fresh object is created
- Aggregates must only reference other aggregates via the ID of the aggregate root
- Generate a Repository for each Aggregate that needs to be persisted
- A Repository MUST be abstract (the implementation is not part of the model)
- A Repository MUST have at least a function `get_by_id` and a function `save`
- Private methods must be prefixed with an underscore
- Make assertions about the model state before the actual code in the model methods
- Use enums to restrict values
- Aggregates and value objects must not depend on or call domain services
"""
        
        # Generate the model modifications using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content="Please generate the necessary changes to the DDD model based on the requirements.")
        ]
        
        response = self.llm_service.generate_response(messages)
        
        # Parse the diffs from the response
        diffs = self.message_parser.parse_diffs_from_message(response)
        
        # Create a new domain model as a copy of the current one
        modified_model = DomainModel(files=dict(current_model.files))
        
        # Apply the diffs to the model
        for filename, diff_content in diffs.items():
            # In a real implementation, you would apply the diff to the file content
            # For now, we'll just call the apply_diff method which is a placeholder
            modified_model.apply_diff(diff_content)
        
        return modified_model
