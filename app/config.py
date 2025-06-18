from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="aebridge_")

    postgres_user: str = "postgres"
    postgres_password: str = "password"

    env: str = "prod"

    @computed_field
    @property
    def db_url(self) -> str:
        if self.env == "prod":
            return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@timescaledb/postgres"
        elif self.env == "test":
            return "sqlite://"
        raise ValueError


CONFIG = Config()
