# Career Compass - Production-Ready GenAI Career Advisor Chatbot

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-red.svg)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-green.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **production-ready, domain-specific AI chatbot** built with Google Gemini 2.5 Flash and Streamlit. Features a premium dark-gradient UI, multi-turn conversation memory, advanced prompt engineering, and one-command AWS EC2 deployment.

---

## Architecture

```
User
  └─> Streamlit UI (app/ui/)
         └─> ChatService (app/services/)
                ├─> PromptBuilder (app/core/prompts.py)
                ├─> SessionMemory (app/core/memory.py)
                └─> GeminiClient (app/core/models.py)
                       └─> Google Gemini API
```

### Layer Responsibilities

| Layer | Location | Responsibility |
|-------|----------|----------------|
| UI | `app/ui/` | Layout, chat bubbles, sidebar, typing indicator |
| Core | `app/core/` | Config, logging, prompts, memory, Gemini client |
| Services | `app/services/` | Chat orchestration, token estimation, sanitization |
| Config | `config/` | Domain YAML config, logging dictConfig |
| Scripts | `scripts/` | Local dev startup |

---

## Features

- **Google Gemini 2.5 Flash** integration via official `google-genai` SDK
- **Multi-turn conversation memory** with automatic trimming
- **Advanced prompt engineering** - domain-specific system prompts, safety instructions, markdown output
- **Config-driven design** - switch domain by editing `config/app_config.yaml`
- **Premium Streamlit UI** - dark gradient, animated chat bubbles, typing indicator, fixed input bar
- **Structured logging** - rotating file + console with YAML dictConfig
- **AWS EC2 ready** - see `DEPLOYMENT_AWS_EC2.md`

---

## Quick Start (Local)

### 1. Clone
```bash
git clone https://github.com/nasir331786/career-compass-genai-chatbot.git
cd career-compass-genai-chatbot
```

### 2. Virtual environment
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY
```
Get your API key at: https://aistudio.google.com/app/apikey

### 5. Run
```bash
bash scripts/run_local.sh
# OR
streamlit run app/main.py
```

Open http://localhost:8501

---

## Changing the Domain

To adapt Career Compass for any other domain (e.g., legal Q&A, mental health, interview coach):

1. Open `config/app_config.yaml`
2. Update:
   - `app.app_name`
   - `app.domain_name`
   - All `prompts.*` fields
3. Restart the app. No Python code changes required.

---

## Project Structure

```
career-compass-genai-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Streamlit entrypoint
│   ├── ui/
│   │   ├── __init__.py
│   │   └── layout.py            # UI components
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Settings loader
│   │   ├── logging_config.py    # Logging setup
│   │   ├── prompts.py           # Prompt engineering
│   │   ├── memory.py            # Session memory
│   │   └── models.py            # Gemini client
│   └── services/
│       ├── __init__.py
│       ├── chat_service.py      # Orchestrator
│       └── utils.py             # Helpers
├── config/
│   ├── app_config.yaml          # Domain config
│   └── logging.yaml             # Logging config
├── scripts/
│   └── run_local.sh             # Startup script
├── .env.example
├── .gitignore
├── LICENSE
├── requirements.txt
├── README.md
└── DEPLOYMENT_AWS_EC2.md
```

---

## Deployment

See **[DEPLOYMENT_AWS_EC2.md](DEPLOYMENT_AWS_EC2.md)** for the complete step-by-step AWS EC2 deployment guide.

---

## Future Improvements

- RAG with resume/job description upload (PDF + vector DB)
- User authentication (Auth0 / AWS Cognito)
- Persistent conversation history (PostgreSQL / DynamoDB)
- Multi-model fallback routing
- Admin dashboard for prompt management
- Docker + ECS/Fargate deployment
- CI/CD pipeline with GitHub Actions

---

## License

MIT License - see [LICENSE](LICENSE)

---

> Built by [nasir331786](https://github.com/nasir331786) as part of a production GenAI portfolio project.
