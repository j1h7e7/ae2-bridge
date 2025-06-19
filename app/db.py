from flask_sqlalchemy import SQLAlchemy

from db.base import BaseORM

db: SQLAlchemy = SQLAlchemy(model_class=BaseORM)
