from abc import ABC, abstractmethod
from typing import List

from src.model.command.command import Command
from src.model.command.command_id import CommandId


class CommandRepository(ABC):
    """
    Repository interface for Command aggregate.
    """
    @abstractmethod
    def get_by_id(self, id: CommandId) -> Command:
        """
        Retrieves a Command by its ID.
        """
        pass

    @abstractmethod
    def save(self, command: Command) -> Command:
        """
        Saves a Command to the repository.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Command]:
        """
        Retrieves all Commands from the repository.
        """
        pass