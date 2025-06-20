import socket
import socketserver
import threading
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app.app import create_app
from app.db import db as _db
from common.config import CONFIG
from sockets.app import App as SocketApp


@pytest.fixture(scope="session", autouse=True)
def _config():
    CONFIG.db_url = "sqlite://"


@pytest.fixture(scope="session")
def flask_app():
    app = create_app()
    app.config.update({"TEST": True})
    yield app


@pytest.fixture(scope="session")
def app_ctx(flask_app: Flask):
    with flask_app.app_context():
        yield


@pytest.fixture(scope="session")
def db(app_ctx: None):
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="session")
def client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def socket_app():
    HOST = "localhost"
    PORT = 9999

    with socketserver.ThreadingTCPServer((HOST, PORT), SocketApp) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield (HOST, PORT)
        server.shutdown()


@pytest.fixture(scope="function")
def socket_client(socket_app: tuple[str, int]) -> Generator[socket.socket, None, None]:
    HOST, PORT = socket_app
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((HOST, PORT))
        yield soc
        soc.send(b'{"event_type":"close"}\n')
        soc.recv(1024)
