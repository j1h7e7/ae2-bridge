import datetime

from sqlalchemy import Function, func

from common.config import get_dialect

# Needed so I can test using sqlite but deploy with postgres
# Curse you, sql dialects!


def epoch(column: datetime.datetime) -> Function:
    dialect = get_dialect()

    if dialect == "postgresql":
        return func.date_part("epoch", column)
    elif dialect == "sqlite":
        return func.unixepoch(column)

    raise NotImplementedError(f"Unsupported dialect: {dialect}")
