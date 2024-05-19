import pandas as pd 
from db.handlers.handlers import select_all_rows, select_all_cols

def turn_db_into_dataframe(tableName):
    cols = select_all_cols(tableName)
    rows = select_all_rows(tableName)[0]

    print(len(rows),"\n", len(cols))
    df = pd.DataFrame(rows, columns = cols)

    return df 
