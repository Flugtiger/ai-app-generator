import os
import sys
from typing import List

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.model.message.message import Message, MessageRole
from src.model.services.llm_service import LLMService


class LLMServiceImpl(LLMService):
    """
    Implementation of LLMService using Langchain with Anthropic Claude.
    """
    
    def __init__(self):
        """
        Initialize the LLM service with Anthropic Claude.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        self.llm = ChatAnthropic(
            model="claude-3-7-sonnet-latest",
            anthropic_api_key=api_key,
            temperature=0,
            max_tokens=25000,
            streaming=True
        )
    
    def _convert_to_langchain_messages(self, messages: List[Message]):
        """
        Convert domain model messages to Langchain messages.
        """
        langchain_messages = []
        
        for message in messages:
            if message.role == MessageRole.SYSTEM:
                langchain_messages.append(SystemMessage(content=message.content))
            elif message.role == MessageRole.USER:
                langchain_messages.append(HumanMessage(content=message.content))
            elif message.role == MessageRole.ASSISTANT:
                langchain_messages.append(AIMessage(content=message.content))
        
        return langchain_messages
    
    def generate_response(self, messages: List[Message]) -> Message:
        """
        Takes a list of Message value objects as input and returns the response message from the LLM.
        Streams the output to stdout.
        """
        langchain_messages = self._convert_to_langchain_messages(messages)
        
        # Stream the response to stdout
        response_content = ""
        for chunk in self.llm.stream(langchain_messages):
            chunk_content = chunk.content
            response_content += chunk_content
            sys.stdout.write(chunk_content)
            sys.stdout.flush()
        
        # Add a newline at the end of the output
        sys.stdout.write("\n")
        sys.stdout.flush()
        
        # Return the complete response as a Message
        return Message(
            role=MessageRole.ASSISTANT,
            content=response_content
        )