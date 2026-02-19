# app/core/config.py
"""Configuration loader: reads app_config.yaml and environment variables."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import os

import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "config" / "app_config.yaml"


@dataclass
class PromptSettings:
    system_role: str
    domain_description: str
    response_style: str
    safety_instructions: str
    output_format: str


@dataclass
class ModelSettings:
    model_name: str
    temperature: float
    max_output_tokens: int
    top_p: float
    top_k: int


@dataclass
class AppSettings:
    app_name: str
    domain_name: str
    allowed_origins: List[str]
    enable_telemetry: bool
    environment: str  # "local" | "staging" | "production"


@dataclass
class Settings:
    prompts: PromptSettings
    model: ModelSettings
    app: AppSettings
    gemini_api_key: Optional[str] = None


def load_yaml_config(path: Path) -> dict:
    """Load and parse a YAML configuration file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_settings() -> Settings:
    """Load full application settings from YAML + environment."""
    cfg = load_yaml_config(CONFIG_PATH)

    prompts_cfg = cfg["prompts"]
    model_cfg = cfg["model"]
    app_cfg = cfg["app"]

    settings = Settings(
        prompts=PromptSettings(
            system_role=prompts_cfg["system_role"],
            domain_description=prompts_cfg["domain_description"],
            response_style=prompts_cfg["response_style"],
            safety_instructions=prompts_cfg["safety_instructions"],
            output_format=prompts_cfg["output_format"],
        ),
        model=ModelSettings(
            model_name=model_cfg["model_name"],
            temperature=model_cfg["temperature"],
            max_output_tokens=model_cfg["max_output_tokens"],
            top_p=model_cfg["top_p"],
            top_k=model_cfg["top_k"],
        ),
        app=AppSettings(
            app_name=app_cfg["app_name"],
            domain_name=app_cfg["domain_name"],
            allowed_origins=app_cfg.get("allowed_origins", []),
            enable_telemetry=app_cfg.get("enable_telemetry", False),
            environment=app_cfg.get("environment", "local"),
        ),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
    )

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Configure it before running the application."
        )

    return settings
