from .base_agent import BaseAgent
from typing import List


class FallbackAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """You are a fallback agent that handles queries outside the scope 
        of our specialized agents."""

    def process(self, query: str, chat_history: List[tuple] = None) -> str:
        """Override process to always return the fallback message."""
        return "I can only answer questions related to email draft, translation, or weather."
