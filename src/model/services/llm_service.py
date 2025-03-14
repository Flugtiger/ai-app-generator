from abc import ABC, abstractmethod
from typing import List
from src.model.value_objects.message import Message


class LlmService(ABC):
    """
    Abstract domain service that handles interactions with a LLM (chat model).
    Takes 'messages' as input and returns the response message from the LLM.
    The actual implementation is part of the infrastructure layer.
    """
    
    @abstractmethod
    def generate_response(self, messages: List[Message]) -> Message:
        """
        Generates a response from the LLM based on the provided messages.
        
        Args:
            messages: A list of Message objects to send to the LLM.
            
        Returns:
            The response Message from the LLM.
        """
        pass
