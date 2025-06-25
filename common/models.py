import datetime

from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from common.base import BaseORM


class ItemCount(BaseORM):
    __tablename__ = "itemcount"

    item_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        primary_key=True,
    )
    item_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        primary_key=True,
    )
