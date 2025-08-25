#!/bin/sh

uv run --no-sync alembic upgrade head
uv run --no-sync granian --interface wsgi main:flask_app --reload --host 0.0.0.0
