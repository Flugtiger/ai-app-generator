from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LlmService(ABC):
    """
    Abstract domain service that handles interactions with a LLM (chat model).
    Takes 'messages' as input and returns the response message from the LLM.
    The actual implementation is part of the infrastructure layer.
    """
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates a response from the LLM based on the provided messages.
        
        Args:
            messages: A list of message objects to send to the LLM.
                     Each message is a dictionary with at least 'role' and 'content' keys.
            
        Returns:
            The response message from the LLM as a dictionary.
        """
        pass