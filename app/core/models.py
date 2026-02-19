# app/core/models.py
"""Gemini API client wrapper with structured request handling and fallback."""

import logging
from typing import List, Optional

from google import genai
from google.genai import types

from .config import Settings


logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Thin, testable wrapper around the Google Gen AI Python SDK.
    API key is read from GEMINI_API_KEY environment variable.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        # The SDK reads GEMINI_API_KEY from environment automatically.
        self.client = genai.Client()
        self.model_name = settings.model.model_name

    def generate_chat_completion(
        self,
        messages: List[dict],
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
    ) -> str:
        """
        Call Gemini and return the text response.

        Falls back to a safe error message on any exception so the UI
        is never broken by an API failure.
        """
        cfg = self.settings.model
        generation_config = types.GenerateContentConfig(
            temperature=temperature if temperature is not None else cfg.temperature,
            max_output_tokens=(
                max_output_tokens
                if max_output_tokens is not None
                else cfg.max_output_tokens
            ),
            top_p=cfg.top_p,
            top_k=cfg.top_k,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[m["content"] for m in messages],
                config=generation_config,
            )
            text = getattr(response, "text", "").strip()
            if not text:
                logger.warning("Empty response received from Gemini.")
                return (
                    "I could not generate a response right now. "
                    "Please try again in a moment."
                )
            return text

        except Exception as exc:  # noqa: BLE001
            logger.exception("Gemini API call failed: %s", exc)
            return (
                "I ran into an issue while generating your answer. "
                "Please try rephrasing your question or try again."
            )
