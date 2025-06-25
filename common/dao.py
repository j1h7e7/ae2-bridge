import datetime

from sqlalchemy.orm import Query, Session

from common.models import ItemCount


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
