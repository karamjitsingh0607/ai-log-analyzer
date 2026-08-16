from app.services.log_analyzer import analyze_logs, detect_component

def test_analyze_logs():
    logs = [
        {
            "timestamp": "2026-08-13 11:00:01",
            "level": "INFO",
            "message": "Application started"
        },
        {
            "timestamp": "2026-08-13 11:00:03",
            "level": "ERROR",
            "message": "Database connection failed"
        },
        {
            "timestamp": "2026-08-13 11:00:04",
            "level": "ERROR",
            "message": "Connection refused: 10.10.20.15:5432"
        }
    ]

    result = analyze_logs(logs)

    assert result["total_entries"] == 3
    assert result["error_count"] == 2
    assert result["severity"] == "MEDIUM"
    assert result["component_detection"]["component"] == "DATABASE"

def test_detect_authentication_component():
    logs = [
        {
            "timestamp": "2026-08-13 11:00:01",
            "level": "ERROR",
            "message": "Invalid credentials"
        },
        {
            "timestamp": "2026-08-13 11:00:02",
            "level": "ERROR",
            "message": "Login failed"
        }
    ]

    result = detect_component(logs)

    assert result["component"] == "AUTHENTICATION"
    assert result["confidence"] == 1.0

def test_unknown_component():
    logs = [
        {
            "timestamp": "2026-08-13 11:00:01",
            "level": "INFO",
            "message": "Application started successfully"
        }
    ]

    result = detect_component(logs)

    assert result["component"] == "UNKNOWN"
    assert result["confidence"] == 0.0
    assert result["evidence"] == []

