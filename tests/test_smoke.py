import json
import socket
import uuid

from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from common.models import ItemCount

# basic tests to make sure that very basic functionality is still there


def test_db_access(db: SQLAlchemy):
    item_name = str(uuid.uuid4())
    db.session.add(ItemCount(item_name=item_name, item_count=1))
    db.session.commit()

    db.session.query(ItemCount).filter(ItemCount.item_name == item_name).one()


def test_api_access(client: FlaskClient):
    resp = client.get("/")
    assert resp.status_code == 200

    resp = client.get("/_should_never_exist")
    assert resp.status_code == 404


def test_socket(socket_client: socket.socket):
    socket_client.send(
        json.dumps({"event_type": "test", "data": "hello"}).encode() + b"\n"
    )
    resp = socket_client.recv(1024)
    assert resp == b"Hello\n"
