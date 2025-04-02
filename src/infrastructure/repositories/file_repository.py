import json
import os
import re
from abc import ABC
from pathlib import Path
from typing import Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
ID = TypeVar('ID', bound=BaseModel)

class FileRepository(Generic[T, ID]):
    """
    Generic repository implementation that stores entities as JSON files.
    """
    
    def __init__(self, 
                 entity_class: Type[T], 
                 id_class: Type[ID], 
                 folder_name: str, 
                 id_prefix: str):
        """
        Initialize the repository with entity class, ID class, folder name and ID prefix.
        """
        self.entity_class = entity_class
        self.id_class = id_class
        self.base_folder = os.path.join('data', folder_name)
        self.id_prefix = id_prefix
        self.next_id = self._determine_next_id()
        
        # Create folder if it doesn't exist
        os.makedirs(self.base_folder, exist_ok=True)
    
    def _determine_next_id(self) -> int:
        """
        Determine the next available ID by scanning existing files.
        """
        if not os.path.exists(self.base_folder):
            return 1
            
        max_id = 0
        pattern = re.compile(f"{self.id_prefix}-([0-9]+)")
        
        for filename in os.listdir(self.base_folder):
            if not filename.endswith('.json'):
                continue
                
            match = pattern.match(filename.split('.')[0])
            if match:
                id_num = int(match.group(1))
                max_id = max(max_id, id_num)
        
        return max_id + 1
    
    def _generate_id(self) -> ID:
        """
        Generate a new ID for an entity.
        """
        id_value = f"{self.id_prefix}-{self.next_id}"
        self.next_id += 1
        return self.id_class(value=id_value)
    
    def _get_file_path(self, id_value: str) -> str:
        """
        Get the file path for an entity with the given ID.
        """
        return os.path.join(self.base_folder, f"{id_value}.json")
    
    def get_by_id(self, id: ID) -> T:
        """
        Retrieve an entity by its ID.
        """
        file_path = self._get_file_path(str(id))
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Entity with ID {id} not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return self.entity_class.model_validate(data)
    
    def save(self, entity: T) -> T:
        """
        Save an entity to the repository. Generates and sets ID if not present.
        """
        # Generate and set ID if not present
        if entity.id is None:
            entity.id = self._generate_id()
        
        # Save to file
        file_path = self._get_file_path(str(entity.id))
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(entity.model_dump_json(indent=2))
        
        return entity
    
    def get_all(self) -> List[T]:
        """
        Retrieve all entities from the repository, sorted by ID.
        """
        entities = []
        
        if not os.path.exists(self.base_folder):
            return entities
        
        for filename in os.listdir(self.base_folder):
            if not filename.endswith('.json'):
                continue
                
            file_path = os.path.join(self.base_folder, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            entity = self.entity_class.model_validate(data)
            entities.append(entity)
        
        # Sort by ID length first, then by ID string
        return sorted(entities, key=lambda e: (len(str(e.id)), str(e.id)))