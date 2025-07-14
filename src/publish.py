import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from sqlalchemy import text

from src.transformations.error_handling import global_error_handler
from src.utils.db import get_engine

@global_error_handler('publish')
def main():
    engine = get_engine()

    with engine.begin() as conn:
        print('[publish]: Check that datamart table exists')
        check_mart_table_exists(conn)

        # print('[publish]: Check tasks - not relevant for now')

        print('[publish]: insert new data by executing procedure `build_mart_table`')
        with open('sql/procedures/build_mart_table.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        sql_query = text(sql)
        try:
            conn.execute(sql_query)
        except Exception as e:
            raise Exception(f'[build_mart_table][ERROR] : {e}')


    print('[publish]: DataMart layer was built')

def check_mart_table_exists(conn):
    # Check if mart.citizens table exists
    check_table_sql = text('''
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'mart' AND TABLE_NAME = 'citizens'
    ''')

    result = conn.execute(check_table_sql)
    table_exists = result.scalar() > 0
    if table_exists:
        print('[publish]: Table mart.citizens exists')
    else:
        raise Exception('[publish] : [ERROR] : Table mart.citizens does not exist.')

# def delete_all_rows_from_mart_table(conn):
#     try:
#         delete_sql = text("DELETE FROM mart.citizens")
#         conn.execute(delete_sql)
#         print('[publish][delete_all_rows_from_mart_table]: Deleted all records from mart.citizens')
#     except Exception as e:
#         raise Exception(f'[publish][delete_all_rows_from_mart_table]: Can not delete rows from mart.citizen. [ERROR]: {e}')

if __name__ == "__main__":
    main()
