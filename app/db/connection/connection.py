import psycopg2
import os 
import time 

def start_connection(retry_count=5, delay=2):
    last_exception = None
    for attempt in range(retry_count):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DBNAME'),
                user=os.getenv('USERNAME'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'),
                port=os.getenv('PORT')
            )
            return None, conn
        except psycopg2.Error as e:
            print(f"Attempt {attempt+1} failed: {e}")
            last_exception = e
            time.sleep(delay)  
    return last_exception, None
