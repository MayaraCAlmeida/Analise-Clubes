import pandas as pd

# CAMINHO DO ARQUIVO DE ENTRADA
df = pd.read_csv("nome_do_arquivo.csv")

# Garantir tipos
df["ano"] = df["ano"].astype(int)
df["faturamento"] = (
    df["faturamento"]
    .astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

# ORDENAR DADOS POR ANO E FATURAMENTO
df = df.sort_values(["ano", "faturamento"], ascending=[True, False])

# PASTA DE SAIDA
df.to_csv("nome_do_arquivo_limpo.csv", index=False)

print("Arquivo limpo gerado!")
