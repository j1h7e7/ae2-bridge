import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio import SocketIO, SocketIOTestClient

from app.app import create_app
from app.config import CONFIG
from app.db import db as _db


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
def socket_client(flask_app: Flask) -> SocketIOTestClient:
    sio: SocketIO = flask_app.extensions["socketio"]
    return sio.test_client(app=flask_app)
