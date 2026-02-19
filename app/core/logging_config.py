# app/core/logging_config.py
"""Logging configuration setup using dictConfig from YAML file."""

import logging
import logging.config
from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
LOGGING_CONFIG_PATH = BASE_DIR / "config" / "logging.yaml"


def setup_logging() -> None:
    """
    Configure application-wide logging using dictConfig.
    Falls back to basicConfig if config file is missing.
    """
    if LOGGING_CONFIG_PATH.exists():
        with open(LOGGING_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        logging.config.dictConfig(cfg)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logging.getLogger(__name__).warning(
            "logging.yaml not found, using basicConfig."
        )
