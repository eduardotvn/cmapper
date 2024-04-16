import psycopg2

def start_connection(connection_str = None):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="cmapper",
            password="cmapper123456",
            host="localhost",
            port="5432"
        )

        return f"Connection to database succesful", conn 

    except psycopg2.Error as e: 
        return e



