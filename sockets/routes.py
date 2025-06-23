from sqlalchemy.orm import Session

from common.dao import create_item_count
from sockets.db import engine
from sockets.event_handler import EventHandlerManager
from sockets.event_types import ItemCountEventPayload, TestEventPayload

event_handler = EventHandlerManager()


@event_handler.register
def test(payload: TestEventPayload):
    return payload.data.capitalize()


@event_handler.register
def write_item(payload: ItemCountEventPayload):
    # TODO: pass session in from event handler, or use contextvar (?)
    with Session(engine) as session:
        create_item_count(
            session=session,
            item_name=payload.item_name,
            item_count=payload.item_count,
        )
        session.commit()
