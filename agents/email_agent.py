from .base_agent import BaseAgent

class EmailAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """You are an email drafting assistant. Help users write professional 
        and well-structured emails based on their requirements. Focus on clarity, 
        professionalism, and appropriate tone."""

    def can_handle(self, query: str) -> bool:
        keywords = ['email', 'draft', 'write', 'compose', 'mail']
        return any(keyword in query.lower() for keyword in keywords)
