from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum

class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class TopError(BaseModel):
    message: str
    occurrences: int

class ComponentDetection(BaseModel):
    component: str
    confidence: float
    evidence: List[str]

class RuleBasedAnalysis(BaseModel):
    total_entries: int
    level_counts: Dict[str, int]
    severity: str
    severity_score: int
    component_detection: ComponentDetection
    error_count: int
    top_errors: List[TopError]


class AIAnalysis(BaseModel):
    problem_summary: str
    root_cause: str
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    possible_causes: List[str]
    recommended_actions: List[str]
    next_steps: List[str]


class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str


class LogAnalysisResponse(BaseModel):
    filename: str
    analysis: RuleBasedAnalysis
    ai_analysis: AIAnalysis
    logs: List[LogEntry]

