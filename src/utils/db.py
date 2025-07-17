from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from urllib.parse import quote_plus
from src.utils.config import settings

_engine: Engine | None = None

def get_engine() -> Engine:
    global _engine
    db_uri = get_connection_uri()
    if _engine is None:
        _engine = create_engine(db_uri, pool_pre_ping=True)
    return _engine

def get_connection_uri():
    connection_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={settings.server};"
        f"Database={settings.database};"
        "Trusted_Connection=yes;"
    )

    encoded_connection_string = quote_plus(connection_string)
    connection_uri = f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}"
    return connection_uri