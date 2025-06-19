import datetime

from sqlalchemy.orm import Query

from app.data.base import db
from app.data.models import ItemCount


def create_item_count(
    item_name: str, item_count: int, time: datetime.datetime | None = None
) -> ItemCount:
    entry = ItemCount(item_name=item_name, item_count=item_count, time=time)
    db.session.add(entry)
    db.session.flush()
    return entry


def item_base_query() -> Query[ItemCount]:
    return db.session.query(ItemCount)


def item_query_by_name(item_name: str) -> Query[ItemCount]:
    query = item_base_query()
    query = query.filter(ItemCount.item_name == item_name)
    return query
