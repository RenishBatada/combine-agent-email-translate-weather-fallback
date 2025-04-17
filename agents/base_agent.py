from abc import ABC, abstractmethod
from typing import Optional, List
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage, AIMessage


class BaseAgent(ABC):
    def __init__(self, api_key: str):
        self.llm = ChatGroq(api_key=api_key, model_name="llama-3.3-70b-versatile")
        self.system_prompt = self._get_system_prompt()

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    def process(self, query: str, chat_history: List[tuple] = None) -> str:
        """Process the query and return a response."""
        messages = [SystemMessage(content=self.system_prompt)]

        # Add chat history if available
        if chat_history:
            for human_msg, ai_msg in chat_history:
                messages.extend(
                    [HumanMessage(content=human_msg), AIMessage(content=ai_msg)]
                )

        messages.append(HumanMessage(content=query))
        response = self.llm.invoke(messages)
        return response.content
