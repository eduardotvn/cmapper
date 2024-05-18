import psycopg2
from db.connection.connection import start_connection

def insert_table(tableName, insertionSchema ) -> bool:
    try:
        _, conn = start_connection()
        cur = conn.cursor()

        existing_columns = select_all_cols(tableName) 
        pkey = find_primary_key_column(tableName)
        if len(pkey) > 0:
            existing_columns.remove(pkey[0])

        print(pkey)

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

def update_table(tableName, column, value, pkey) -> bool:
    try:
        _, conn = start_connection()
        cur = conn.cursor()

        pkey_column = find_primary_key_column(tableName)[0]

        query = f"""UPDATE {tableName}
                    SET "{column}" = %s
                    WHERE "{pkey_column}" = %s
                """

        cur.execute(query, (value, pkey))
        conn.commit()
        cur.close()
        conn.close() 

        return True
    except Exception as e:
        print(e)
        return False 

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

        col = find_primary_key_column(tableName)[0]

        query = f"DELETE FROM {tableName} WHERE {col} = {identifier}"
        cur.execute(query)

        conn.commit() 
        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e: 
        raise psycopg2.Error(f"{e}")
        return False 

def find_primary_key_column(tablename): 
    try: 
        _, conn = start_connection()
        cur = conn.cursor()

        query = f"""
        SELECT c.column_name
        FROM information_schema.table_constraints tc 
        JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
        JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
        AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
        WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{tablename}';
        """

        cur.execute(query)
        col = cur.fetchall()
        print("cols: ", col)

        cur.close()
        conn.close()  
        return [row[0] for row in col]

    except psycopg2.Error as e: 
        print(e)
        return []

def create_new_pkey(tableName): 
    try:
        _, conn = start_connection()
        cur = conn.cursor()

        query = f"""
        ALTER TABLE {tableName}
        ADD COLUMN pkey SERIAL PRIMARY KEY;
        SELECT setval(pg_get_serial_sequence('{tableName}', 'pkey'), 1, false);
        """

        cur.execute(query)
        conn.commit()

        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e:
        print(e)
        return False 