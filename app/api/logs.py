from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.log_parser import parse_logs
from app.services.log_analyzer import analyze_logs
from app.services.ai_analyzer import analyze_with_ai
from app.schemas.log import LogAnalysisResponse

router = APIRouter(
    prefix='/logs',
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
        raise HTTPException(
            status_code=400,
            detail="Only .log files are supported"
        )

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded log file is empty"
            )
        log_text = content.decode("utf-8")

        parsed_logs = parse_logs(log_text)

        if not parsed_logs:
            raise HTTPException(
                status_code=400,
                detail="No valid log entries found"
            )

        analysis = analyze_logs(parsed_logs)

        try:
            ai_analysis = analyze_with_ai(parsed_logs)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=503,
                detail=str(exc)
            ) from exc

        return {
            "filename": file.filename,
            "analysis": analysis,
            "ai_analysis": ai_analysis,
            "logs": parsed_logs
        }
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Log file must be UTF-8 encoded"
        )
