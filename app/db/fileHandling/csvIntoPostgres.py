import psycopg2 
from psycopg2 import sql  
import csv
from db.connection.connection import start_connection
from db.connection.tableHandlers import create_table
from db.fileHandling.typechecker.checker import sqlTypeReturn, convert_to_iso_date
from dateutil.parser import parse

def is_date(string):
    try:
        parse(string)
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
                if sqlTypeReturn(value) == "UKNOWN":
                    raise TypeError("Not a supported variable type")
                column_types[i] = sqlTypeReturn(value)

    with open(url, 'r') as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader) 
        
        data = []
        for row in reader:
            for index, value in enumerate(row):
                if sqlTypeReturn(value) == "DATE":
                    row[index] = convert_to_iso_date(value)
            data.append(row)

    return column_names, column_types, data

def try_table_creation(tableName : str, url : str, username, password) -> bool: 
    try:
        _, conn = start_connection(username, password)
        cur = conn.cursor() 

        col_names, col_types, data = get_csv_info(url)

        columns_for_creation = [f'"{col_name}" {col_type}' for col_name, col_type in zip(col_names, col_types)]
        columns_for_insertion = [f'"{col_name}"' for col_name in col_names]

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {tableName} (
            {', '.join(columns_for_creation)}
        )
        """
        cur.execute(create_table_query)
        conn.commit()

        insertion_query = f"""
        INSERT INTO {tableName} 
        (
            {', '.join(columns_for_insertion)}
        )
        VALUES
        {", ".join(["(" + ", ".join([f"'{value}'" if value != "" else 'NULL' for value in row]) + ")" for row in data])}
        """
        cur.execute(insertion_query)
        conn.commit()

        cur.close()
        conn.close()
        return True 
    except psycopg2.Error as e:
        raise psycopg2.Error(f"{e}")
        return False 
    