import math
from datetime import datetime as dt
from datetime import timezone as tz

import pytest
from sqlalchemy import func
from sqlalchemy.orm import Session

from common.dao import create_item_count, time_interval
from common.models import ItemCount


@pytest.mark.parametrize("hours", [1, 2, 3, 7, 13])
def test_time_query(session: Session, hours: int):
    for i in range(24):
        create_item_count(session, "a", 1, dt(2025, 1, 1, i, tzinfo=tz.utc))
        create_item_count(session, "a", 1, dt(2025, 1, 2, i, tzinfo=tz.utc))
        create_item_count(session, "a", 1, dt(2025, 1, 3, i, tzinfo=tz.utc))
    total_count = 24 * 3

    res = (
        session.query(func.min(ItemCount.time))
        .group_by(
            time_interval(
                ItemCount.time,
                seconds=60 * 60 * hours,
                start_time=dt(2025, 1, 1, tzinfo=tz.utc),
            )
        )
        .all()
    )
    assert len(res) == math.ceil(total_count / hours)
