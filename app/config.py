from pydantic_settings import BaseSettings


class Config(BaseSettings):
    postgres_username: str = "postgres"
    postgres_password: str = "password"
    db_url: str = ""


CONFIG: Config = Config()


def get_db_url():
    if CONFIG.db_url:
        return CONFIG.db_url

    return f"postgresql+psycopg2://{CONFIG.postgres_username}:{CONFIG.postgres_password}@localhost/postgres"
