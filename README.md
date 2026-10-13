# AI Recommendation Service

FastAPI service that generates job recommendations based on user preferences and available jobs.
## Project Structure

```text
AI-recommendationService/
├── app/
|   |── .env                             # Local configuration; do not commit
│   ├── main.py                         # FastAPI application entry point
│   ├── api/
│   │   └── recommendations.py          # Recommendation endpoint and dependencies
│   ├── clients/
│   │   ├── openai_client.py            # OpenAI configuration and client
│   │   ├── llm_client.py               # LLM requests
│   │   └── EmbeddingClient.py          # Embedding generation
│   ├── core/
│   │   ├── Settings.py                 # Application settings
│   │   └── exceptions.py               # Custom exceptions
│   ├── models/
│   │   ├── recommendationRequest.py    # Request validation model
│   │   ├── RecommendationResponse.py   # Response model
│   │   ├── JobData.py                  # Job model
│   │   ├── JobPreferences.py           # User preferences model
│   │   ├── LookupValue.py              # Lookup model
│   │   └── *.py                        # Enum and package models
│   └── services/
│       ├── RecommendationService.py    # Main recommendation workflow
│       ├── PreprocessingService.py     # Data preparation
│       ├── DeterministicMatchingService.py
│       ├── SemanticMatchingService.py
│       ├── ScoringService.py
│       └── ExplanationService.py
├── tests/                              # not yet
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
└── .gitignore                          # Ignored files
```

Unit tests run locally and do not consume OpenAI tokens unless they explicitly call the real OpenAI API. Use mocks for external clients.

## Workflow

1. `app.main` creates the FastAPI application.
2. The recommendations router is registered under `/api/recommendations`.
3. FastAPI validates the request using Pydantic models:
   - required `preferences`;
   - at least 1 and at most 500 jobs;
   - unique job IDs;
   - `limit` between 1 and 100;
   - valid enum values and UUIDs.
4. Dependencies create the recommendation pipeline:
   - preprocessing;
   - deterministic matching;
   - semantic matching with embeddings;
   - scoring;
   - LLM-generated explanations.
5. `RecommendationService` combines the results and returns ranked recommendations.

## Requirements

- Python 3.11+
- OpenAI API key
- Dependencies from `requirements.txt`

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
Activate.ps1
pip install -r requirements.txt
```

Create a .env file with the settings required by app.core.Settings, for example:
``` OPENAI_API_KEY=your-api-key ```
Do not commit .env or API keys to source control.

Run:

``` uvicorn app.main:app --reload ```

Available URLs:

API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
Health check: http://127.0.0.1:8000/health
Recommendations: POST /api/recommendations

