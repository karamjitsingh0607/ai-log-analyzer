from app.services.log_parser import parse_log_line, parse_logs


def test_parse_valid_log_line():

    line = "2026-08-13 11:00:04 ERROR Invalid credentials"

    result = parse_log_line(line)

    assert result is not None
    assert result["timestamp"] == "2026-08-13 11:00:04"
    assert result["level"] == "ERROR"
    assert result["message"] == "Invalid credentials"


def test_parse_invalid_log_line():

    line = "This is not a valid log line"

    result = parse_log_line(line)

    assert result is None


def test_parse_multiple_logs():

    log_text = """\
2026-08-13 11:00:01 INFO Application started
2026-08-13 11:00:04 ERROR Invalid credentials
2026-08-13 11:00:05 WARNING Authentication retry
"""

    result = parse_logs(log_text)

    assert len(result) == 3
    assert result[0]["level"] == "INFO"
    assert result[1]["level"] == "ERROR"
    assert result[2]["level"] == "WARNING"