Projeto de Análise do Mercado Imobiliário

Este projeto tem como analisar o perfil dos consumidores do mercado imobiliário brasileiro, com foco na faixa etária predominante (38 a 58 anos), e estimar a evolução da razão entre consumidores dessa faixa etária e o número de empresas ativas por região entre 2007 e 2022.

Estrutura do Projeto
Abaixo estão descritas as funcionalidades de cada parte do código e os arquivos do projeto:

Arquivos do Projeto

ibge_utils.py: Responsável por processar os dados populacionais fornecidos pelo IBGE.

sidra_utils.py: Responsável por processar os dados sobre as empresas de construção (obtidos da API SIDRA).



Coleta dos Dados
Para coletar os dados necessários para a análise, utilizamos os seguintes fontes:

Empresas de construção: Os dados de empresas de construção foram obtidos através da API do SIDRA, especificamente da Tabela 1757, que contém informações sobre empresas ativas por região e faixa de pessoal ocupado.
Projeção populacional: A estimativa da população por faixa etária foi obtida diretamente da projeção populacional fornecida pelo IBGE, através da tabela "População por sexo e idade simples".


## Módulos Principais

### 1. 'ibge_utils.py'
**Função**: Processamento de dados populacionais do IBGE.

**Principais funcionalidades**:
- `processar_dados_populacionais(arquivo)`: 
  - Carrega arquivo Excel com dados populacionais
  - Renomeia colunas para padronização
  - Filtra população na faixa etária 38-58 anos
  - Identifica colunas de anos (2007-2030)
  - Transforma dados para formato longo
  - Remove valores inválidos e converte dados para inteiros
  - Agrupa dados por estado (UF) e ano

### 2. 'sidra_util.py'
**Função**: Processamento de dados de empresas ativas (SIDRA/IBGE).

**Principais funcionalidades**:
  - Lê CSV da Tabela 1757 do SIDRA
  - Ajusta nomes de colunas e remove cabeçalhos extras
  - Filtra dados de "Total" de pessoal ocupado (2007-2020)
  - Converte valores para inteiros
  - Realiza merge com dados populacionais
  - Calcula razão População/Empresas Ativas por estado/ano

### 3. 'analise_temporal.py'
**Função**: Análise temporal com regressão linear.

**Principais funções**:
- 'carregar_dados': Carrega CSV com razão calculada
- 'projetar_razao()': Aplica regressão linear para estimar valores futuros
- 'visualizar_projecao()': Gera gráficos com série histórica e projeções
- 'analise_temporal()': Executa fluxo completo de análise

### 4. 'analise.py'
**Função**: Análise temporal com Média Móvel.

**Principais funções**:
- analise_temporal_media_movel():
  - Aplica média móvel à série histórica
  - Projeta valores futuros baseados na tendência
  - Retorna previsões em formato de dicionário
  - Gera gráficos comparativos

### 5. 'grafico_e_cluster.py'
**Função**: Clusterização e visualização de dados.

**Principais funcionalidades**:
- Escalonamento de dados com StandardScaler
- Clusterização com K-Means (3 clusters)
- Cálculo de tendências por regressão linear (2015-2020)
- Mapeamento de clusters para regiões
- Visualização gráfica por cluster:
  - Comportamento da Razão por Cluster
  - Evolução Temporal (2015-2020)

## Fluxo de Análise

1. Processamento dos dados populacionais ('ibge_utils.py')
2. Processamento dos dados de empresas ('sidra_util.py')
3. Cálculo da razão População/Empresas
4. Análise temporal (regressão linear ou média móvel)
5. Clusterização e classificação das regiões
6. Visualização dos resultados

## Classificação de Regiões

As regiões são classificadas em:
- **Saturado**: Razão > média + desvio padrão com tendência positiva
- **Oportunidade**: Razão < média - desvio padrão OU 70% da média
- **Neutro**: Demais casos

## Requisitos

- Python 3.x
- Bibliotecas: pandas, numpy, scikit-learn, matplotlib, scipy

## Como Usar

1. Instale as dependências: 'pip install -r requirements.txt'
2. Execute os scripts na ordem:
   - Processamento de dados ('ibge_utils.py' e 'sidra_util.py')
   - Análises ('analise_temporal.py' ou 'analise.py')
   - Clusterização ('grafico_e_cluster.py')

## Saídas

- DataFrames com dados processados
- Gráficos de evolução temporal
- Classificação das regiões por cluster
