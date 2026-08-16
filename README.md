# AI Log Analyzer

[![Tests](https://github.com/karamjitsingh0607/ai-log-analyzer/actions/workflows/tests.yml/badge.svg)](https://github.com/karamjitsingh0607/ai-log-analyzer/actions/workflows/tests.yml)

An AI-powered log analysis backend built with **Python, FastAPI, Ollama, and Pydantic**.

The application analyzes application logs using a combination of deterministic rule-based analysis and local LLM-powered analysis. It identifies errors, detects the affected system component, calculates severity, and generates AI-assisted root-cause analysis and troubleshooting recommendations.

## Features

- Upload and analyze `.log` files
- Parse structured application logs
- Rule-based error and severity analysis
- Automatic component detection
  - Database
  - Network
  - Authentication
  - Storage
  - Memory
  - CPU
- AI-powered incident analysis using local Ollama
- Structured AI responses with Pydantic validation
- AI confidence scoring
- Root-cause analysis
- Recommended troubleshooting actions
- Next-step recommendations
- Ollama health check
- Comprehensive automated tests
- Docker support
- Local AI processing without external AI APIs

## Architecture

```text
                    ┌─────────────────────┐
                    │       Client        │
                    │   curl / Postman    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      REST API       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Log Parser      │
                    │                     │
                    │  Timestamp parsing  │
                    │  Level parsing      │
                    │  Message parsing    │
                    └──────────┬──────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │   Rule-Based Analyzer   │
                  │                         │
                  │  Component detection    │
                  │  Error analysis         │
                  │  Severity scoring       │
                  └──────────┬──────────────┘
                             │
                             ▼
                  ┌─────────────────────────┐
                  │      AI Analyzer        │
                  │                         │
                  │  Ollama + Llama 3.2    │
                  │  Root cause analysis    │
                  │  Recommendations       │
                  └──────────┬──────────────┘
                             │
                             ▼
                  ┌─────────────────────────┐
                  │   Pydantic Validation   │
                  │                         │
                  │  Structured AI response │
                  └──────────┬──────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │    JSON Response    │
                    └─────────────────────┘

```
## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- Ollama
- Llama 3.2
- Pytest
- Docker
- Uvicorn

## Project Structure

```text
ai-log-analyzer/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── logs.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── log.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_analyzer.py
│   │   ├── log_analyzer.py
│   │   ├── log_parser.py
│   │   └── ollama_service.py
│   │
│   ├── __init__.py
│   ├── config.py
│   └── main.py
│
├── logs/
│   ├── authentication_error.log
│   ├── empty.log
│   ├── healthy.log
│   ├── network_error.log
│   ├── sample.log
│   ├── storage_error.log
│   └── test.txt
│
├── tests/
│   ├── test_ai_analyzer.py
│   ├── test_health.py
│   ├── test_log_analyzer.py
│   ├── test_log_parser.py
│   └── test_logs_api.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## How It Works

The application performs two types of analysis.

### 1. Rule-Based Analysis

The uploaded logs are parsed and analyzed using deterministic rules.

The analyzer:

- Counts log levels
- Counts errors and critical events
- Detects repeated errors
- Detects the most likely system component
- Calculates a severity score
- Determines overall severity
- Extracts the most frequent errors

Supported components include:

- Database
- Network
- Authentication
- Storage
- Memory
- CPU

## Example Use Case

A production application generates the following logs:

```text
2026-08-09 10:15:01 INFO Application started
2026-08-09 10:15:05 INFO Connecting to database
2026-08-09 10:15:06 ERROR Database connection failed
2026-08-09 10:15:06 ERROR Connection refused: 10.10.20.15:5432
2026-08-09 10:15:10 WARNING Retrying database connection
2026-08-09 10:15:15 ERROR Database connection failed again
2026-08-09 10:16:00 INFO Application shutting down
```

The rule-based analyzer can identify:

```text
Component: DATABASE
Severity: HIGH
Severity Score: 7
Error Count: 3
```

### 2. AI Analysis

The parsed logs are then analyzed using a locally running **Llama 3.2** model through **Ollama**.

The AI generates:

- Problem summary
- Most likely root cause
- Severity
- Confidence score
- Possible causes
- Recommended actions
- Next steps

The AI-generated response is validated using a **Pydantic** model before being returned to the API client.

## API Endpoints

### 1. Health Check

Checks whether the **AI Log Analyzer** application and Ollama service are available.

```http
GET /health
```

#### Request

```bash
curl http://localhost:8000/health
```

#### Response — Ollama Available

```json
{
  "status": "healthy",
  "service": "AI Log Analyzer",
  "ollama": {
    "status": "available"
  }
}
```

#### Response — Ollama Unavailable

```json
{
  "status": "degraded",
  "service": "AI Log Analyzer",
  "ollama": {
    "status": "unavailable"
  }
}
```

---

### 2. Analyze Logs

Uploads a `.log` file and performs both **rule-based** and **AI-powered** analysis.

```http
POST /logs/analyze
```

#### Request

```bash
curl -X POST \
  http://localhost:8000/logs/analyze \
  -F "file=@logs/sample.log"
```

#### Response

```json
{
  "filename": "sample.log",
  "analysis": {
    "total_entries": 7,
    "level_counts": {
      "INFO": 3,
      "ERROR": 3,
      "WARNING": 1
    },
    "severity": "HIGH",
    "severity_score": 7,
    "component_detection": {
      "component": "DATABASE",
      "confidence": 0.83,
      "evidence": [
        "Connecting to database",
        "Database connection failed",
        "Connection refused: 10.10.20.15:5432"
      ]
    },
    "error_count": 3,
    "top_errors": [
      {
        "message": "Database connection failed",
        "occurrences": 1
      },
      {
        "message": "Connection refused: 10.10.20.15:5432",
        "occurrences": 1
      }
    ]
  },
  "ai_analysis": {
    "problem_summary": "Database connection failure",
    "root_cause": "Connection refused to the database server",
    "severity": "CRITICAL",
    "confidence": 0.9,
    "possible_causes": [
      "Database server is down or not reachable",
      "Network connectivity issue"
    ],
    "recommended_actions": [
      "Check the database server status",
      "Check network connectivity"
    ],
    "next_steps": [
      "Verify database server status",
      "Run a network connectivity test"
    ]
  }
}
```

### Supported File Type

The endpoint accepts only:

```text
.log
```

Example:

```bash
curl -X POST \
  http://localhost:8000/logs/analyze \
  -F "file=@logs/sample.log"
```

### Error Responses

#### Invalid File Type

```json
{
  "detail": "Only .log files are supported"
}
```

#### Empty Log File

```json
{
  "detail": "Uploaded log file is empty"
}
```

#### Invalid Log File

```json
{
  "detail": "No valid log entries found"
}
```

#### Ollama Unavailable

```json
{
  "detail": "AI analyzer is currently unavailable"
}
```

---

### 3. Interactive API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open:

```text
http://localhost:8000/docs
```

You can use the Swagger UI to:

- View available endpoints
- Upload log files
- Execute API requests
- Inspect JSON responses
- Test error scenarios

### 4. ReDoc Documentation

Alternative API documentation is available through ReDoc.

Open:

```text
http://localhost:8000/redoc
```

### 5. OpenAPI Specification

FastAPI automatically generates an OpenAPI specification for the application.

The raw OpenAPI schema is available at:

```text
http://localhost:8000/openapi.json
```

This specification can be used by API tools and clients to understand the available endpoints, request formats, and response schemas.

## Local Setup

### Prerequisites

Make sure the following are installed:

- Python 3.14+
- Ollama
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-log-analyzer
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

Pull the required model:

```bash
ollama pull llama3.2
```

Start Ollama:

```bash
ollama serve
```

Verify the model:

```bash
ollama list
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
```

The `.env` file is excluded from Git using `.gitignore`.

A template is available in:

```text
.env.example
```

### 6. Start the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Docker

The application can also be run inside a Docker container.

### Build the Image

```bash
docker build -t ai-log-analyzer .
```

### Run the Container

If Ollama is running on the host machine:

```bash
docker run -d \
  --name ai-log-analyzer \
  -p 8000:8000 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  ai-log-analyzer:latest
```

### Verify the Container

```bash
docker ps
```

Check the application health:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "AI Log Analyzer",
  "ollama": {
    "status": "available"
  }
}
```

### Analyze a Log Using Docker

```bash
curl -X POST \
  http://localhost:8000/logs/analyze \
  -F "file=@logs/sample.log"
```

## Testing

The project uses **Pytest** for automated testing.

Run the complete test suite:

```bash
pytest -v
```

Current test result:

```text
19 passed
```

The test suite covers:

- Log parsing
- Invalid log parsing
- Multiple log entries
- Component detection
- Severity calculation
- AI response validation
- Invalid AI JSON
- Missing AI fields
- Invalid severity
- Invalid confidence
- Ollama failures
- Ollama health checks
- API validation
- Empty files
- Invalid file types
- AI service unavailability

AI responses from Ollama are mocked during unit tests so that the test suite remains fast and independent of the Ollama service.

## Error Handling

The application handles failures at multiple layers.

### Invalid File Type

Only `.log` files are accepted.

```json
{
  "detail": "Only .log files are supported"
}
```

### Empty Log File

```json
{
  "detail": "Uploaded log file is empty"
}
```

### Invalid Log File

If the uploaded file does not contain valid log entries:

```json
{
  "detail": "No valid log entries found"
}
```

### Ollama Unavailable

If the Ollama service cannot be reached:

```json
{
  "detail": "AI analyzer is currently unavailable"
}
```

### Invalid AI JSON

If the LLM returns malformed JSON:

```text
AI analyzer returned an invalid response
```

### Invalid AI Response Structure

If the AI response does not match the expected Pydantic schema:

```text
AI analyzer returned an invalid response structure
```

## Design Decisions

### Rule-Based + AI Analysis

The application combines deterministic rule-based analysis with AI-powered analysis.

The rule-based analyzer provides:

- Predictable results
- Explainable severity scoring
- Component detection
- Error statistics

The AI analyzer provides:

- Contextual root-cause analysis
- Possible causes
- Troubleshooting recommendations
- Next-step suggestions
- Confidence estimation

This combination provides both **deterministic analysis and contextual reasoning**.

### Local LLM

The project uses Ollama with Llama 3.2 instead of an external AI API.

This allows logs to remain on the local system and avoids sending potentially sensitive log information to third-party AI services.

### Pydantic Validation

AI output is not returned directly to the client.

The response follows this flow:

```text
Ollama Response
      ↓
JSON Parsing
      ↓
Pydantic Validation
      ↓
Validated AIAnalysis
      ↓
API Response
```

This ensures that the AI response follows the expected structure.

### Automated Testing

External AI calls are mocked during unit tests.

This makes the tests:

- Fast
- Deterministic
- Independent of Ollama
- Suitable for CI/CD environments

## Security Considerations

- `.env` is excluded from Git
- `.env.example` contains only non-sensitive configuration
- AI analysis is performed locally
- Logs are not sent to external AI APIs
- Uploaded files are validated before processing
- AI responses are validated before being returned
- AI prompts explicitly instruct the model not to expose secrets or credentials

## Future Improvements

The project can be extended with:

- Web-based frontend dashboard
- Log search and filtering
- Historical incident storage
- Database integration
- User authentication and authorization
- Background processing for large log files
- Streaming AI responses
- Advanced anomaly detection
- Confidence-based alerting
- Rate limiting
- Structured application logging
- Prometheus metrics
- Application monitoring
- CI/CD pipeline
- Cloud deployment
- Production-grade observability

## Project Status

The current backend implementation includes:

- FastAPI REST API
- Rule-based log analysis
- Component detection
- Severity scoring
- AI-powered incident analysis
- Pydantic response validation
- Ollama health monitoring
- Error handling
- Automated testing
- Docker support
- Docker-to-Ollama integration

All automated tests are currently passing:

```text
19 passed
```

## License

This project is intended for learning, portfolio, and demonstration purposes.