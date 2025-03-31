import json
import os
from typing import List, Dict, Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks.usage import get_usage_metadata_callback

from src.model.services.llm_service import LlmService
from src.model.value_objects.message import Message


class LangchainLlmService(LlmService):
    """
    Langchain implementation of the LlmService interface using Anthropic Claude 3.7 Sonnet.
    """

    def __init__(self):
        """
        Initialize the LangchainLlmService with Anthropic Claude 3.7 Sonnet.
        The API key is read from the ANTHROPIC_API_KEY environment variable.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

        self.llm = ChatAnthropic(
            model="claude-3-7-sonnet-latest",
            anthropic_api_key=api_key,
            temperature=0.0,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            max_tokens=50000
        )

    def generate_response(self, messages: List[Message]) -> Message:
        """
        Takes messages as input and returns the response message from the LLM.

        Args:
            messages: List of messages to send to the LLM

        Returns:
            Response message from the LLM
        """
        # Convert our domain Message objects to Langchain message objects
        langchain_messages = []

        for message in messages:
            if message.role == "system":
                langchain_messages.append(SystemMessage(content=message.content))
            elif message.role == "user":
                langchain_messages.append(HumanMessage(content=message.content))
            elif message.role == "assistant":
                langchain_messages.append(AIMessage(content=message.content))

        # Generate response
        with get_usage_metadata_callback() as cb:
            response = self.llm.invoke(langchain_messages)

        # Print token usage statistics
        if cb.usage_metadata:
            print("\n--- Token Usage Statistics ---")
            print(json.dumps(cb.usage_metadata, indent=2))
            print("-----------------------------\n")

        # Convert Langchain response back to our domain Message object
        return Message(role="assistant", content=response.content)
