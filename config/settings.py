"""
Configuration settings for the SauceDemo E2E Automation Suite.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    BASE_URL: str = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com")
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT_MS", "10000"))
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    BROWSER: str = os.getenv("BROWSER", "chromium")
    
    # Standard credentials
    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_OUT_USER: str = os.getenv("LOCKED_OUT_USER", "locked_out_user")
    PROBLEM_USER: str = os.getenv("PROBLEM_USER", "problem_user")
    PERF_GLITCH_USER: str = os.getenv("PERF_GLITCH_USER", "performance_glitch_user")
    DEFAULT_PASSWORD: str = os.getenv("DEFAULT_PASSWORD", "secret_sauce")

settings = Settings()
