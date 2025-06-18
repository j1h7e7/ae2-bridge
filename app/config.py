from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="aebridge_")

    postgres_user: str = "postgres"
    postgres_password: str = "password"

    @computed_field
    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@timescaledb/postgres"


CONFIG = Config()
