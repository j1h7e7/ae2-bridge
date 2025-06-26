from flask import Flask
from flask_pydantic_api import apidocs_views

import common.manifest as manifest  # noqa: F401
from api.db import db
from api.routes import main
from api.serialization import CustomJSONProvider
from common.config import get_db_url


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = get_db_url()
    flask_app.json = CustomJSONProvider(flask_app)
    db.init_app(flask_app)

    flask_app.register_blueprint(main)
    flask_app.register_blueprint(apidocs_views.blueprint, url_prefix="/apidocs")
    flask_app.add_url_rule("/", view_func=str)  # basic / endpoint

    return flask_app
