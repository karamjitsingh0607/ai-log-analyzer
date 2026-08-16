from collections import Counter

def detect_component(parsed_logs):
    # text = "".join(
    #     log["message"].lower()
    #     for log in parsed_logs
    # )
    component_keywords = {
        "DATABASE": [
            "database",
            "sql",
            "postgres",
            "mysql",
            "oracle",
            "5432",
            "3306"
        ],
        "NETWORK": [
            "network",
            "connection refused",
            "timeout",
            "unreachable",
            "dns",
            "socket"
        ],
        "AUTHENTICATION": [
            "authentication",
            "unauthorized",
            "permission denied",
            "invalid credentials",
            "login failed"
        ],
        "STORAGE": [
            "disk",
            "storage",
            "filesystem",
            "file system",
            "no space left"
        ],
        "MEMORY": [
            "out of memory",
            "memory",
            "oom",
            "heap"
        ],
        "CPU": [
            "cpu",
            "high cpu",
            "processor"
        ]
    }
    component_scores = Counter()
    component_evidence = {}
    for log in parsed_logs:
        message = log["message"]
        message_lower = message.lower()

        for component, keywords in component_keywords.items():
            matched_keyword = [
                keyword
                for keyword in keywords
                if keyword in message_lower
            ]

            if matched_keyword:
                component_scores[component] += len(matched_keyword)

                component_evidence.setdefault(
                    component,[]
                ).append(message)
    if not component_scores:
        return {
            "component": "UNKNOWN",
            "confidence": 0.0,
            "evidence": []
        }
    component, score = component_scores.most_common(1)[0]

    total_score = sum(component_scores.values())

    confidence = round(
        score/total_score,
        2
    ) 
    return {
        "component": component,
        "confidence": confidence,
        "evidence": component_evidence[component]
    }

def analyze_logs(parsed_logs):
    level_counts = Counter(
        log["level"] for log in parsed_logs
    )
    component_detection = detect_component(parsed_logs)
    error_messages = [
        log["message"]
        for log in parsed_logs
        if log["level"] in {"ERROR", "CRITICAL"}
    ]

    error_counts = Counter(error_messages)

    # -------------------------
    # Severity scoring
    # -------------------------

    severity_score = 0

    # Critical logs
    severity_score += level_counts["CRITICAL"] * 5

    # Error logs
    severity_score += level_counts["ERROR"] * 2

    # Warning logs
    severity_score += level_counts["WARNING"] * 1

    # Repeated errors
    repeated_errors = sum(
        count - 1
        for count in error_counts.values()
        if count > 1
    )

    severity_score += repeated_errors * 2

    # -------------------------
    # Determine severity
    # -------------------------

    if level_counts["CRITICAL"] > 0 or severity_score >= 8:
        severity = "CRITICAL"
    elif severity_score >= 5:
        severity = "HIGH"
    elif severity_score >= 2:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "total_entries": len(parsed_logs),
        "level_counts": dict(level_counts),
        "severity": severity,
        "severity_score": severity_score,
        "component_detection": component_detection,
        "error_count": len(error_messages),
        "top_errors": [
            {
                "message": message,
                "occurrences": count
            }
            for message, count in error_counts.most_common(5)
        ]
    }