import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

def apply_dt(dataframe, target, random_state, test_size):
    try:
        df = dataframe.copy()
        df = df.dropna()

        X = df.drop(columns = [target], axis=1)  
        y = df[target]  
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        clf = DecisionTreeClassifier(random_state=42)

        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cr = classification_report(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        tree = clf.tree_
        gini = tree.impurity
        return clf, accuracy, f1, cr, gini, cm, None
    except Exception as e: 
        return None, None, None, None, None, None,e
