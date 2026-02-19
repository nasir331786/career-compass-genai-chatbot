# app/main.py
"""
Streamlit application entrypoint.
Orchestrates UI, session state, and ChatService.
"""

import logging

import streamlit as st

from app.core.config import load_settings
from app.core.logging_config import setup_logging
from app.core.memory import SessionMemory
from app.services.chat_service import ChatService
from app.ui.layout import (
    setup_page,
    render_sidebar,
    render_chat_history,
    render_typing_indicator,
    chat_input,
)


def init_session_state() -> None:
    """Initialize Streamlit session state on first run."""
    if "memory" not in st.session_state:
        st.session_state["memory"] = SessionMemory()
    if "chat_tokens" not in st.session_state:
        st.session_state["chat_tokens"] = 0
    if "settings" not in st.session_state:
        st.session_state["settings"] = load_settings()
    if "chat_service" not in st.session_state:
        st.session_state["chat_service"] = ChatService(
            settings=st.session_state["settings"]
        )


def main() -> None:
    """Application entrypoint."""
    setup_logging()
    logger = logging.getLogger("app.main")

    init_session_state()
    settings = st.session_state["settings"]
    chat_service: ChatService = st.session_state["chat_service"]
    memory: SessionMemory = st.session_state["memory"]

    # --- UI setup ---
    setup_page(
        app_name=settings.app.app_name,
        domain_name=settings.app.domain_name,
    )
    overrides = render_sidebar(settings=settings)

    # --- Chat history ---
    render_chat_history(memory=memory)

    # --- Input & response ---
    user_prompt = chat_input()

    if user_prompt:
        with st.spinner(""):
            render_typing_indicator()
            reply, est_tokens = chat_service.handle_user_message(
                user_message=user_prompt,
                memory=memory,
                temperature=overrides.get("temperature"),
                max_output_tokens=overrides.get("max_output_tokens"),
            )
            st.session_state["chat_tokens"] += est_tokens
            logger.info("Message processed. tokens=%s", est_tokens)
            st.rerun()


if __name__ == "__main__":
    main()
