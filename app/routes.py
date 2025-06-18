from flask import Blueprint
from sqlalchemy import select

from app.data.base import db
from app.data.models import ItemCount

main = Blueprint("main", __name__)


@main.route("/insert")
def add_entry():
    count = ItemCount(item_name="test item", item_count=1, time=None)
    db.session.add(count)
    db.session.commit()
    return "added!"


@main.route("/query")
def query():
    query = select(ItemCount)
    counts = db.session.execute(query).scalars().all()
    return f"there are {len(counts)}"
