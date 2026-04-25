.PHONY: up down logs test lint format type-check clean

up:
	docker compose up -d
	@echo "✓ All services started"

down:
	docker compose down

logs:
	docker compose logs -f

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/

format:
	black src/ tests/

type-check:
	mypy src/

simulate:
	python -m src.ingestion.simulator --patients 50 --rate 5

serve:
	uvicorn src.serving.api:app --reload --port 8000

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".mypy_cache" -exec rm -rf {} +

# 21:31:17 — automated update
# chore: chore: add .gitignore for Python/Docker/MLflow artifacts
