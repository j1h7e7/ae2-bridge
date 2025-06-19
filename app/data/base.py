from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class BaseORM(DeclarativeBase):
    pass


db: SQLAlchemy = SQLAlchemy(model_class=BaseORM)
