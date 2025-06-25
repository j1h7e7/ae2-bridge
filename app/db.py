from flask_sqlalchemy import SQLAlchemy

from common.base import BaseORM

db: SQLAlchemy = SQLAlchemy(model_class=BaseORM)
