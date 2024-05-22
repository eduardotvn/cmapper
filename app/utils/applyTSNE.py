import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler

def apply_TSNE(dataframe, num_components, scaler_option, rand_state, perplex, num_iter):
    try:
        tsne = TSNE(num_components=num_components, random_state=rand_state, perplexity=perplex, n_iter=num_iter)
        df = dataframe.copy()

        scaler = None 

        if scaler_option == "MinMax":
            scaler = MinMaxScaler()
        elif scaler_option == "Standard":
            scaler = StandardScaler()
        elif scaler_option == "MaxAbs":
            scaler = MaxAbsScaler()

        if scaler is not None: 
            df = scaler.fit_transform(df)

        tsne_results = tsne.fit_transform(df)

        tsne_df = pd.DataFrame(tsne_results, columns=[f'TSNE{i+1}' for i in range(num_components)])

        return tsne_df, None

    except Exception as e:
        
        return None, e
    
    

