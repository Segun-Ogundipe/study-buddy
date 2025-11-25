# Parent image
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

# Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUDDERED=1

# Work directory inside the docker container
WORKDIR /app

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

#  Copy all contents from local to container in /app
COPY . .

# Setup the project
RUN uv sync --refresh

# Add virtual env to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Used PORTS
EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
