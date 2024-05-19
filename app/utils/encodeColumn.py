from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder

def encode_column(df, col, encoder):
    if encoder == "Label Encoder":
        label_encoder = LabelEncoder()
        df[col] = label_encoder.fit_transform(df[col])
    elif encoder == "One-Hot Encoder":
        one_hot_encoder = OneHotEncoder(sparse=False)
        encoded_column = one_hot_encoder.fit_transform(df[[col]])
        encoded_df = pd.DataFrame(encoded_column, columns=one_hot_encoder.get_feature_names_out([col]))
        df = pd.concat([df, encoded_df], axis=1)
        df.drop(columns=[col], inplace=True)
    elif encoder == "Ordinal Encoder":
        ordinal_encoder = OrdinalEncoder()
        df[col] = ordinal_encoder.fit_transform(df[[col]])