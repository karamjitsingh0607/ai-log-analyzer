from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Log Analyzer"
    app_version: str = "1.0.0"
    ollama_model: str = "llama3.2"
    ollama_host: str = "http://localhost:11434"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
