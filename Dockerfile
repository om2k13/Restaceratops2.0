
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install poetry && poetry install --no-dev
COPY agent/ ./agent
COPY tests/ ./tests
ENTRYPOINT ["poetry", "run", "python", "-m", "agent.runner", "--tests", "tests"]
