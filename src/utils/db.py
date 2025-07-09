from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import urllib
from src.utils.config import settings

_engine: Engine = None

def get_engine() -> Engine:
    global _engine
    server = urllib.parse.quote_plus(settings.server)
    database = settings.database
    driver = urllib.parse.quote_plus("ODBC Driver 17 for SQL Server")

    db_url = (
    f"mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes"
    )

    if _engine is None:
        _engine = create_engine(db_url, pool_pre_ping=True)
    return _engine