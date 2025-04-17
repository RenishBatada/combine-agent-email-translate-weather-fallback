from typing import Dict, List, Tuple


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, List[Tuple[str, str]]] = {}

    def add_message(self, session_id: str, user_message: str, bot_message: str):
        """Add a message pair to the session history."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append((user_message, bot_message))

    def get_history(self, session_id: str) -> List[Tuple[str, str]]:
        """Get the message history for a session."""
        return self.sessions.get(session_id, [])
