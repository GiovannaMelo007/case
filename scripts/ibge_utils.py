import pandas as pd
def processar_dados_populacionais(arquivo):
    """Carregamento, Filtragem e Transformação de Dados Populacionais por Faixa Etária (38 a 58 anos) -IBGE"""
    #carregando o arquivo
    try:
        df_pop = pd.read_excel(arquivo, engine='openpyxl')
        print(" Arquivo carregado com sucesso.")
        print(f"Colunas detectadas: {list(df_pop.columns)}")
    except Exception as e:
        raise ValueError(f"Erro ao abrir o arquivo: {e}")
   
    colunas_necessarias = {'LOCAL': 'UF', 'IDADE': 'Idade'} # renomeando as colunas que vou usar
    df_ibge = df_pop.rename(columns=colunas_necessarias)[
        list(colunas_necessarias.values()) +
        [col for col in df_pop.columns if isinstance(col, int)]]
    #vendo se tem valores únicos na coluna de idade
    print("Faixas etarias encontradas na tabela:")
    print(df_ibge['Idade'].unique())
    # filtrando  a população entre 38 e 58 anos
    try:
        df_faixa_etaria = df_ibge.query("38 <= Idade <= 58").copy()
        print(f"\n Registros filtrados nessa faixa: {len(df_faixa_etaria)}")
    except:
        df_faixa_etaria = df_ibge[(df_ibge['Idade'] >= 38) & (df_ibge['Idade'] <= 58)].copy()
    # procurando as colunas 
    colunas_ano = [col for col in df_faixa_etaria.columns 
                   if isinstance(col, int) and 2007 <= col <= 2030]    
    if not colunas_ano:
        raise ValueError(" Nenhuma coluna de ano entre 2007 e 2030 foi encontrada.")
    print(f"\n Anos encontrados: {colunas_ano}")

    # transformando os dados para o formato longo
    df_populacao = df_faixa_etaria.melt(
        id_vars=['UF', 'Idade'],value_vars=colunas_ano,var_name='ANO',value_name='Populacao')
    #limpando os dados da coluna de populacao
    def limpar_populacao(valor):
        if isinstance(valor, (int, float)):
            return int(valor)
        valor = str(valor).strip()
        if valor.replace('.', '').isdigit():
            return int(float(valor.replace('.', '')))
        return 0  # Caso o valor não seja numérico
    df_populacao['Populacao'] = df_populacao['Populacao'].apply(limpar_populacao)
    #aagrupar os dados por estado e ano e somar a população da faixa etaria
    df_final = (df_populacao.groupby(['UF', 'ANO'])['Populacao'].sum().reset_index().rename(columns={'Populacao': 'Populacao_38_58'}))

    return df_final
