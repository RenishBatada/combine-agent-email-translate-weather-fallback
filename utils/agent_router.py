from typing import List, Dict
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from agents.base_agent import BaseAgent

class AgentRouter:
    def __init__(self, agents: List[BaseAgent], groq_api_key: str):
        self.agents = agents
        self.llm = ChatGroq(
            api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile"
        )
        self.agent_map: Dict[str, BaseAgent] = {
            "email": agents[0],
            "translate": agents[1],
            "weather": agents[2],
            "fallback": agents[3]
        }
        self.last_category = None

    def route_query(self, query: str, chat_history: List[tuple] = None) -> BaseAgent:
        """Route the query to the appropriate agent using LLM."""
        print(f"\nDEBUG: Current query: {query}")
        print(f"DEBUG: Chat history exists: {bool(chat_history)}")
        print(f"DEBUG: Last category: {self.last_category}")
        
        if chat_history and len(chat_history) > 0:
            # Get the last exchange
            last_query, last_response = chat_history[-1]
            
            system_prompt = f"""Analyze if this is a follow-up question to the previous conversation.

Previous conversation:
User: {last_query}
Assistant: {last_response}

New message: {query}

Task: Is this a follow-up to modify/continue the previous conversation?
If YES: respond with exactly "{self.last_category if self.last_category else 'fallback'}"
If NO: classify as one of: email, translate, weather, fallback

Examples of follow-ups:
1. Previous: "write a sick leave email"
   Follow-up: "add my name as John" -> email
   Follow-up: "make it shorter" -> email
   Follow-up: "change the date" -> email

2. Previous: "translate hello to Spanish"
   Follow-up: "now to French" -> translate
   Follow-up: "make it formal" -> translate

Respond with ONLY the category name."""

            print(f"DEBUG: Using follow-up detection prompt")
        else:
            system_prompt = """Classify the query into exactly one category:
- email: Writing or modifying emails
- translate: Language translation
- weather: Weather information
- fallback: Anything else

Examples:
"write a sick leave email" -> email
"translate hello to Spanish" -> translate
"what's the weather in London" -> weather
"what is 2+2" -> fallback

Respond with ONLY the category name."""
            print(f"DEBUG: Using initial classification prompt")

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        category = response.content.strip().lower()
        print(f"DEBUG: LLM classified as: {category}")
        
        self.last_category = category
        print(f"DEBUG: Updated last category to: {self.last_category}")
        
        return self.agent_map.get(category, self.agent_map["fallback"])
