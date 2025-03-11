from pydantic import BaseModel
from typing import Optional

from src.model.bounded_context.bounded_context import BoundedContext
from src.model.bounded_context.bounded_context_id import BoundedContextId
from src.model.bounded_context.bounded_context_repository import BoundedContextRepository


class CreateBoundedContextInput(BaseModel):
    """Input data for creating a bounded context"""
    name: str


class CreateBoundedContextOutput(BaseModel):
    """Output data after creating a bounded context"""
    id: str
    name: str


class RenameBoundedContextInput(BaseModel):
    """Input data for renaming a bounded context"""
    bounded_context_id: str
    new_name: str


class BoundedContextCommands:
    """
    Application service for bounded context commands
    """
    
    def __init__(self, bounded_context_repository: BoundedContextRepository):
        """Initialize with required repositories"""
        self.bounded_context_repository = bounded_context_repository
    
    def create_bounded_context(self, input_data: CreateBoundedContextInput) -> CreateBoundedContextOutput:
        """
        Creates a new bounded context with the given name
        """
        # Create a new bounded context
        bounded_context = BoundedContext(name=input_data.name)
        
        # Save it to the repository
        self.bounded_context_repository.save(bounded_context)
        
        # Return the output DTO
        return CreateBoundedContextOutput(
            id=str(bounded_context.id),
            name=bounded_context.name
        )
    
    def rename_bounded_context(self, input_data: RenameBoundedContextInput) -> None:
        """
        Renames an existing bounded context
        """
        # Create the ID value object
        bounded_context_id = BoundedContextId(value=input_data.bounded_context_id)
        
        # Get the bounded context from the repository
        bounded_context = self.bounded_context_repository.get_by_id(bounded_context_id)
        if not bounded_context:
            raise ValueError(f"Bounded context with ID {bounded_context_id} not found")
        
        # Update the name
        bounded_context.update_name(input_data.new_name)
        
        # Save the updated bounded context
        self.bounded_context_repository.save(bounded_context)