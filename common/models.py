import datetime

from sqlalchemy import TIMESTAMP, Text
from sqlmodel import Field, SQLModel


class ItemCount(SQLModel, table=True):
    __tablename__ = "itemcount"
    item_name: str = Field(sa_type=Text, primary_key=True)
    item_count: int = Field(primary_key=True)
    time: datetime.datetime = Field(  # ty: ignore[no-matching-overload]
        sa_type=TIMESTAMP(timezone=True),
        default_factory=datetime.datetime.now,
        primary_key=True,
    )
