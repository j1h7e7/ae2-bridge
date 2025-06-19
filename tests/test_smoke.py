import uuid

from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from db.models import ItemCount


def test_db_access(db: SQLAlchemy):
    item_name = str(uuid.uuid4())
    db.session.add(ItemCount(item_name=item_name, item_count=1))
    db.session.commit()

    db.session.query(ItemCount).filter(ItemCount.item_name == item_name).one()


def test_api_access(client: FlaskClient):
    resp = client.get("/")
    assert resp.status_code == 200

    resp = client.get("/_should_never_exist")
    assert resp.status_code == 404
