import json
import socket
from typing import Any

from sqlalchemy.orm import Session

from common.dao import item_query_by_name
from common.models import ItemCount


def send(soc: socket.socket, data: Any):
    soc.send(json.dumps(data).encode() + b"\n")


def test_item_count(socket_client: socket.socket, session: Session):
    item_name = "test_item_0"
    send(
        socket_client,
        {"event_type": "item_count", "item_name": item_name, "item_count": 5},
    )
    resp = socket_client.recv(1024)
    assert resp == b"ack\n"
    count: ItemCount = item_query_by_name(item_name).with_session(session).one()
    assert count.item_count == 5


def test_multiple_items(socket_client: socket.socket, session: Session):
    item_name_0 = "test_two_items_0"
    item_name_1 = "test_two_items_1"
    send(
        socket_client,
        {"event_type": "item_count", "item_name": item_name_0, "item_count": 1},
    )
    socket_client.recv(1024)
    send(
        socket_client,
        {"event_type": "item_count", "item_name": item_name_1, "item_count": 2},
    )
    socket_client.recv(1024)
    count0: ItemCount = item_query_by_name(item_name_0).with_session(session).one()
    count1: ItemCount = item_query_by_name(item_name_1).with_session(session).one()
    assert count0.item_count == 1
    assert count1.item_count == 2
