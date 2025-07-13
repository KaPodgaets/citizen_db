from src.transformations.error_handling import global_error_handler
from src.utils.db import get_engine

@global_error_handler('publish')
def main():
    engine = get_engine()

    with engine.begin() as conn:
        print('check that datamart table exists')
        check_mart_table_exists(conn)

        print('check tasks - not relevant for now')
        print('get one mega table by merge')
        print('clean table with pandas')

        print('delete previous data')
        delete_all_rows_from_mart_table(conn)
        
        print('insert new data')
    print('Mart population complete.')

def check_mart_table_exists(conn):
    # Check if mart.citizens table exists
    check_table_sql = '''
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'mart' AND TABLE_NAME = 'citizens'
    '''
    result = conn.execute(check_table_sql)
    table_exists = result.scalar() > 0
    if table_exists:
        delete_sql = "DELETE FROM mart.citizens"
        conn.execute(delete_sql)
        print('Deleted all records from mart.citizens')
    else:
        raise Exception('Table mart.citizens does not exist.')

def delete_all_rows_from_mart_table(conn):
    try:
        delete_sql = "DELETE FROM mart.citizens"
        conn.execute(delete_sql)
        print('Deleted all records from mart.citizens')
    except Exception as e:
        print(f'Can not delete rows from mart.citizen. [ERROR]: {e}')
        raise Exception(f'Can not delete rows from mart.citizen. [ERROR]: {e}')

if __name__ == "__main__":
    main()
