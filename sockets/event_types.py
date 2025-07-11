from typing import Literal, Union

from pydantic import BaseModel, Field, RootModel


class BaseEventPayload(BaseModel):
    event_type: str


class CloseEventPayload(BaseEventPayload):
    event_type: Literal["close"]


class TestEventPayload(BaseEventPayload):
    event_type: Literal["test"]
    data: str = ""


class ItemCountEventPayload(BaseEventPayload):
    event_type: Literal["item_count"]
    item_name: str
    item_count: int


AllEventPayloads = Union[CloseEventPayload | TestEventPayload | ItemCountEventPayload]


class EventPayload(RootModel[AllEventPayloads]):
    root: AllEventPayloads = Field(discriminator="event_type")
