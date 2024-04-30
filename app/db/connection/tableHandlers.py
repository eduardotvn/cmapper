from .connection import start_connection
import psycopg2

def check_tables() -> list:
    try:
        _, conn = start_connection()
        cur = conn.cursor()
        cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")

        existing_tables = cur.fetchall()
            
        cur.close()
        conn.close()

        return existing_tables
    except Exception as e:
        print("Error while checking tables :", e)
        return []

def create_table(tableName, tableSchema, ) -> bool: 
    try: 
        _, conn = start_connection() 
        cur = conn.cursor() 

        creation_order = "CREATE TABLE IF NOT EXISTS " + tableName

        schema = "(id SERIAL PRIMARY KEY "
        if tableSchema:
            schema += ", ".join([f"{column} {dtype}" for column, dtype in tableSchema])
        schema += ")"
            
        cur.execute(creation_order + schema)
        conn.commit()
        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e:
        raise psycopg2.Error(f"{e}")
        return False 

def delete_table(tableName) -> bool:
    try: 
        _, conn = start_connection()
        cur = conn.cursor()

        cur.execute(f"""DROP TABLE IF EXISTS {tableName}""")
        conn.commit()

        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e: 
        raise psycopg2.Error(f"{e}")
        return False 