import psycopg2
import os 

def start_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DBNAME'),
            user = os.getenv('USERNAME'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST'),
            port=os.getenv('PORT')
        )

        return f"Connection to database succesful", conn 

    except psycopg2.Error as e: 
        return e
