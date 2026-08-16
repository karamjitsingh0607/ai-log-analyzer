import logging

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.log_parser import parse_logs
from app.services.log_analyzer import analyze_logs
from app.services.ai_analyzer import analyze_with_ai
from app.schemas.log import LogAnalysisResponse


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


@router.post(
    "/analyze",
    response_model=LogAnalysisResponse
)
async def analyze_log(file: UploadFile = File(...)):

    if not file:
        raise HTTPException(
            status_code=400,
            detail="File name is required"
        )

    if not file.filename.endswith(".log"):
        logger.warning(
            "Rejected file | filename=%s | reason=invalid_extension",
            file.filename
        )

        raise HTTPException(
            status_code=400,
            detail="Only .log files are supported"
        )

    logger.info(
        "Log analysis started | filename=%s",
        file.filename
    )

    try:
        content = await file.read()

        if not content:
            logger.warning(
                "Rejected empty log file | filename=%s",
                file.filename
            )

            raise HTTPException(
                status_code=400,
                detail="Uploaded log file is empty"
            )

        log_text = content.decode("utf-8")

        parsed_logs = parse_logs(log_text)

        if not parsed_logs:
            logger.warning(
                "No valid log entries | filename=%s",
                file.filename
            )

            raise HTTPException(
                status_code=400,
                detail="No valid log entries found"
            )

        logger.info(
            "Logs parsed successfully | filename=%s | entries=%d",
            file.filename,
            len(parsed_logs)
        )

        analysis = analyze_logs(parsed_logs)

        try:
            ai_analysis = analyze_with_ai(parsed_logs)

        except RuntimeError as exc:
            logger.error(
                "AI analysis failed | filename=%s | error=%s",
                file.filename,
                exc
            )

            raise HTTPException(
                status_code=503,
                detail=str(exc)
            ) from exc

        logger.info(
            "Log analysis completed | filename=%s",
            file.filename
        )

        return {
            "filename": file.filename,
            "analysis": analysis,
            "ai_analysis": ai_analysis,
            "logs": parsed_logs
        }

    except UnicodeDecodeError:
        logger.warning(
            "Invalid encoding | filename=%s",
            file.filename
        )

        raise HTTPException(
            status_code=400,
            detail="Log file must be UTF-8 encoded"
        )