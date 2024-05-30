import psycopg2 
from psycopg2 import sql  
import csv
from db.connection.connection import start_connection
from db.connection.tableHandlers import create_table
from db.fileHandling.typechecker.checker import sqlTypeReturn, convert_to_iso_timestamp
from db.handlers.handlers import select_all_cols
from dateutil.parser import parse

def is_date(string: str) -> bool:
    try:
        parse(string)
        return True
    except ValueError:
        return False

def get_csv_info(url: str):
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
                print(i)
                column_types[i] = sqlTypeReturn(value)

    with open(url, 'r') as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader) 
        
        data = []
        for row in reader:
            for index, value in enumerate(row):
                if sqlTypeReturn(value) == "TIMESTAMP":
                    row[index] = convert_to_iso_timestamp(value)
            data.append(row)

    return column_names, column_types, data

def try_table_creation(tableName : str, url : str) -> bool: 
    try:
        _, conn = start_connection()
        cur = conn.cursor() 

        col_names, col_types, data = get_csv_info(url)

        print(col_names, col_types)

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
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return False
 

def search_primary_key(tableName: str):
    try:
        _, conn = start_connection()
        cur = conn.cursor() 

        all_cols, err = select_all_cols(tableName)
        if err: 
            return None, err 
        candidates = []

        for col in all_cols: 
            query = (f"""
            SELECT 
            CASE 
                WHEN COUNT(*) = COUNT(DISTINCT "{col}") THEN 'yes'
                ELSE 'no'
            END AS result
            FROM {tableName};
            """)

            cur.execute(query)
            result = cur.fetchall()
            print(result)
            if result[0][0] == 'yes':
                candidates.append(col)
            
        cur.close()
        conn.close()
        return candidates, None
        
    except psycopg2.Error as e:
        return None, e

def turn_column_into_primary_key(tableName: str, column: str) -> bool:
    try:
        _, conn = start_connection()
        cur = conn.cursor()

        cur.execute(f"""SELECT MAX("{column}") FROM {tableName}""")
        max_value = cur.fetchone()[0]

        starting_value = max_value + 1 if max_value is not None else 1

        query = f"""
        ALTER TABLE {tableName}
        ADD PRIMARY KEY ("{column}");
        """
        cur.execute(query)

        cur.execute(f"""CREATE SEQUENCE {tableName}_pkey_seq OWNED BY {tableName}."{column}";
                        SELECT setval('{tableName}_pkey_seq', coalesce(max("{column}"), 0) + 1, false) FROM {tableName};
                        ALTER TABLE {tableName} ALTER COLUMN "{column}" SET DEFAULT nextval('{tableName}_pkey_seq')""")

        conn.commit()
        cur.close()
        conn.close()

        return True

    except psycopg2.Error as e:
        return False