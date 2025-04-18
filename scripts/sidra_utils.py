import pandas as pd
import numpy as np
def processar_dados_empresas(arquivo_csv, df_populacao_final):
    """Carregamento, Filtragem e Transformação dos Dados do SIDRA para Empresas Ativas,
    e cálculo da razão com os dados populacionais (faixa etária 38-58 anos)"""
    try:
        df_sidra = pd.read_csv(arquivo_csv, sep=',')
        print("Arquivo SIDRA carregado com sucesso.")
        print(f"Colunas detectadas: {list(df_sidra.columns)}")
    except Exception as e:
        raise ValueError(f"Erro ao abrir o arquivo SIDRA: {e}")
    df_sidra.columns = df_sidra.iloc[0]  # colocando a primeira linha como colunas
    df_sidra = df_sidra[1:].reset_index(drop=True)  # removendo a primeira linha
    # renomeando as colunas  
    df_sidra = df_sidra[['Grande Região', 'Ano', 'Faixas de pessoal ocupado', 'Valor']].rename(columns={
        'Grande Região': 'UF','Ano': 'ANO','Faixas de pessoal ocupado': 'Faixa_Pessoal','Valor': 'Empresas_Ativas'})
    # convertendo 'ANO' para numerico e limpando os dados de 'Empresas_Ativas'
    df_sidra['ANO'] = pd.to_numeric(df_sidra['ANO'], errors='coerce')
    # filtrando 
    df_filtrado = df_sidra.query("Faixa_Pessoal == 'Total' and ANO >= 2007 and ANO <= 2020")
    df_filtrado['Empresas_Ativas'] = pd.to_numeric(df_filtrado['Empresas_Ativas'].replace('-', '0').str.replace('.', '', regex=False), errors='coerce').fillna(0).astype(int)
    # juntando os dados do SIDRA com IBGE
    df_completo = pd.merge(df_filtrado, df_populacao_final, on=['UF', 'ANO'], how='inner')
    # calculando  razao entre populacao e empresas ativas
    df_completo['Razao'] = df_completo['Populacao_38_58'] / df_completo['Empresas_Ativas']
    df_completo['Razao'] = df_completo['Razao'].replace([np.inf, -np.inf], np.nan)
    return df_completo
