from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import db.manifest  # noqa: F401 # loads all models
from app.config import get_db_url
from app.data.base import BaseORM

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseORM.metadata
config.set_main_option("sqlalchemy.url", get_db_url())


def exclude_by_name(name, type_, parent_names):
    # needed for timescaledb
    exclude_indexes = {"itemcount_time_idx"}
    if type_ == "index":
        return name not in exclude_indexes
    else:
        return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=exclude_by_name,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_name=exclude_by_name,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
