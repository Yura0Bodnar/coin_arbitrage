FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . .

# Додаємо каталог у PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "coin_arbitrage/main.py"]
