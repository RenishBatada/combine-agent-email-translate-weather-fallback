from .base_agent import BaseAgent

class FallbackAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """You are a fallback agent that handles queries outside the scope 
        of our specialized agents."""

    def can_handle(self, query: str) -> bool:
        return True  # Fallback agent handles everything

    def process(self, query: str) -> str:
        return "I can only answer questions related to email draft, translation, or weather."
