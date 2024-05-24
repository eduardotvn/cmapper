from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import pandas as pd 

def encode_column(df, col, encoder):
    df[col] = df[col].str.strip()
    if encoder == "Label Encoder":
        label_encoder = LabelEncoder()
        df[col] = label_encoder.fit_transform(df[col])
        return df
    elif encoder == "One-Hot Encoder":
        df = pd.get_dummies(df, columns = [col])
        return df
    elif encoder == "Ordinal Encoder":
        ordinal_encoder = OrdinalEncoder()
        df[col] = ordinal_encoder.fit_transform(df[[col]])
        return df