from abc import ABC, abstractmethod
from typing import List

from src.model.value_objects.message import Message


class LlmService(ABC):
    """
    Abstract domain service that handles interactions with a LLM (chat model).
    The actual implementation is part of the infrastructure layer.
    """
    
    @abstractmethod
    def generate_response(self, messages: List[Message]) -> Message:
        """
        Takes messages as input and returns the response message from the LLM.
        
        Args:
            messages: List of messages to send to the LLM
            
        Returns:
            Response message from the LLM
        """
        pass