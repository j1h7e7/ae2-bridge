import socket
import socketserver
import threading
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

from app.app import create_app
from app.db import db as _db
from common.config import get_db_url
from sockets.app import App as SocketApp


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
def engine():
    engine = create_engine(get_db_url())
    import common.manifest  # noqa: F401

    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def _sessionmaker(engine: Engine):
    return sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def socket_app():
    HOST = "localhost"
    PORT = 9999

    with socketserver.TCPServer((HOST, PORT), SocketApp) as server:
        server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield (HOST, PORT)
        server.shutdown()


@pytest.fixture(scope="function")
def socket_client(socket_app: tuple[str, int]) -> Generator[socket.socket, None, None]:
    HOST, PORT = socket_app
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((HOST, PORT))
        soc.settimeout(10)
        yield soc

        # close nicely
        soc.settimeout(0.0001)
        try:
            soc.send(b'{"event_type":"close","src":"test"}\n')
            soc.recv(1024)
            soc.close()
        except (TimeoutError, ConnectionAbortedError):
            pass


@pytest.fixture(scope="function")
def session(_sessionmaker: sessionmaker) -> Generator[Session, None, None]:
    with _sessionmaker() as session:
        yield session
