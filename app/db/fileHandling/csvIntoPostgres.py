import psycopg2 
from psycopg2 import sql  
import csv
from db.connection.connection import start_connection
from db.connection.tableHandlers import create_table
from dateutil.parser import parse

def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False

def is_bool(string):
    return string.lower() in ['true', 'false']

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_csv_info(url):
    with open(url, 'r') as file:
        first_line = file.readline().strip()
        delimiters = [',','\t',':']
        delimiter = None
        for delim in delimiters: 
            if delim in first_line:
                delimiter = delim

    if delimiter is None:
        print("Unable to determine delimiter. Please use either comma (,) or tab (\\t).")
        return None, None
    
    with open(url, 'r') as file:
        reader = csv.reader(file, delimiter=delimiter)
        column_names = next(reader)
        
        column_types = ['TEXT'] * len(column_names)
        
        for row in reader:
            for i, value in enumerate(row):
                if column_types[i] == 'TEXT' and value.isdigit():
                    column_types[i] = 'INTEGER'
                elif column_types[i] == 'TEXT' and is_date(value):
                    column_types[i] = 'DATE'
                elif column_types[i] == 'TEXT' and is_bool(value):
                        column_types[i] = 'BOOLEAN'
                elif column_types[i] == 'TEXT' and is_float(value):
                        column_types[i] == 'REAL'

    return column_names, column_types


def try_table_creation(tableName, url) -> bool: 
    try:
        _, conn = start_connection()
        cur = conn.cursor() 

        col_names, col_types = get_csv_info(url)

        columns = [f'"{col_name}" {col_type}' for col_name, col_type in zip(col_names, col_types)]

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {tableName} (
            {', '.join(columns)}
        )
        """
        
        print(col_names)
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e:
        raise psycopg2.Error(f"{e}")
        return False 