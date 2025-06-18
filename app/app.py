from flask import Flask

import app.data.manifest as manifest  # noqa: F401
from app.config import CONFIG
from app.data.base import db
from app.routes import main


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = CONFIG.db_url
    db.init_app(flask_app)

    flask_app.register_blueprint(main)

    return flask_app
