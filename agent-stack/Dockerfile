FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TUKUK_AGENT_MODEL=${TUKUK_AGENT_MODEL:-llama3.2}

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent ./agent
COPY mcp_server ./mcp_server
COPY security ./security

EXPOSE 8000 8080

CMD ["python", "-m", "agent.main"]
