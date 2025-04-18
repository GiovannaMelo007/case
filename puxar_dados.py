'''import requests
import json

# URL formatada no estilo desejado
url = 'https://apisidra.ibge.gov.br/values/t/1757/n2/all/v/410/p/2007-2022/c319/104029'

# Requisição GET
response = requests.get(url)

# Verifica o status
if response.status_code == 200:
    data_json = response.json()

    # Exibe o JSON formatado
    print(json.dumps(data_json, indent=2, ensure_ascii=False))
else:
    print(f"Erro na requisição: {response.status_code}")
'''

import requests
import time
import json
import csv
# colunas que devem ter na tabela
COLUNAS_ESPERADAS = ['NC', 'NN', 'MC', 'MN', 'V','D1C', 'D1N', 'D2C', 'D2N','D3C', 'D3N', 'D4C', 'D4N']
def montar_url(tabela, variavel, nivel_territorial, unidade_territorial, periodo, classificacao=None):
    base_url = "https://apisidra.ibge.gov.br/values"
    url = f"{base_url}/t/{tabela}/n{nivel_territorial}/{unidade_territorial}/v/{variavel}/p/{periodo}"
    if classificacao:
        url += f"/c319/{classificacao}"
    return url
#  requisicao com 3 tentativas
def requisitar_dados(url, tentativas=3, intervalo=2):
    for tentativa in range(tentativas):
        try:
            resposta = requests.get(url, timeout=10)
            if resposta.status_code == 200:
                return resposta.json()
            else:
                print(f"Erro {resposta.status_code} ao acessar a API")
        except requests.exceptions.RequestException as erro:
            print(f"Tentativa {tentativa + 1} falhou: {erro}")
        time.sleep(intervalo)
    return None

# extraiindo dados da API
def extrair_dados_ibge(tabela, variavel, nivel, unidade, periodo, classificacao=None):
    url = montar_url(tabela, variavel, nivel, unidade, periodo, classificacao)
    print("URL gerada:", url)
    dados = requisitar_dados(url)
    if not dados:
        print("ERRO, nao foi possivel obter os dados da API.")
        return []
    cabecalho = list(dados[0].keys())
    colunas_faltando = [coluna for coluna in COLUNAS_ESPERADAS if coluna not in cabecalho]
    if colunas_faltando:
        print("Colunas ausentes:", colunas_faltando)
    else:
        print("Todas as colunas esperadas estão presentes.")
    quantidade_linhas = len(dados) - 1  
    print("Total de linhas de dados:", quantidade_linhas)
    return dados

# salvar  em csv
def salvar_csv(dados, nome_arquivo):
    if len(dados) < 2:
        print("Nenhum dado para salvar.")
        return
    cabecalho = list(dados[0].keys())

    try:
        with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.DictWriter(arquivo_csv, fieldnames=cabecalho)
            writer.writeheader()
            for linha in dados[1:]:  
                writer.writerow(linha)
        print(f"Arquivo CSV salvo como: {nome_arquivo}")
    except Exception as erro:
        print("Erro ao salvar CSV:", erro)
if __name__ == "__main__":
    tabela = '1757'
    variavel = '410'
    nivel = '2'  
    unidade = 'all'
    periodo = '2007-2022'
    classificacao = '104029' 
    dados_json = extrair_dados_ibge(tabela, variavel, nivel, unidade, periodo, classificacao)
    if dados_json:
        salvar_csv(dados_json, "dados_empresas_ativas_grande_regiao_2007_2022.csv")
