from flask import Blueprint

from app.db import db
from common import dao

main = Blueprint("main", __name__)


@main.route("/insert")
def add_entry():
    dao.create_item_count(db.session, item_name="test item", item_count=1, time=None)
    db.session.commit()
    return "added!"


@main.route("/query")
def query():
    query = dao.item_base_query()
    counts = db.session.execute(query).scalars().all()
    return f"there are {len(counts)}"


@main.route("/all")
def get_all():
    query = dao.item_base_query()
    all_item_logs = db.session.execute(query).scalars().all()
    return all_item_logs
