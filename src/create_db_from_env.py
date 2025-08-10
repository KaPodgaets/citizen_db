import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text

from src.utils.config import settings
from utils.db import get_connection_uri_to_master


def main():
    """Drop existing DB and create new one. DB name defined in .env file"""
    db_name = settings.database

    connection_uri = get_connection_uri_to_master()
    engine = create_engine(connection_uri, pool_pre_ping=True)

    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        # Check if DB exists, if so, drop it
        result = conn.execute(text("SELECT db_id(:db_name)"), {"db_name": db_name})
        exists = result.scalar() is not None
        if exists:
            conn.execute(text(f"DROP DATABASE [{db_name}]"))
            print(f"Database '{db_name}' dropped.")
        # Create the database
        conn.execute(text(f"CREATE DATABASE [{db_name}]"))
        print(f"Database '{db_name}' created successfully.")

if __name__ == "__main__":
    main() 