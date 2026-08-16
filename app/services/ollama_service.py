import ollama

from app.config import settings


def get_ollama_client():
    return ollama.Client(
        host=settings.ollama_host
    )


def check_ollama_health() -> bool:
    try:
        client = get_ollama_client()
        client.list()
        return True
    except Exception:
        return False