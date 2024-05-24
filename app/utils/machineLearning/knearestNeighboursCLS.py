import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def apply_knn(dataframe, target, random_state, test_size, n_neighbors):
    try:
        df = dataframe.copy()
        X = df.drop(columns = [target])
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        knn = KNeighborsClassifier(n_neighbors=3)

        knn.fit(X_train, y_train)

        y_pred = knn.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        return knn, accuracy, report, cm, None
        
    except Exception as e:
        return None, None, None, None, e