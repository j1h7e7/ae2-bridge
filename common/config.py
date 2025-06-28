from functools import cache

from pydantic_settings import BaseSettings
from sqlalchemy import make_url


class Config(BaseSettings):
    postgres_username: str = "postgres"
    postgres_password: str = "password"
    db_url: str = ""


CONFIG: Config = Config()


def get_db_url():
    if CONFIG.db_url:
        return CONFIG.db_url

    return f"postgresql+psycopg2://{CONFIG.postgres_username}:{CONFIG.postgres_password}@localhost/postgres"


@cache
def get_dialect():
    return make_url(get_db_url()).get_backend_name()
