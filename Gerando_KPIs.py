"""
Script para gerar KPIs de faturamento a partir do CSV.

KPIs gerados:
- Total por clube
- Total por estado
- Média anual por clube
- YoY (crescimento ano a ano)
- CAGR (crescimento anual composto)

Saída: arquivos CSV salvos na pasta definida por variável de ambiente.
"""

import os
import pandas as pd


# Leitura das variáveis de ambiente

INPUT_PATH = os.getenv("INPUT_CSV", "./data/faturamento_padronizado.csv")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./data/kpis")


# Função auxiliar para garantir diretório de saída


def ensure_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Pasta criada: {path}")


# Cálculo do CAGR


def calcular_cagr(g):
    g = g.sort_values("ano")

    if g["ano"].nunique() < 2:
        return None

    valor_inicial = g["faturamento"].iloc[0]
    valor_final = g["faturamento"].iloc[-1]
    anos = g["ano"].nunique() - 1

    return (valor_final / valor_inicial) ** (1 / anos) - 1


# Execução principal


def main():

    print("📂 Lendo arquivo de entrada:", INPUT_PATH)

    try:
        df = pd.read_csv(INPUT_PATH)
    except Exception as e:
        print("❌ Erro ao carregar CSV:", e)
        return

    # Garantir pasta de saída
    ensure_output_dir(OUTPUT_DIR)

    # 1. Total por clube
    kpi_total_clube = df.groupby("clube")["faturamento"].sum().reset_index()

    # 2. Total por estado
    kpi_total_estado = df.groupby("estado")["faturamento"].sum().reset_index()

    # 3. Média anual por clube
    kpi_media_anual = df.groupby("clube")["faturamento"].mean().reset_index()

    # 4. YoY (Ano a Ano)
    df_sorted = df.sort_values(["clube", "ano"])
    df_sorted["crescimento_yoy"] = df_sorted.groupby("clube")[
        "faturamento"
    ].pct_change()

    # 5. CAGR
    kpi_cagr = (
        df.groupby("clube", group_keys=False)
        .apply(lambda g: calcular_cagr(g.drop(columns=["clube"])))
        .reset_index(name="cagr")
    )

    # Salvando arquivos
    kpi_total_clube.to_csv(os.path.join(OUTPUT_DIR, "kpi_total_clube.csv"), index=False)
    kpi_total_estado.to_csv(
        os.path.join(OUTPUT_DIR, "kpi_total_estado.csv"), index=False
    )
    kpi_media_anual.to_csv(os.path.join(OUTPUT_DIR, "kpi_media_anual.csv"), index=False)
    df_sorted.to_csv(os.path.join(OUTPUT_DIR, "kpi_yoy.csv"), index=False)
    kpi_cagr.to_csv(os.path.join(OUTPUT_DIR, "kpi_cagr.csv"), index=False)

    print("✅ KPIs gerados com sucesso!")
    print("📁 Arquivos salvos em:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
