import pandas as pd
import matplotlib.pyplot as plt

def analise_temporal_media_movel(df_completo, regiao='Nordeste', janela=3, anos_futuros=[2021, 2022]):
    """Análise temporal usando média móvel simples"""
    
    subset = df_completo[df_completo['UF'] == regiao].copy()# filtro de regiao desejada
    subset = subset.sort_values('ANO')
    subset['Media_Movel'] = subset['Razao'].rolling(window=janela).mean()# calculo da media movel da razão
    ultima_media = subset['Media_Movel'].dropna().iloc[-1]
    previsoes = {ano: ultima_media for ano in anos_futuros}
    print(f"Previsões com média móvel ({janela} anos) para {regiao}: {previsoes}")

    # grafico
    plt.figure(figsize=(10, 6))
    plt.plot(subset['ANO'], subset['Razao'], label='Razão Original', marker='o')
    plt.plot(subset['ANO'], subset['Media_Movel'], label=f'Média Móvel ({janela} anos)', linestyle='--')
    plt.scatter(anos_futuros, list(previsoes.values()), color='red', label='Previsões Futuras', zorder=5)
    plt.title(f'Projeção por Média Móvel - {regiao}')
    plt.xlabel('Ano')
    plt.ylabel('Razão População / Empresas Ativas')
    plt.legend()
    plt.grid(True)
    plt.show()
    return previsoes
