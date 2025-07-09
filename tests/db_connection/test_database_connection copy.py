from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import urllib
from src.utils.config import settings

def test_database_connection(server: str, database: str):
    connection_uri = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

    try:
        print("🔌 Attempting to connect to the database...")
        engine = create_engine(connection_uri)
        with engine.connect() as connection:
            # Run a simple query to validate the connection
            result = connection.execute(text("SELECT GETDATE()")).scalar()
            print(f"✅ Connection successful. Server time: {result}")
    except SQLAlchemyError as e:
        print("❌ Connection failed.")
        print(f"Error: {e}")
    finally:
        # Ensure the engine is properly disposed
        engine.dispose()
        print("🔒 Connection closed (engine disposed).")

if __name__ == "__main__":
    server = settings.server
    database = settings.database
    # server = r"10.160.236.73\DATAWAREHOUSE"
    # database = "citizen_db_project_test"

    test_database_connection(server, database)
