import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Text, func
from sqlmodel import Field, SQLModel


class ItemCount(SQLModel, table=True):
    __tablename__ = "itemcount"

    uuid: UUID = Field(primary_key=True, default_factory=uuid4)
    item_name: str = Field(sa_type=Text)
    item_count: int = Field()
    time: datetime.datetime = Field(  # ty: ignore[no-matching-overload]
        default=None,
        primary_key=True,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )
