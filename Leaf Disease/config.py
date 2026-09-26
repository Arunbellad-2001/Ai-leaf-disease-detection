import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AppConfig:
    """
    Centralized configuration for the Leaf Disease Detection System.

    Loads sensitive information and dynamic settings from environment variables,
    providing a single source of truth for application configuration.
    """
    # --- API Credentials ---
    # NEW: Switched from GROQ to GEMINI
    gemini_api_key: str = os.environ.get("GEMINI_API_KEY", "")

    # --- AI Model Settings ---
    # NEW: Updated Model Name
    model_name: str = "gemini-2.5-flash"
    model_temperature: float = 0.3
    max_completion_tokens: int = 1024 # Maximum tokens in model responses

    @classmethod
    def from_env(cls):
        """Creates an instance of AppConfig populated with environment variables."""
        return cls()