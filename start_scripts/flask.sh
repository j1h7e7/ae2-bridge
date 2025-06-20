#!/bin/sh

uv run --no-sync alembic upgrade head
uv run --no-sync gunicorn main:flask_app --reload