# app/core/prompts.py
"""Prompt engineering module: builds domain-aware system prompts and messages."""

from dataclasses import dataclass
from typing import List

from .config import Settings


@dataclass
class PromptBuilder:
    """Builds structured prompts for the Gemini API."""
    settings: Settings

    def build_system_prompt(self) -> str:
        """Assemble the full system prompt from config."""
        p = self.settings.prompts
        return (
            f"{p.system_role}\n\n"
            f"Domain: {p.domain_description}\n\n"
            f"Response style: {p.response_style}\n\n"
            f"Safety:\n{p.safety_instructions}\n\n"
            f"Output format:\n{p.output_format}\n"
        )

    def build_messages(
        self,
        history: List[dict],
        user_message: str,
    ) -> List[dict]:
        """
        Build the full messages list including system prompt.

        Args:
            history: list of {role: 'user'|'assistant', content: str}
            user_message: the new user input

        Returns:
            List of message dicts for the Gemini API.
        """
        system_prompt = self.build_system_prompt()
        messages: List[dict] = [
            {"role": "user", "content": system_prompt}
        ]

        for h in history:
            messages.append(
                {
                    "role": "user" if h["role"] == "user" else "model",
                    "content": h["content"],
                }
            )

        messages.append({"role": "user", "content": user_message})
        return messages
