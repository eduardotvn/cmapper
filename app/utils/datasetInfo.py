import pandas as pd 
from db.handlers.handlers import select_all_rows, select_all_cols

def turn_db_into_dataframe(tableName):
    cols, err = select_all_cols(tableName)
    if err:
        return 
    rows, _, err = select_all_rows(tableName)
    if err:
        return 

    df = pd.DataFrame(rows, columns = cols)

    return df 
