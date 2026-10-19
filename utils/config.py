"""
Centralized Configuration Loader for AI-QA-Suite.

Loads settings from environment variables and .env file with safe defaults.
Zero hardcoding of secrets.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Project Root Directory
ROOT_DIR = Path(__file__).parent.parent.resolve()

# Load .env if present
load_dotenv(dotenv_path=ROOT_DIR / ".env")


@dataclass(frozen=True)
class Config:
    """Application and test execution configuration settings."""

    # Project paths
    root_dir: Path = ROOT_DIR
    logs_dir: Path = ROOT_DIR / "logs"
    reports_dir: Path = ROOT_DIR / "reports"
    test_data_dir: Path = ROOT_DIR / "test_data"

    # Environments & Endpoints
    environment: str = os.getenv("ENVIRONMENT", "local")
    base_url: str = os.getenv("BASE_URL", "http://127.0.0.1:8765")
    api_base_url: str = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    # UI / Browser Settings
    browser: str = os.getenv("BROWSER", "chromium").lower()
    headless: bool = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    timeout: int = int(os.getenv("TIMEOUT", "15000"))
    slow_mo: int = int(os.getenv("SLOW_MO", "0"))
    screenshot_on_failure: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() in ("true", "1", "yes")

    # AI Provider Settings
    ai_provider: str = os.getenv("AI_PROVIDER", "mock").lower()
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()


# Global Singleton instance
config = Config()

# Ensure runtime directories exist
config.logs_dir.mkdir(parents=True, exist_ok=True)
config.reports_dir.mkdir(parents=True, exist_ok=True)
