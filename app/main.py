from fastapi import FastAPI

from app.api.logs import router as logs_router
from app.services.ollama_service import check_ollama_health

app = FastAPI(
    title="AI Log Analyzer",
    description="AI-powered log analysis and troubleshooting API",
    version="1.0.0"
)

app.include_router(router=logs_router)

@app.get("/health")
def health_check():
    ollama_available = check_ollama_health()
    return {
        "status": "healthy" if ollama_available else "degraded",
        "service": "AI Log Analyzer",
        "ollama": {
            "status": "available" if ollama_available else "unavailable"
        }
    }
