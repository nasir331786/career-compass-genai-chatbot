# app/services/utils.py
"""Helper utilities: token estimation and input validation."""

from typing import List


def approximate_token_count(texts: List[str]) -> int:
    """
    Rough heuristic to estimate token count for cost awareness.
    For English text, ~4 characters approximate 1 token.

    Args:
        texts: List of text strings to count.

    Returns:
        Estimated total token count.
    """
    char_count = sum(len(t) for t in texts)
    return char_count // 4


def sanitize_user_input(text: str, max_length: int = 2000) -> str:
    """
    Basic sanitization: strip whitespace and truncate to max_length.

    Args:
        text: Raw user input string.
        max_length: Maximum allowed characters.

    Returns:
        Sanitized string.
    """
    return text.strip()[:max_length]
