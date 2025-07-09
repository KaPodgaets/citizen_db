from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
from src.utils.config import settings
from src.utils.db import get_engine

def test_can_connect_to_database():
    connection_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={settings.server};"
        f"Database={settings.database};"
        "Trusted_Connection=yes;"
    )

    encoded_connection_string = quote_plus(connection_string)
    connection_uri = f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}"

    try:
        engine = create_engine(connection_uri)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            assert result == 1
    finally:
        engine.dispose()


def test_get_engine():
    try:
        engine = get_engine()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            assert result == 1
    finally:
        engine.dispose()