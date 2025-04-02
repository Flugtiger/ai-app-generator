from typing import List

from src.model.command.command import Command
from src.model.command.command_id import CommandId
from src.model.command.command_repository import CommandRepository
from src.infrastructure.repositories.file_repository import FileRepository


class CommandRepositoryImpl(CommandRepository):
    """
    Implementation of CommandRepository that stores Commands as JSON files.
    """
    
    def __init__(self):
        """
        Initialize the repository with Command class and CommandId class.
        """
        self.repository = FileRepository(
            entity_class=Command,
            id_class=CommandId,
            folder_name='commands',
            id_prefix='CMD'
        )
    
    def get_by_id(self, id: CommandId) -> Command:
        """
        Retrieves a Command by its ID.
        """
        return self.repository.get_by_id(id)
    
    def save(self, command: Command) -> Command:
        """
        Saves a Command to the repository.
        """
        return self.repository.save(command)
    
    def get_all(self) -> List[Command]:
        """
        Retrieves all Commands from the repository.
        """
        return self.repository.get_all()