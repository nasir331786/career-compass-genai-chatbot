# app/core/memory.py
"""Session-based conversation memory abstraction."""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ChatMessage:
    """Single chat turn."""
    role: str   # 'user' | 'assistant'
    content: str


@dataclass
class SessionMemory:
    """
    In-session memory. Stored in st.session_state in Streamlit.
    Automatically trims history to control token usage.
    """
    messages: List[ChatMessage] = field(default_factory=list)
    max_history: int = 15

    def add_message(self, role: str, content: str) -> None:
        """Add a new message and trim if over the limit."""
        self.messages.append(ChatMessage(role=role, content=content))
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def to_dicts(self) -> List[Dict[str, Any]]:
        """Convert messages to list of plain dicts for prompt building."""
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def clear(self) -> None:
        """Reset conversation history."""
        self.messages.clear()
