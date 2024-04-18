import psycopg2
from db.connection.connection import start_connection

def insert_table(tableName = None, insertionSchema = None) -> bool:
    try:
        _, conn = start_connection()
        cursor = conn.cursor()

        cur.execute(f"""SELECT column_names FROM information_schema.columns WHERE table_name = '{tableName}'""")
        existing_columns = cur.fetchall() 

        insertion_query = f"INSERT INTO {tableName} "
        columns = "( "
        if existing_columns: 
            columns += existing_columns[0][0] 
            columns += ", ".join([f", {value[0]}" for value in existing_columns[1:]])
        columns += " )"

        insertion_query += columns 

        query = " VALUES ("
        if insertionSchema:
            query += insertionSchema[0]
            query += ", ".join([f", {value}" for value in insertionSchema[1:]])
        query += " )"

        insertion_query += query

        cur.execute(insertion_query)
        conn.commit()
        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e: 
        raise psycopg2.Error(f"{e}")
        return False 

def update_table(tableName = None, updateSchema = None) -> bool: 
    #Under development
    pass 

def select_all_cols(tableName: str) -> list: 
    try: 
        _, conn = start_connection()
        cur = conn.cursor()

        cur.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s;
        """, (tableName,))
        headers = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()
        return headers
    except psycopg2.Error as e:
        return []


def select_all_rows(tableName) -> list:
    try: 
        _, conn = start_connection() 
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {tableName}")

        all_rows = cur.fetchall()

        headers = select_all_cols(tableName)

        return all_rows, headers
    except psycopg2.Error as e: 
        return []

def filter_rows(tableName = None, filter = None, column = None) -> list:
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

def delete_row(tableName = None, identifier = None) -> bool:
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