from abc import ABC, abstractmethod
from typing import List

from src.model.message.message import Message


class LLMService(ABC):
    """
    Abstract domain service that handles the interactions with a LLM (chat model).
    """
    
    @abstractmethod
    def generate_response(self, messages: List[Message]) -> Message:
        """
        Takes a list of Message value objects as input and returns the response message from the LLM.
        """
        pass