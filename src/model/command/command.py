from pydantic import BaseModel

from src.model.bounded_context.bounded_context_id import BoundedContextId
from src.model.command.command_id import CommandId


class Command(BaseModel):
    """
    Represents a Command in the system.
    A Command is associated with a BoundedContext and has a name and description.
    """
    id: CommandId
    bounded_context_id: BoundedContextId
    name: str
    description: str

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, bounded_context_id: BoundedContextId, name: str, description: str, id: CommandId = None, **data):
        """
        Creates a new Command with the given bounded_context_id, name, and description.
        If no ID is provided, a new one is generated.
        """
        if id is None:
            id = CommandId.generate()
        super().__init__(id=id, bounded_context_id=bounded_context_id, name=name, description=description, **data)

    def update_name(self, new_name: str) -> None:
        """
        Updates the name of the Command.
        """
        assert new_name, "Name cannot be empty"
        self.name = new_name

    def update_description(self, new_description: str) -> None:
        """
        Updates the description of the Command.
        """
        assert new_description, "Description cannot be empty"
        self.description = new_description