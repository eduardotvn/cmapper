from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import pandas as pd 

def encode_column(df, col, encoder):
    if encoder == "Label Encoder":
        label_encoder = LabelEncoder()
        df[col] = label_encoder.fit_transform(df[col])
        return df
    elif encoder == "One-Hot Encoder":
        one_hot_encoder = OneHotEncoder(sparse_output=False)
        encoded_column = one_hot_encoder.fit_transform(df[[col]])
        encoded_df = pd.DataFrame(encoded_column, columns=one_hot_encoder.get_feature_names_out([col]))
        df = pd.concat([df, encoded_df], axis=1)
        df = df.drop(columns=[col])
        return df
    elif encoder == "Ordinal Encoder":
        ordinal_encoder = OrdinalEncoder()
        df[col] = ordinal_encoder.fit_transform(df[[col]])
        return df