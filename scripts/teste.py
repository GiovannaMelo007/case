import pandas as pd
import numpy as np

def testar_razao(df):
    print("\n Verificando registros aleatorios da razão População / Empresas\n")
    for _, row in df.sample(5).iterrows():
        expected = row['Populacao_38_58'] / row['Empresas_Ativas']
        atual = row['Razao']
        print(f"UF: {row['UF']} | ANO: {row['ANO']} | Esperado: {expected:.4f} | Calculado: {atual:.4f}")
        assert np.isclose(expected, atual), "Erro no calculo"
    populacao = df.iloc[0]['Populacao_38_58']
    empresas = df.iloc[0]['Empresas_Ativas']
    razao_calculada = populacao / empresas
    print(f"\n Valor esperado: {razao_calculada:.4f} | Valor no DataFrame: {df.iloc[0]['Razao']:.4f}")
    print("  sucesso com os teste")

if __name__ == "__main__":
    df = pd.read_csv("data/df_completo.csv")
    testar_razao(df)
