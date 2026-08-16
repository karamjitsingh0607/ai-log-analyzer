import logging
from fastapi.testclient import TestClient

from app.main import app
from app.api.logs import analyze_with_ai

client = TestClient(app)

def test_analyze_valid_log(monkeypatch):
    def mock_ai_analysis(parsed_logs):
        return {
            "problem_summary": "Database connection failed",
            "root_cause": "Connection refused",
            "severity": "HIGH",
            "confidence": 0.9,
            "possible_causes": [
                "Database server unavailable"
            ],
            "recommended_actions": [
                "Check database connectivity"
            ],
            "next_steps": [
                "Check database server status"
            ]
        }
    monkeypatch.setattr(
        "app.api.logs.analyze_with_ai",
        mock_ai_analysis
    )

    log_content = """\
        2026-08-13 11:00:01 INFO Application started
        2026-08-13 11:00:03 INFO Connecting to database
        2026-08-13 11:00:04 ERROR Database connection failed
        2026-08-13 11:00:05 ERROR Connection refused: 10.10.20.15:5432
    """

    response = client.post(
        "/logs/analyze",
        files= {
            "file" : (
                "sample.log",
                log_content,
                "text/plain"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["filename"] == "sample.log"
    assert data["analysis"]["total_entries"] == 4
    assert data["analysis"]["error_count"] == 2
    assert data["analysis"]["component_detection"]["component"] == "DATABASE"

    assert data["ai_analysis"]["severity"] == "HIGH"
    assert data["ai_analysis"]["confidence"] == 0.9

def test_reject_non_log_file():

    response = client.post(
            "/logs/analyze",
            files= {
                "file" : (
                    "sample.txt",
                    "some log content",
                    "text/plain"
                )
            }
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only .log files are supported"


def test_reject_empty_file():
    response = client.post(
        "/logs/analyze",
        files= {
            "file" : (
                "empty.log",
                "",
                "text/plain"
            )
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded log file is empty"

def test_reject_invalid_log():
    response = client.post(
        "/logs/analyze",
        files= {
            "file" : (
                "invalid.log",
                "This is not a valid log line",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No valid log entries found"


def test_ai_analyzer_unavailable(monkeypatch):
    def mock_ai_analysis(parsed_logs):
        raise RuntimeError(
            "AI analyzer is currently unavailable"
        )
    monkeypatch.setattr(
        "app.api.logs.analyze_with_ai",
        mock_ai_analysis
    )
    log_content = """\
    2026-08-13 11:00:01 INFO Application started
    2026-08-13 11:00:04 ERROR Database connection failed
    """

    response = client.post(
        "/logs/analyze",
        files={
            "file": (
                "sample.log",
                log_content,
                "text/plain"
            )
        }
    )
    assert response.status_code == 503
    assert response.json()["detail"] == (
        "AI analyzer is currently unavailable"
    )

def test_log_analysis_logging(monkeypatch, caplog):
    def mock_ai_analysis(parsed_logs):
        return {
            "problem_summary": "Database connection failed",
            "root_cause": "Connection refused",
            "severity": "HIGH",
            "confidence": 0.9,
            "possible_causes": [
                "Database server unavailable"
            ],
            "recommended_actions": [
                "Check database connectivity"
            ],
            "next_steps": [
                "Check database server status"
            ]
        }
    monkeypatch.setattr(
        "app.api.logs.analyze_with_ai",
        mock_ai_analysis
    )
    log_content = """\
        2026-08-13 11:00:01 INFO Application started
        2026-08-13 11:00:03 INFO Connecting to database
        2026-08-13 11:00:04 ERROR Database connection failed
    """
    with caplog.at_level(logging.INFO):
        response = client.post(
            "/logs/analyze",
            files={
                "file": (
                    "sample.log",
                    log_content,
                    "text/plain"
                )
            }
        )
    assert response.status_code == 200
    assert "Log analysis started" in caplog.text
    assert "Logs parsed successfully" in caplog.text
    assert "Log analysis completed" in caplog.text
