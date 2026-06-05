from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # ── DeepSeek V3 (LLM) ──────────────────────────────
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # ── Server ──────────────────────────────────────────
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_port: int = 3000

    # ── Database ────────────────────────────────────────
    database_url: str = "sqlite:///./data/max_coach.db"
    chroma_persist_dir: str = "./data/chroma"

    # ── Memory ──────────────────────────────────────────
    max_conversation_history: int = 50
    memory_retrieval_count: int = 5

    # ── Voice ───────────────────────────────────────────
    voice_speed: float = 1.0
    voice_volume: float = 1.0

    # ── Learning ────────────────────────────────────────
    correction_frequency: str = "moderate"
    default_learning_mode: str = "free_conversation"

    # ── Prompts ─────────────────────────────────────────
    prompts_dir: str = "./app/prompts"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
