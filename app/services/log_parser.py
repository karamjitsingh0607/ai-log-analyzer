import re

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+ \S+)\s+"
    r"(?P<level>INFO|WARNING|ERROR|DEBUG|CRITICAL)\s+"
    r"(?P<message>.*)$"
)

def parse_log_line(line: str):
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    return {
        "timestamp" : match.group("timestamp"),
        "level" : match.group("level"),
        "message" :  match.group("message")
    }

def parse_logs(log_text: str):
    parsed_logs = []

    for line in log_text.splitlines():
        parsed_line = parse_log_line(line)

        if parsed_line:
            parsed_logs.append(parsed_line)

    return parsed_logs