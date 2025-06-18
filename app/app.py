from flask import Flask

from app.config import CONFIG
from app.db.base import db
from app.db.manifest import *  # noqa: F403

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = CONFIG.db_url
db.init_app(app)


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/test")
def test():
    thing = db.session.execute(db.session.query(1))
    return f"test {thing}"
