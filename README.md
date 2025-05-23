# Multi-Agent Assistant System

A Streamlit-based application that combines multiple AI agents to provide various services through a unified chat interface.

## 🌟 Features

- **📧 Email Agent**: Drafts professional emails based on your requirements
- **🌐 Translation Agent**: Translates text between different languages
- **⛅ Weather Agent**: Provides weather information for specified locations
- **🤖 Fallback Agent**: Handles general queries not covered by specialized agents

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Backend**: Groq API
- **Language**: Python 3.x
- **Architecture**: Multi-agent system with dynamic routing

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multi-agent-system.git
   cd multi-agent-system
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 💻 Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Interact with the multi-agent system through the chat interface

## 🧩 System Architecture

The system consists of:

- **Agent Router**: Analyzes user queries and routes them to the appropriate specialized agent
- **Session Manager**: Maintains conversation context and history
- **Specialized Agents**:
  - Email Agent: Handles email drafting requests
  - Translation Agent: Processes language translation requests
  - Weather Agent: Responds to weather-related queries
  - Fallback Agent: Handles general queries outside the scope of specialized agents

## 🔧 Customization

You can extend the system by adding new agents:

1. Create a new agent class in the `agents` directory that inherits from `BaseAgent`
2. Implement the required methods
3. Add the new agent to the initialization in `app.py`

## 📄 License

[MIT License](LICENSE)

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.