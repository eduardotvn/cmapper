import psycopg2 
import csv
from connection.connection import start_connection
from connection.tableHandlers import create_table

def get_csv_info(url):
    with open(url, 'r') as file: 
        reader = csv.reader(file)
        column_headers = next(reader)
        sample = next(reader)
    
    column_types = [sql.Identifier(header).getquoted() + ' ' + 'TEXT' for header in column_headers]
    for i, data in enumerate(sample):
        try:
            int(data)
            column_types[i] = sql.Identifier(column_headers[i]).getquoted() + ' ' + 'INTEGER'
        except ValueError:
            try:
                float(data)
                column_types[i] = sql.Identifier(column_headers[i]).getquoted() + ' ' + 'NUMERIC'
            except ValueError:
                pass

    return column_headers, column_types

def try_table_creation(tableName, url) -> bool: 
    try:
        _, conn = start_connection()
        cur = conn.cursor() 

        col_names, col_types = get_csv_info(url)

        create_table_query = sql.SQL(f"""
        CREATE TABLE IF NOT EXISTS {tableName} (
            {sql.SQL(', ').join(sql.SQL(col_type) for col_type in col_types)}
        )""")

        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e:
        raise psycopg2.Error(f"{e}")
        return False 