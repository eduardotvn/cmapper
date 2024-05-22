from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
import pandas as pd 
from sklearn.cluster import KMeans


def apply_pca(dataframe, scaler_option, num_components):
    try:
        if scaler_option == "MinMax":
            scaler = MinMaxScaler()
        elif scaler_option == "Standard":
            scaler = StandardScaler()
        elif scaler_option == "MaxAbs":
            scaler = MaxAbsScaler()

        df = dataframe.dropna()
        scaled_data = scaler.fit_transform(df)

        pca = PCA(n_components=num_components)
        pca_result = pca.fit_transform(scaled_data)

        pca_df = pd.DataFrame(data=pca_result, columns=[f'PC{i+1}' for i in range(num_components)])

        evr = pca.explained_variance_ratio_

        return pca_df, evr, None 
    except Exception as e: 
        print(e)
        return None, None, e 


def apply_kmeans(pca_dataframe, clusters):

    kmeans = KMeans(n_clusters=clusters)  
    kmeans.fit(pca_dataframe)
    pca_dataframe['Clusters'] = kmeans.labels_

    return pca_dataframe

def elbow_method(pca_dataframe):
    wcss = []
    k_values = range(1, 11)  

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(pca_dataframe)
        wcss.append(kmeans.inertia_)

    return wcss, k_values