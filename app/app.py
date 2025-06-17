from flask import Flask

from app.db.access import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:password@timescaledb/postgres"
)
db.init_app(app)


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/test")
def test():
    thing = db.session.execute(db.session.query(1))
    return f"test {thing}"
