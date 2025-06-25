FROM ghcr.io/astral-sh/uv:python3.13-bookworm as base

WORKDIR /
ADD pyproject.toml uv.lock /
RUN uv sync --no-default-groups

# ===== #

FROM base as flask

ENV PORT=8000
EXPOSE 8000

RUN uv sync --no-default-groups --group flask
ADD alembic.ini /
ADD migrations migrations
ADD main.py /
ADD --chmod=0755 start_scripts/flask.sh start.sh

ENTRYPOINT [ "/start.sh" ]

# ===== #

FROM base as socket
EXPOSE 9999

RUN uv sync --no-default-groups --group socket
ADD --chmod=0755 start_scripts/socket.py start.py
ENTRYPOINT [ "/start.py" ]
