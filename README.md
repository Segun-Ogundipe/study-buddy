# Study Buddy

Lightweight Streamlit app to generate and take short quizzes using LLMs (Groq / OpenAI).

## Features
- Generate Multiple Choice (MCQ) and Fill-in-the-Blank questions via LLMs.
- Evaluate and save quiz results as CSV.
- Configurable model provider, model, temperature and retry policy.
- Dockerized and CI/CD-ready (Jenkins + Kubernetes manifests).

## Quickstart

Prerequisites
- Python >= 3.13
- Streamlit
- Environment variables: `OPENAI_API_KEY` and/or `GROQ_API_KEY`

Install & run locally
```sh
uv sync
streamlit run main.py
```

Run with Docker
```sh
docker build -t studybuddy-image:v1 .
docker run -p 8501:8501 studybuddy-image:v1
```

Configuration
- UI defaults are in [src/config/ui_config.ini](src/config/ui_config.ini) and accessed via [src/config/ui_config.py](src/config/ui_config.py).
- Model clients are created in [src/llm/clients.py](src/llm/clients.py).
- Prompt templates are in [src/prompts/templates.py](src/prompts/templates.py).

How it works (core components)
- The app entry point is [main.py](main.py).
- Question generation is handled by the [`QuestionGenerator`](src/generator/question_generator.py) class.
- Quiz orchestration (generate, present, evaluate, save) is done by the [`QuizManager`](src/utils/helpers.py) class.
- Question schemas: [`MCQQuestion`](src/models/question_schemas.py) and [`FillBlankQuestion`](src/models/question_schemas.py).

Persistence & artifacts
- Generated results are saved to the `results/` directory (CSV).
- Logs are written to the `logs/` directory.

CI / CD
- Jenkins pipeline: [Jenkinsfile](Jenkinsfile)
- Kubernetes manifests: [ci_cd/deployment.yaml](ci_cd/deployment.yaml), [ci_cd/service.yaml](ci_cd/service.yaml)
- CI image for Jenkins: [ci_cd/Dockerfile](ci_cd/Dockerfile)

Development notes
- See [pyproject.toml](pyproject.toml) for dependencies.
- Docker build uses the repository root [Dockerfile](Dockerfile).
- Secrets and API keys may be provided via environment variables or the Streamlit UI.
