import psycopg2
from db.connection.connection import start_connection

def insert_table(tableName, insertionSchema ) -> bool:
    try:
        _, conn = start_connection()
        cur = conn.cursor()

        existing_columns = select_all_cols(tableName) 

        insertion_query = f"INSERT INTO {tableName} "
        columns = "("
        if existing_columns:
            columns += ", ".join(f'"{column}"' for column in existing_columns)
            columns += ")"

        insertion_query += columns 

        query = " VALUES ("
        if insertionSchema:
            query += ", ".join([f'{value}' for value in insertionSchema])
        query += " )"

        insertion_query += query

        print(insertion_query)

        cur.execute(insertion_query)
        conn.commit()
        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e: 
        raise psycopg2.Error(f"{e}")
        return False 

def update_table(tableName , updateSchema ) -> bool: 
    #Under development
    pass 

def select_all_cols(tableName: str ) -> list: 
    try: 
        _, conn = start_connection()
        cur = conn.cursor()

        cur.execute(f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{tableName}'
            ORDER BY ORDINAL_POSITION;
        """)
        headers = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()
        return headers
    except psycopg2.Error as e:
        return []

def select_all_cols_and_types(tableName: str) -> list: 
    try: 
        _, conn = start_connection()
        cur = conn.cursor()

        cur.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{tableName}'
            ORDER BY ORDINAL_POSITION;
        """)
        
        columns_info = cur.fetchall()

        cur.close()
        conn.close()

        return columns_info
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return []

        
def select_all_rows(tableName ) -> list:
    try: 
        _, conn = start_connection() 
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {tableName}")

        all_rows = cur.fetchall()

        headers = select_all_cols(tableName)

        return all_rows, headers
    except psycopg2.Error as e: 
        return []

def filter_rows(tableName, filter, column ) -> list:
    try:
        _, conn = start_connection()

        cur = conn.cursor() 

        cur.execute(f'SELECT * FROM {tableName} WHERE "{column}"::TEXT LIKE %s', (f"{filter}%",))

        rows = cur.fetchall() 
        cur.close()
        conn.close()
        return rows 
    except psycopg2.Error as e:
        raise psycopg2.Error(f"{e}")
        return []

def delete_row(tableName, identifier ) -> bool:
    try: 
        _, conn = start_connection()
        cur = conn.cursor()

        query = f"DELETE FROM {table_name} WHERE {condition_column} = ?"
        cur.execute(query, (identifier,))

        conn.comit() 
        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e: 
        raise psycopg2.Error(f"{e}")
        return False 