from dateutil.parser import parse
from datetime import datetime

def convert_to_iso_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d-%m-%Y")
        iso_date = parsed_date.strftime("%Y-%m-%d")
        return iso_date
    except ValueError:
        return None

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

def sqlTypeReturn(v) -> str:

    if v.isdigit():
        return "INTEGER"
    elif is_date(v):
        return "DATE"
    elif is_float(v):
        return "REAL"
    elif is_bool(v): 
        return "BOOLEAN"
    elif type(v) == str: 
        return "TEXT"
    else: 
        return "UNKNOWN"