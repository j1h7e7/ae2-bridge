FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /
ENV PORT=8000
EXPOSE 8000

ADD pyproject.toml uv.lock /
RUN uv sync

ENTRYPOINT [ "uv", "run" ]
CMD [ "gunicorn", "app.app:app", "--reload" ]