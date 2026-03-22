import pandas as pd

df = pd.read_csv("nome_do_arquivo.csv")

df["ano"] = df["ano"].astype(int)
df["faturamento"] = (
    df["faturamento"].astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

df = df.sort_values(["ano", "faturamento"], ascending=[True, False])
df.to_csv("nome_do_arquivo_limpo.csv", index=False)
