"""add timescaledb stuff

Revision ID: ee93214218cf
Revises: d8e6715f2475
Create Date: 2025-06-30 21:02:08.214122

"""

from typing import Sequence, Union

from alembic import op

TABLE_NAME = "itemcount"
TIME_COLUMN = "time"

# revision identifiers, used by Alembic.
revision: str = "ee93214218cf"
down_revision: Union[str, Sequence[str], None] = "d8e6715f2475"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        f"""ALTER TABLE {TABLE_NAME} SET(
                timescaledb.enable_columnstore, 
                timescaledb.orderby = '{TIME_COLUMN} DESC', 
                timescaledb.segmentby = 'item_name',
                timescaledb.compress_chunk_time_interval = '24 hours');"""
    )
    op.execute(f"CALL add_columnstore_policy('{TABLE_NAME}', after => INTERVAL '7d');")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
