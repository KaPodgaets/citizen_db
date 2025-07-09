from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from src.utils.config import settings

_engine: Engine = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(settings.db_url, pool_pre_ping=True)
    return _engine
