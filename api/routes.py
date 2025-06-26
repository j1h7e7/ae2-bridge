from flask import Blueprint

from api.db import db
from api.decorators import pydantic_api
from common import dao
from common.models import ItemCount

main = Blueprint("main", __name__)


@main.get("/insert")
@pydantic_api()
def add_entry() -> str:
    dao.create_item_count(db.session, item_name="test item", item_count=1, time=None)
    db.session.commit()
    return "added!"


@main.get("/query")
@pydantic_api()
def query() -> str:
    query = dao.item_base_query()
    counts = query.with_session(db.session).all()
    return f"there are {len(counts)}"


@main.post("/item_count")
@pydantic_api()
def create_item_count(item_count: ItemCount) -> ItemCount:
    db.session.add(item_count)
    db.session.commit()
    return item_count


@main.get("/all")
@pydantic_api()
def get_all() -> list[ItemCount]:
    query = dao.item_base_query()
    all_item_logs = query.with_session(db.session).all()
    return all_item_logs
