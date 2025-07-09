from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from src.utils.config import settings

def test_can_connect_to_database():
    server = settings.server
    database = settings.database

    connection_uri = (
        f"mssql+pyodbc://@{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )

    try:
        engine = create_engine(connection_uri)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            assert result == 1
    finally:
        engine.dispose()
