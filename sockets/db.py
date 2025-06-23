from sqlalchemy import create_engine

from common.config import get_db_url

engine = create_engine(url=get_db_url(), pool_size=10)
