import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
def carregar_dados(arquivo_csv):
    """Carrega e processa os dados , já com a razao calculada"""
    try:
        df_completo = pd.read_csv(arquivo_csv)
        print("Arquivo df_completo.csv carregado com sucesso.")
        print(f"Colunas detectadas: {list(df_completo.columns)}")
    except Exception as e:
        raise ValueError(f"Erro ao abrir o arquivo df_completo.csv: {e}")
    return df_completo
def projetar_razao(df_completo, regiao, anos_futuros=[2021, 2022]):
    """Projeta a razão para anos futuros usando regressão linear."""
    subset = df_completo[df_completo['UF'] == regiao].copy()
    X = subset[['ANO']]
    y = subset['Razao']
    #  modelo
    modelo = LinearRegression()
    modelo.fit(X, y)
    # calculando   para avaliar a qualidade do modelo
    r2 = modelo.score(X, y)
    print(f"{regiao}: R² = {r2:.2f}")
    #  previsões pra os anos futuros
    previsoes = {}
    for ano in anos_futuros:
        previsoes[ano] = modelo.predict([[ano]])[0]
    
    return previsoes, r2
def visualizar_projecao(df_completo, regiao, previsoes):
    """Visualiza a projeção da razão para anos futuros"""
    subset = df_completo[df_completo['UF'] == regiao]
    plt.figure(figsize=(10, 6))
    plt.plot(subset['ANO'], subset['Razao'], label='Razão histórica', color='b', marker='o')
    anos_futuros = list(previsoes.keys())
    razoes_futuras = list(previsoes.values())
    plt.scatter(anos_futuros, razoes_futuras, color='r', label='Previsões 2021 e 2022', zorder=5)
    
    #  grafico
    plt.title(f'Projeção da Razão para {regiao}')
    plt.xlabel('Ano')
    plt.ylabel('Razão População / Empresas Ativas')
    plt.legend()
    plt.grid(True)
    plt.show()

def analise_temporal(arquivo_csv, regiao='Nordeste', anos_futuros=[2021, 2022]):
    """Função principal para análise temporal"""
    df_completo = carregar_dados(arquivo_csv)
    previsoes, r2 = projetar_razao(df_completo, regiao, anos_futuros)
    print(f"Previsões para {regiao} em {anos_futuros}: {previsoes}")
    visualizar_projecao(df_completo, regiao, previsoes) 
    return previsoes, r2
