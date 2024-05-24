import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def apply_lnr(dataframe, target, test_size, random_state):
    try:
        df = dataframe.copy()
        X = df.drop(columns=[target])
        y = df[target]    

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return model, mse, r2, X_test, y_test, y_pred, None
    except Exception as e: 
        return None, None, None, None, None, None, e