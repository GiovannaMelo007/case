import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

def agrupamento_temporal(df_completo):
    # regressão linear por regiao
    projeções = []
    for regiao in df_completo['UF'].unique():
        subset = df_completo[df_completo['UF'] == regiao]
        X = subset[['ANO']]
        y = subset['Razao']
        modelo = LinearRegression().fit(X, y)
        razao_2021 = modelo.predict([[2021]])[0]
        razao_2022 = modelo.predict([[2022]])[0]
        projeções.append({'Regiao': regiao, 2021: razao_2021, 2022: razao_2022})
    # agruoando regioes 
    df_pivot = df_completo.pivot(index='UF', columns='ANO', values='Razao').fillna(0)
    kmeans = KMeans(n_clusters=3).fit(df_pivot)  # 3 grupos
    df_pivot['Cluster'] = kmeans.labels_
    media_razao = df_completo[df_completo['ANO'] >= 2015]['Razao'].mean()
    desvio_padrao = df_completo[df_completo['ANO'] >= 2015]['Razao'].std()
    classificacao_final = []
    for _, row in df_pivot.iterrows():
        regiao = row.name  
        tendencia = LinearRegression().fit(df_completo[df_completo['UF'] == regiao][['ANO']], df_completo[df_completo['UF'] == regiao]['Razao']).coef_[0]
        ultima_razao = df_completo[df_completo['UF'] == regiao]['Razao'].iloc[-1]
        #  criterios para Saturado e Oportunidade
        if ultima_razao > media_razao + desvio_padrao and tendencia > 0:
            status = "Saturado"
        elif ultima_razao < media_razao - desvio_padrao and tendencia < 0:
            status = "Oportunidade"
        elif ultima_razao < media_razao * 0.7:  
            status = "Oportunidade"
        elif tendencia > 20:  
            status = "Saturado"
        else:
            status = "Neutro"  
        classificacao_final.append({'Regiao': regiao, 'Status': status})
    df_final = pd.DataFrame(classificacao_final)
    return df_final


