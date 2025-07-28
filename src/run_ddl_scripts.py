import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yaml
from sqlalchemy import text

from utils.db import get_engine

DDL_DIR = os.path.join(os.path.dirname(__file__), '..', 'sql', 'ddl')
ORDER_FILE = os.path.join(DDL_DIR, 'sql_scripts_order.yml')

SQL_VIEW_DROP = """
IF EXISTS (
    SELECT * FROM sys.views 
    WHERE name = 'vw_citizens_anon' 
        AND schema_id = SCHEMA_ID('mart')
    )

    EXEC('DROP VIEW [mart].[vw_citizens_anon]');
"""

def main():
    # Load order from YAML
    with open(ORDER_FILE, 'r', encoding='utf-8') as f:
        order = yaml.safe_load(f)['order']

    engine = get_engine()
    print(f"Connecting to: {engine.url}")
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        for script_name in order:
            if script_name == 'mart_view_citizens_anon.sql':
                conn.execute(text(SQL_VIEW_DROP))
                conn.commit()

            script_path = os.path.join(DDL_DIR, script_name)
            if not os.path.exists(script_path):
                print(f"[ERROR] Script not found: {script_path}")
                continue
            print(f"[INFO] Executing {script_name} ...")
            with open(script_path, 'r', encoding='utf-8') as sql_file:
                sql = sql_file.read()
                batches = split_with_go_word(sql)
                for i, batch in enumerate(batches, 1):
                    try:
                        # conn.execute(text(batch))
                        conn.exec_driver_sql(batch)
                        conn.commit() 
                        print(f"[OK] {script_name} batch {i} executed successfully.")
                        # print(f"""---{script_name} batch #{i}---""")
                        # print(f"""{batch}""")
                    except Exception as e:
                        print(f"[ERROR] Failed to execute {script_name}: {e}")


def split_with_go_word(sql: str):
    import re
    # Split on lines that contain only GO (case-insensitive),
    # possibly with surrounding whitespace
    def is_not_just_comment(block: str) -> bool:
        lines = [line.strip() for line in block.strip().splitlines()]
        return any(line and not line.startswith("--") for line in lines)
    
    batches = [
        b.strip() for b in re.split(
            r'^\s*GO\s*$',
            sql,
            flags=re.IGNORECASE | re.MULTILINE
        ) if b.strip() and is_not_just_comment(b)
    ]
    # for i, batch in enumerate(batches, 1):
    #     print(f"\n--- BATCH {i} ---")
    #     print(batch)
    #     print(
    #         "IS COMMENT ONLY:",
    #         all(
    #             line.strip().startswith("--")
    #             for line in batch.splitlines()
    #             if line.strip()
    #         )
    #     )
    return batches

if __name__ == "__main__":
    main() 