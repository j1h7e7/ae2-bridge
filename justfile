test:
    uv run pytest -vv

lint:
    uv run ty check .
    uv run ruff check --fix .

dev:
    docker-compose up --build
