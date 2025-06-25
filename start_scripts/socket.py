#!/usr/bin/env -S uv run --no-sync --script
from sockets.app import start_server

# TODO: figure out a way to make this work from root directory too?
start_server(host="0.0.0.0")
