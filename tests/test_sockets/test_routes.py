import json
import socket

from sqlalchemy.orm import Session

from common.dao import item_query_by_name
from common.models import ItemCount


def test_socket(socket_client: socket.socket, session: Session):
    item_name = "test_item_0"
    socket_client.send(
        json.dumps(
            {"event_type": "item_count", "item_name": item_name, "item_count": 5}
        ).encode()
        + b"\n"
    )
    resp = socket_client.recv(1024)
    assert resp == b"ack\n"
    count: ItemCount = item_query_by_name(item_name).with_session(session).one()
    assert count.item_count == 5
