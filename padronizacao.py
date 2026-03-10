import pandas as pd
import os
import unicodedata

# Caminho da pasta onde está o script e os arquivos
BASE_DIR = r"SEU/CAMINHO/AQUI"

# Arquivo de entrada
INPUT_FILE = os.path.join(BASE_DIR, "faturamento_limpo.csv")

# Arquivo de saída
OUTPUT_FILE = os.path.join(BASE_DIR, "faturamento_padronizado.csv")

print("Lendo arquivo:", INPUT_FILE)

# Função simples para remover acentos, tios e cedilha
def remover_acentos(texto):
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return texto

# Lê o CSV
df = pd.read_csv(INPUT_FILE)

# Padroniza nomes das colunas
df.columns = (
    df.columns
    .str.lower()
    .map(remover_acentos)     # remove acento agudo, circunflexo, til e ç
    .str.replace(" ", "_")
)

# Remove valores de faturamento com símbolos e transforma em número
if "faturamento" in df.columns:
    df["faturamento"] = (
        df["faturamento"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

# Salva o novo CSV
df.to_csv(OUTPUT_FILE, index=False)

print("Arquivo padronizado gerado com sucesso!")
print("Local:", OUTPUT_FILE)