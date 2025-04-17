from typing import List
from agents.base_agent import BaseAgent

class AgentRouter:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents

    def route_query(self, query: str) -> BaseAgent:
        """Route the query to the appropriate agent."""
        for agent in self.agents:
            if agent.can_handle(query):
                return agent
        return self.agents[-1]  # Return the last agent (FallbackAgent)
