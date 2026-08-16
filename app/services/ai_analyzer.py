import json
import logging
import ollama

from app.config import settings

from dotenv import load_dotenv
from app.schemas.log import AIAnalysis
from pydantic import ValidationError


load_dotenv()

logger = logging.getLogger(__name__)

def analyze_with_ai(parsed_logs):
    prompt = f"""
You are an expert production incident and log analysis assistant.

Analyze the following application logs.

Your job is to:
1. Identify the main problem.
2. Determine the most likely root cause.
3. Estimate severity.
4. Provide a confidence score between 0 and 1.
5. Identify possible causes.
6. Recommend practical troubleshooting actions.
7. Suggest next steps.

Rules:
- Base your analysis ONLY on the provided logs.
- Do not invent facts.
- If information is insufficient, clearly say so.
- Do not expose secrets or credentials.
- Return ONLY valid JSON.

Required JSON format:

{{
    "problem_summary": "string",
    "root_cause": "string",
    "severity": "LOW | MEDIUM | HIGH | CRITICAL",
    "confidence": 0.0,
    "possible_causes": [],
    "recommended_actions": [],
    "next_steps": []
}}

Logs: 

{parsed_logs}
"""
    try:
        response = ollama.chat(
            model=settings.ollama_model,
            messages= [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        ai_text = response.message.content
    except Exception as exc:
        logger.error("AI analyzer failed: %s", exc)

        raise RuntimeError(
            "AI analyzer is currently unavailable"
        ) from exc

    try:
        ai_data = json.loads(ai_text)

    except json.JSONDecodeError as exc:
        logger.error("AI returned invalid JSON: %s", exc)

        raise RuntimeError(
            "AI analyzer returned an invalid response"
        ) from exc
    try:
        validated_response = AIAnalysis.model_validate(ai_data)
    except ValidationError as exc:
        logger.error("AI response failed schema validation: %s", exc)
        raise RuntimeError(
        "AI analyzer returned an invalid response structure"
    ) from exc
    
    return validated_response