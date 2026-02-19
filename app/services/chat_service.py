# app/services/chat_service.py
"""Chat orchestration: ties together prompt building, memory, and Gemini API."""

import logging
from typing import Tuple

from app.core.config import Settings
from app.core.memory import SessionMemory
from app.core.prompts import PromptBuilder
from app.core.models import GeminiClient
from .utils import approximate_token_count, sanitize_user_input


logger = logging.getLogger(__name__)


class ChatService:
    """
    Orchestrates the full pipeline for a single user message:
    1. Sanitize input
    2. Build prompt with history
    3. Call Gemini API
    4. Store assistant reply in memory
    5. Return reply + token estimate
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.prompt_builder = PromptBuilder(settings=settings)
        self.client = GeminiClient(settings=settings)

    def handle_user_message(
        self,
        user_message: str,
        memory: SessionMemory,
        temperature: float = None,
        max_output_tokens: int = None,
    ) -> Tuple[str, int]:
        """
        Process one user turn and return the assistant reply.

        Args:
            user_message: Raw user input text.
            memory: Current session memory object.
            temperature: Optional temperature override.
            max_output_tokens: Optional token limit override.

        Returns:
            Tuple of (assistant_reply_str, estimated_total_tokens).
        """
        clean_message = sanitize_user_input(user_message)
        memory.add_message("user", clean_message)
        history_dicts = memory.to_dicts()

        messages = self.prompt_builder.build_messages(
            history=history_dicts,
            user_message=clean_message,
        )

        est_tokens_in = approximate_token_count([m["content"] for m in messages])
        logger.debug("Estimated input tokens: %s", est_tokens_in)

        assistant_reply = self.client.generate_chat_completion(
            messages=messages,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )

        memory.add_message("assistant", assistant_reply)

        est_tokens_out = approximate_token_count([assistant_reply])
        est_total = est_tokens_in + est_tokens_out
        logger.info("Message handled. Estimated total tokens: %s", est_total)

        return assistant_reply, est_total
