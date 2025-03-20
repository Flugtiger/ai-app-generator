import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
ID = TypeVar('ID', bound=BaseModel)


class FileBasedRepository(Generic[T, ID], ABC):
    """
    A generic file-based repository implementation that serializes entities to JSON files.
    """

    def __init__(self, base_dir: str):
        """
        Initialize the repository with a base directory for storing files.

        Args:
            base_dir: The base directory where entity files will be stored
        """
        self.base_dir = Path(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    @abstractmethod
    def get_id(self, entity: T) -> ID:
        """
        Extract the ID from an entity.

        Args:
            entity: The entity to extract the ID from

        Returns:
            The ID of the entity
        """
        pass

    @abstractmethod
    def get_entity_type(self) -> Type[T]:
        """
        Get the type of entity this repository manages.

        Returns:
            The entity type
        """
        pass

    def get_file_path(self, id: ID) -> Path:
        """
        Get the file path for an entity with the given ID.

        Args:
            id: The ID of the entity

        Returns:
            The file path where the entity is stored
        """
        return self.base_dir / f"{str(id)}.json"

    def save(self, entity: T) -> None:
        """
        Save an entity to a file.

        Args:
            entity: The entity to save
        """
        entity_id = self.get_id(entity)
        file_path = self.get_file_path(entity_id)

        with open(file_path, 'w') as f:
            f.write(entity.model_dump_json(indent=2))

    def get_by_id(self, id: ID) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        Args:
            id: The ID of the entity to retrieve

        Returns:
            The entity if found, None otherwise
        """
        file_path = self.get_file_path(id)

        if not file_path.exists():
            return None

        with open(file_path, 'r') as f:
            data = json.load(f)

        return self.get_entity_type().model_validate(data)

    def get_all(self) -> List[T]:
        """
        Retrieve all entities in the repository.

        Returns:
            A list of all entities
        """
        entities = []

        # Create the directory if it doesn't exist
        os.makedirs(self.base_dir, exist_ok=True)

        for file_path in self.base_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                entity = self.get_entity_type().model_validate(data)
                entities.append(entity)
            except (json.JSONDecodeError, FileNotFoundError):
                # Skip files that can't be parsed
                continue

        return entities

    def delete(self, id: ID) -> None:
        """
        Delete an entity by its ID.

        Args:
            id: The ID of the entity to delete
        """
        file_path = self.get_file_path(id)

        if file_path.exists():
            os.remove(file_path)
