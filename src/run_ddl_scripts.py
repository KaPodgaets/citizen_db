import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yaml
from sqlalchemy import text

from utils.db import get_engine

DDL_DIR = os.path.join(os.path.dirname(__file__), '..', 'sql', 'ddl')
ORDER_FILE = os.path.join(DDL_DIR, 'sql_scripts_order.yml')


def main():
    # Load order from YAML
    with open(ORDER_FILE, 'r', encoding='utf-8') as f:
        order = yaml.safe_load(f)['order']

    engine = get_engine()
    with engine.begin() as conn:
        for script_name in order:
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
                        conn.execute(text(batch))
                        print(f"[OK] {script_name} executed successfully.")
                    except Exception as e:
                        print(f"[ERROR] Failed to execute {script_name}: {e}")


def split_with_go_word(sql: str):
    import re
    # Split on lines that contain only GO (case-insensitive),
    # possibly with surrounding whitespace
    batches = [
        b.strip() for b in re.split(
            r'^\s*GO\s*$',
            sql,
            flags=re.IGNORECASE | re.MULTILINE
        ) if b.strip()
    ]
    return batches

if __name__ == "__main__":
    main() 