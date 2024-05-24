from dateutil.parser import parse
from datetime import datetime

def convert_to_iso_timestamp(datetime_str):
    try:
        parsed_datetime = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M:%S")
        iso_timestamp = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            parsed_datetime = datetime.strptime(datetime_str, "%d-%m-%Y")
            iso_timestamp = parsed_datetime.strftime("%Y-%m-%d")
        except ValueError:
            return None
    return iso_timestamp

def is_date(string):
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False

def is_bool(string):
    return string.lower() in ['true', 'false']

def is_float(string):
    try:
        float(string)
        return '.' in string or 'e' in string.lower()
    except ValueError:
        return False

def sqlTypeReturn(v) -> str:
    if is_bool(v):
        return "BOOLEAN"
    elif is_float(v):
        return "REAL"
    elif v.isdigit():
        return "INTEGER"
    elif is_date(v):
        return "TIMESTAMP"
    elif isinstance(v, str): 
        return "TEXT"
    else: 
        return "UNKNOWN"
