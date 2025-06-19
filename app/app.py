from flask import Flask
from flask_socketio import send

import db.manifest as manifest  # noqa: F401
from app.config import get_db_url
from app.db import db
from app.routes import main
from app.socket import socketio


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = get_db_url()
    db.init_app(flask_app)
    socketio.init_app(flask_app)

    flask_app.register_blueprint(main)
    flask_app.add_url_rule("/", view_func=str)  # basic / endpoint
    socketio.on_event("test_event", lambda: send("test_resp"))  # test socket event

    return flask_app
