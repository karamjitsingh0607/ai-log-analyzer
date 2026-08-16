import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.logs import router as logs_router
from app.services.ollama_service import check_ollama_health
from app.utils.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Log Analyzer",
    description="AI-powered log analysis and troubleshooting API",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception | method=%s | path=%s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
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
