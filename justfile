test:
    uv run pytest -vv

lint:
    uv run ty check .
    uv run ruff check --fix .

dev:
    docker-compose up --build

export DOCKER_CLI_HINTS := "false"

oc-test:
    docker build -t oc .
    docker run -it --rm --network="host" --volume "{{absolute_path("./opencomputers/bridge/")}}:/OCEmu/src/loot/openos/bridge" oc