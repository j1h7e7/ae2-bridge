FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /
ENV PORT=8000
EXPOSE 8000

ADD pyproject.toml uv.lock /
RUN uv sync --no-dev

ADD main.py run_app.sh /

ENTRYPOINT [ "/run_app.sh" ]