from abc import ABC, abstractmethod
from typing import Optional
from langchain.chat_models import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

class BaseAgent(ABC):
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            api_key=api_key,
            model_name="llama2-70b-4096"
        )
        self.system_prompt = self._get_system_prompt()

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """Check if this agent can handle the given query."""
        pass

    def process(self, query: str) -> str:
        """Process the query and return a response."""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=query)
        ]
        response = self.llm.invoke(messages)
        return response.content
