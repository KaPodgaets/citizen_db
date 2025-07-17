import os
import pandas as pd
from sqlalchemy import text
from datetime import datetime

from src.utils.db import get_engine

def run_update_fake_id_table():
    """We need this table to be related to HAMAL application which uses only FID values to identify citizens"""
    engine = get_engine()
    
    with engine.begin() as conn:
        print('[LOG][update_fake_ids]: executing procedure `fid_update`')
        with open('sql/procedures/fid_update.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        sql_query = text(sql)
        try:
            conn.execute(sql_query)
            print('[LOG][update_fake_ids]: `table fake_id was updated successfully`')
        except Exception as e:
            raise Exception(f'[ERR][update_fake_ids] : {e}')

def save_fake_id_table_as_snapshot():
    """Saving xlsx file as snapshot to backfill dictionary in case of full restart the system"""
    engine = get_engine()
    with engine.begin() as conn:
        print('[LOG][fake_id_snapshot]: start snapshoting the table `fid_update`')
        sql_query = text('''
                        select 
                            citizen_id
                            , fake_citizen_id
                        from core.fake_citizen_ids
                    ''')
        try:
            df = pd.read_sql(sql_query, conn)
            # Ensure the directory exists
            os.makedirs('data/snapshots/', exist_ok=True)
            today_str = datetime.today().strftime('%Y-%m-%d')
            file_path = f'data/snapshots/fake_id-{today_str}.xlsx'
            df.to_excel(file_path, index=False)
            print(f'[LOG][fake_id_snapshot]: Saved snapshot to {file_path}')
        except Exception as e:
            raise Exception(f'[ERR][fake_id_snapshot] : {e}') 