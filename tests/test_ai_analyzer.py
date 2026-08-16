from app.services.ai_analyzer import analyze_with_ai
import pytest

class MockMessage:
    def __init__(self, content):
        self.content = content


class MockResponse:
    def __init__(self, content):
        self.message = MockMessage(content)


def test_ai_analyzer_valid_response(monkeypatch):
    valid_json = """
    {
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
    """
    def mock_ollama_chat(*args, **kwargs):
        return MockResponse(valid_json)
    monkeypatch.setattr(
        "app.services.ai_analyzer.ollama.chat",
        mock_ollama_chat
    )

    logs = [
        {
            "timestamp": "2026-08-13 11:00:04",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]
    result = analyze_with_ai(logs)

    assert result.problem_summary == "Database connection failed"
    assert result.root_cause == "Connection refused"
    assert result.severity.value == "HIGH"
    assert result.confidence == 0.9
    assert len(result.possible_causes) == 1

def test_ai_analyzer_invalid_json(monkeypatch):

    mock_response = {
        "message" : {
            "content" : "This is not valid JSON"
        }
    }
    def mock_ollama_chat(*args, **kwargs):
        return MockResponse("This is not valid JSON")

    monkeypatch.setattr(
        "app.services.ai_analyzer.ollama.chat",
        mock_ollama_chat
    )

    logs = [
        {
            "timestamp": "2026-08-13 11:00:04",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]

    with pytest.raises(RuntimeError,match= "invalid response"):
        analyze_with_ai(logs)

def test_ai_analyzer_ollama_failure(monkeypatch):
    def mock_ollama_chat(*args, **kwargs):
        raise Exception("Ollama server unavailable")
    monkeypatch.setattr(
        "app.services.ai_analyzer.ollama.chat",
        mock_ollama_chat
    )

    logs = [
        {
            "timestamp": "2026-08-13 11:00:04",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]

    with pytest.raises(RuntimeError, match="currently unavailable"):
        analyze_with_ai(logs)

def test_ai_analyzer_missing_field(monkeypatch):
    invalid_json = """
    {
        "problem_summary": "Database connection failed",
        "root_cause": "Connection refused",
        "severity": "HIGH",
        "confidence": 0.9,
        "possible_causes": [
            "Database server unavailable"
        ],
        "recommended_actions": [
            "Check database connectivity"
        ]
    }
    """
    def mock_ollama_chat(*args, **kwargs):
        return MockResponse(invalid_json)

    monkeypatch.setattr(
        "app.services.ai_analyzer.ollama.chat",
        mock_ollama_chat
    )

    logs = [
        {
            "timestamp": "2026-08-13 11:00:04",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]

    with pytest.raises(RuntimeError, match="invalid response structure"):
        analyze_with_ai(logs)

def test_ai_analyzer_invalid_severity(monkeypatch):
    invalid_json = """
    {
        "problem_summary": "Database connection failed",
        "root_cause": "Connection refused",
        "severity": "BANANA",
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
    """

    def mock_ollama_chat(*args, **kwargs):
        return MockResponse(invalid_json)

    monkeypatch.setattr(
        "app.services.ai_analyzer.ollama.chat",
        mock_ollama_chat
    )

    logs = [
        {
            "timestamp": "2026-08-13 11:00:04",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]

    with pytest.raises(RuntimeError, match="invalid response structure"):
        analyze_with_ai(logs)

def test_ai_analyzer_invalid_confidence(monkeypatch):
    invalid_json = """
    {
        "problem_summary": "Database connection failed",
        "root_cause": "Connection refused",
        "severity": "HIGH",
        "confidence": 1.5,
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
    """
    def mock_ollama_chat(*args, **kwargs):
        return MockResponse(invalid_json)

    monkeypatch.setattr(
        "app.services.ai_analyzer.ollama.chat",
        mock_ollama_chat
    )

    logs = [
        {
            "timestamp": "2026-08-13 11:00:04",
            "level": "ERROR",
            "message": "Database connection failed"
        }
    ]

    with pytest.raises(
        RuntimeError,
        match="invalid response structure"
    ):
        analyze_with_ai(logs)
        