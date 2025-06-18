#!/bin/sh

# uv run alembic upgrade head
uv run gunicorn app.app:app --reload