from .connection import start_connection
import psycopg2

def check_tables() -> list:
    _, conn = start_connection()
    cur = conn.cursor()
    cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")

    existing_tables = cur.fetchall()
        
    cur.close()
    conn.close()
    return existing_tables