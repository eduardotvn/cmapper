import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

def apply_lda(dataframe, num_components, scaler_option, target):
    try:
        data = dataframe.copy()
        X = data.drop(columns=[target])
        print(X.columns.tolist())
        y = data[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        if scaler_option == "MinMax":
            scaler = MinMaxScaler()
        elif scaler_option == "Standard":
            scaler = StandardScaler()
        elif scaler_option == "MaxAbs":
            scaler = MaxAbsScaler()

        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        lda = LinearDiscriminantAnalysis(n_components=num_components) 
        X_train_lda = lda.fit_transform(X_train, y_train)
        X_test_lda = lda.transform(X_test)

        classifier = LogisticRegression()
        classifier.fit(X_train_lda, y_train)

        y_pred = classifier.predict(X_test_lda)

        accuracy = accuracy_score(y_test, y_pred)
        
        result = scaler.fit_transform(X)
        result = lda.fit_transform(X, y)
        result = classifier.predict(result)
        return result, accuracy, None
    except Exception as e: 
        print(e)
        return None, None, e
