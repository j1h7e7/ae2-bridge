import datetime

from sqlalchemy import SQLColumnExpression
from sqlalchemy.orm import Query, Session

from common.models import ItemCount
from common.sql_func import epoch


def create_item_count(
    session: Session,
    item_name: str,
    item_count: int,
    time: datetime.datetime | None = None,
) -> ItemCount:
    entry = ItemCount(item_name=item_name, item_count=item_count, time=time)
    session.add(entry)
    session.flush()
    return entry


def item_base_query() -> Query[ItemCount]:
    return Query(ItemCount)


def item_query_by_name(item_name: str) -> Query[ItemCount]:
    query = item_base_query()
    query = query.filter(ItemCount.item_name == item_name)
    return query


def time_interval(
    column: datetime.datetime, seconds: int, start_time: datetime.datetime | None = None
) -> SQLColumnExpression:
    if start_time and start_time.tzinfo is None:
        raise ValueError("start_time must have a timezone")

    start_epoch = int(start_time.timestamp()) if start_time else 0
    return (epoch(column) - start_epoch) // seconds
