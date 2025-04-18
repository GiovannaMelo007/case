
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

def gerar_graficos_e_clusters(df_completo):
    df_pivot = df_completo[df_completo['ANO'].between(2007, 2020)] \
        .pivot(index='UF', columns='ANO', values='Razao') \
        .fillna(0)
    # estimar 2021 e 2022 
    projecoes = {}
    for regiao in df_pivot.index:
        dados = df_completo[(df_completo['UF'] == regiao) & (df_completo['ANO'].between(2007, 2020))]
        X = dados[['ANO']]
        y = dados['Razao']
        modelo = LinearRegression().fit(X, y)
        projecoes[regiao] = {
            2021: modelo.predict([[2021]])[0],
            2022: modelo.predict([[2022]])[0]}
    # adicionar estimativas 
    for regiao in df_pivot.index:
        df_pivot.loc[regiao, 2021] = projecoes[regiao][2021]
        df_pivot.loc[regiao, 2022] = projecoes[regiao][2022]
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_pivot)
    kmeans = KMeans(n_clusters=3, random_state=42).fit(df_scaled)
    df_pivot['Cluster'] = kmeans.labels_
    # calculando tendencias
    tendencias = []
    for regiao in df_pivot.index:
        dados = df_completo[(df_completo['UF'] == regiao) & (df_completo['ANO'].between(2007, 2020))]
        X = dados[['ANO']]
        y = dados['Razao']
        coef = LinearRegression().fit(X, y).coef_[0]
        tendencias.append(coef)
    df_pivot['Tendencia_2007_2020'] = tendencias
    df_completo['Cluster'] = df_completo['UF'].map(df_pivot['Cluster'])
    print(df_pivot[['Cluster', 'Tendencia_2007_2020']])
    for cluster in sorted(df_completo['Cluster'].unique()):
        regioes = df_completo[df_completo['Cluster'] == cluster]['UF'].unique()
        print(f"Cluster {cluster}: {', '.join(regioes)}")
    plt.figure(figsize=(12, 6))
    for cluster in df_completo['Cluster'].unique():
        subset = df_completo[df_completo['Cluster'] == cluster]
        for regiao in subset['UF'].unique():
            dados = subset[subset['UF'] == regiao]
            plt.plot(dados['ANO'], dados['Razao'], label=f"{regiao} (Cluster {cluster})")
    plt.title('Séries Temporais Agrupadas por Cluster (2007–2022)')
    plt.xlabel('Ano')
    plt.ylabel('Razão')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid()
    plt.tight_layout()
    plt.show()
    # evolucao geral
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_completo[df_completo['ANO'].between(2007, 2022)],x='ANO', y='Razao', hue='Cluster', style='UF', markers=True, dashes=False)
    plt.title('Evolução da Razão por Cluster (2007–2022)')
    plt.grid()
    plt.tight_layout()
    plt.show()

    return df_pivot






'''

def gerar_graficos_e_clusters(df_completo, df_pivot):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_pivot.iloc[:, :-1]) 
    kmeans = KMeans(n_clusters=3, random_state=42).fit(df_scaled)
    df_pivot['Cluster'] = kmeans.labels_  
    # calculo das tendencias
    tendencias = []
    for regiao in df_pivot.index:
        dados = df_completo[(df_completo['UF'] == regiao) & (df_completo['ANO'] >= 2015)]
        X = dados[['ANO']]
        y = dados['Razao']
        coef = LinearRegression().fit(X, y).coef_[0]
        tendencias.append(coef)

    df_pivot['Tendencia_2015_2020'] = tendencias
    print(df_pivot[['Cluster', 'Tendencia_2015_2020']])
    df_completo['Cluster'] = df_completo['UF'].map(df_pivot['Cluster'])
    for cluster in sorted(df_completo['Cluster'].unique()):
        regioes = df_completo[df_completo['Cluster'] == cluster]['UF'].unique()
        print(f"Cluster {cluster}: {', '.join(regioes)}")

    plt.figure(figsize=(12, 6))
    for cluster in df_completo['Cluster'].unique():
        subset = df_completo[df_completo['Cluster'] == cluster]
        for regiao in subset['UF'].unique():
            dados = subset[subset['UF'] == regiao]
            plt.plot(dados['ANO'], dados['Razao'], label=f"{regiao} (Cluster {cluster})")
    plt.title('Comportamento da Razão por Cluster')
    plt.xlabel('Ano')
    plt.ylabel('Razão')
    plt.legend()
    plt.grid()
    plt.show()
    # grafico da evolucao 
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_completo, x='ANO', y='Razao', hue='Cluster', style='UF',markers=True)
    plt.title('Evolução da Razão por Cluster (2015-2020)')
    plt.grid()
    plt.show()
'''
