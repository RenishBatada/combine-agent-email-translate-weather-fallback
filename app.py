import os
import streamlit as st
from dotenv import load_dotenv
from agents.email_agent import EmailAgent
from agents.translate_agent import TranslateAgent
from agents.weather_agent import WeatherAgent
from agents.fallback_agent import FallbackAgent
from utils.session_manager import SessionManager
from utils.agent_router import AgentRouter

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize session state
if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionManager()

def initialize_agents():
    """Initialize all agents with necessary API keys."""
    agents = [
        EmailAgent(GROQ_API_KEY),
        TranslateAgent(GROQ_API_KEY),
        WeatherAgent(GROQ_API_KEY),
        FallbackAgent(GROQ_API_KEY)  # Fallback agent should be last
    ]
    return AgentRouter(agents)

def main():
    st.title("🤖 Multi-Agent Assistant")
    st.write("""
    I can help you with:
    - 📧 Email drafting
    - 🌐 Language translation
    - ⛅ Weather information
    """)

    # Initialize agent router
    agent_router = initialize_agents()

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from appropriate agent
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                agent = agent_router.route_query(prompt)
                response = agent.process(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        # Save to session history
        st.session_state.session_manager.add_message(
            session_id=str(id(st.session_state)),
            user_message=prompt,
            bot_message=response
        )

if __name__ == "__main__":
    main()
