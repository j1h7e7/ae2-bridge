import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.data.base import BaseORM, db


class ItemCount(BaseORM):
    __tablename__ = "itemcount"

    item_name: Mapped[str] = mapped_column(
        db.Text,
        nullable=False,
        primary_key=True,
    )
    item_count: Mapped[int] = mapped_column(
        db.Integer,
        nullable=False,
        primary_key=True,
    )
    time: Mapped[datetime.datetime] = mapped_column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        primary_key=True,
    )
