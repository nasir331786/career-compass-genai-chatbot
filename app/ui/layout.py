# app/ui/layout.py
"""
Streamlit UI layout module.
Provides premium dark-gradient chat UI with message bubbles,
fixed bottom input bar, typing indicator, and sidebar controls.
"""

import streamlit as st


def setup_page(app_name: str, domain_name: str) -> None:
    """Configure page settings and inject custom CSS for premium look."""
    st.set_page_config(
        page_title=f"{app_name} - {domain_name}",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ---- Global ---- */
    .stApp {
        background: radial-gradient(ellipse at top left, #0f1629 0%, #050b17 50%, #020408 100%);
        color: #e8eaf6;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .block-container { padding-top: 1rem !important; padding-bottom: 6rem !important; }

    /* ---- Header gradient text ---- */
    .app-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f64f59 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0;
        letter-spacing: -0.02em;
    }
    .app-header p {
        color: rgba(232,234,246,0.6);
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    /* ---- Chat container ---- */
    .chat-wrap { max-width: 860px; margin: 0 auto; padding: 0.5rem 0 2rem; }

    /* ---- Message rows ---- */
    .msg-row { display: flex; align-items: flex-start; gap: 0.6rem; margin-bottom: 1rem; }
    .msg-row.user-row { flex-direction: row-reverse; }

    /* ---- Avatars ---- */
    .avatar {
        width: 34px; height: 34px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 600;
        flex-shrink: 0; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .avatar.ai-av  { background: linear-gradient(135deg,#667eea,#764ba2); color:#fff; }
    .avatar.usr-av { background: linear-gradient(135deg,#11998e,#38ef7d); color:#fff; }

    /* ---- Bubbles ---- */
    .bubble {
        padding: 0.85rem 1.1rem;
        border-radius: 16px;
        max-width: 76%;
        line-height: 1.6;
        font-size: 0.93rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        animation: fadeUp 0.2s ease-out;
    }
    .ai-bubble {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(102,126,234,0.2);
        backdrop-filter: blur(20px);
        border-radius: 4px 16px 16px 16px;
    }
    .usr-bubble {
        background: linear-gradient(135deg,#667eea,#764ba2);
        border-radius: 16px 4px 16px 16px;
        color: #fff;
    }

    /* ---- Labels ---- */
    .msg-label { font-size: 0.72rem; opacity: 0.55; margin-bottom: 0.25rem; font-weight: 500; }

    /* ---- Typing animation ---- */
    .dot { display:inline-block; width:7px; height:7px; border-radius:50%;
           background:#667eea; margin:0 2px;
           animation: bounce 1s ease infinite alternate; }
    .dot:nth-child(2){animation-delay:.2s}
    .dot:nth-child(3){animation-delay:.4s}
    @keyframes bounce { to{transform:translateY(-6px);opacity:.4} }
    @keyframes fadeUp { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

    /* ---- Bottom input area ---- */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 0 !important;
        left: 0; right: 0;
        background: linear-gradient(180deg,rgba(5,11,23,0.85),rgba(2,4,8,0.98)) !important;
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(102,126,234,0.12);
        padding: 0.75rem 1rem 1rem;
        z-index: 999;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#080e1f,#04060e);
        border-right: 1px solid rgba(102,126,234,0.1);
    }
    section[data-testid="stSidebar"] .stSlider > div > div { background: #667eea !important; }

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(102,126,234,0.35); border-radius: 10px; }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(
        f'<div class="app-header"><h1>🧠 {app_name}</h1>'
        f'<p>Intelligent {domain_name} assistant powered by Gemini 2.5</p></div>',
        unsafe_allow_html=True,
    )


def render_sidebar(settings) -> dict:
    """
    Render the sidebar with runtime controls.
    Returns dict of overrides: {temperature, max_output_tokens}.
    """
    overrides = {}
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        st.caption("Tune the assistant in real time.")
        overrides["temperature"] = st.slider(
            "🌡️ Creativity",
            0.0, 1.0,
            float(settings.model.temperature),
            0.05,
            help="Higher = more creative, lower = more focused.",
        )
        overrides["max_output_tokens"] = st.slider(
            "📝 Max tokens",
            256, 2048,
            int(settings.model.max_output_tokens),
            128,
            help="Maximum length of each response.",
        )
        st.divider()
        st.markdown("## 💬 Session")
        if st.button("🔄 Start fresh", use_container_width=True):
            st.session_state["memory"].clear()
            st.session_state["chat_tokens"] = 0
            st.rerun()
        total = st.session_state.get("chat_tokens", 0)
        st.caption(f"∼ {total:,} tokens used this session.")
        st.divider()
        st.markdown("## ℹ️ About")
        st.caption(
            f"📁 Domain: **{settings.app.domain_name}**\n\n"
            f"🤖 Model: `{settings.model.model_name}`\n\n"
            "Built with Google Gemini + Streamlit."
        )
    return overrides


def render_chat_history(memory) -> None:
    """Render all stored chat messages as styled bubbles."""
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in memory.messages:
        is_user = msg.role == "user"
        row_class  = "user-row" if is_user else ""
        av_class   = "usr-av" if is_user else "ai-av"
        av_label   = "You" if is_user else "AI"
        bub_class  = "usr-bubble" if is_user else "ai-bubble"
        label_text = "You" if is_user else "🧠 Career Advisor"

        # Escape HTML in user content minimally
        safe_content = msg.content.replace("<", "&lt;").replace(">", "&gt;")

        st.markdown(
            f"""
            <div class="msg-row {row_class}">
              <div class="avatar {av_class}">{av_label}</div>
              <div>
                <div class="msg-label">{label_text}</div>
                <div class="bubble {bub_class}">{safe_content}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_typing_indicator() -> None:
    """Show animated typing dots while waiting for Gemini."""
    st.markdown(
        '<div class="chat-wrap"><div class="msg-row">'
        '<div class="avatar ai-av">AI</div>'
        '<div><div class="msg-label">🧠 Career Advisor</div>'
        '<div class="bubble ai-bubble">'
        '<span class="dot"></span><span class="dot"></span><span class="dot"></span>'
        '</div></div></div></div>',
        unsafe_allow_html=True,
    )


def chat_input() -> str:
    """Render the bottom-fixed chat input box."""
    return st.chat_input(
        "Ask anything about your career, skills, resume, or interview prep..."
    )
