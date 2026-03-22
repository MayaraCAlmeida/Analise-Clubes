# padroniza colunas e formata faturamento do CSV

import os
import unicodedata
import pandas as pd

INPUT_FILE  = os.path.join(r"SEU/CAMINHO/AQUI", "faturamento_limpo.csv")
OUTPUT_FILE = os.path.join(r"SEU/CAMINHO/AQUI", "faturamento_padronizado.csv")


def remover_acentos(texto):
    return "".join(
        ch for ch in unicodedata.normalize("NFD", texto)
        if unicodedata.category(ch) != "Mn"
    )


df = pd.read_csv(INPUT_FILE)

df.columns = df.columns.str.lower().map(remover_acentos).str.replace(" ", "_")

if "faturamento" in df.columns:
    df["faturamento"] = (
        df["faturamento"].astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

df.to_csv(OUTPUT_FILE, index=False)
print(f"salvo em {OUTPUT_FILE}")
