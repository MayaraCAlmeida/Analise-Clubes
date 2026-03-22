# gera KPIs de faturamento a partir do CSV e salva na pasta de saída

import os
import pandas as pd

INPUT_PATH = os.getenv("INPUT_CSV", "./data/faturamento_padronizado.csv")
OUTPUT_DIR  = os.getenv("OUTPUT_DIR", "./data/kpis")


def calcular_cagr(g):
    g = g.sort_values("ano")
    if g["ano"].nunique() < 2:
        return None
    anos = g["ano"].nunique() - 1
    return (g["faturamento"].iloc[-1] / g["faturamento"].iloc[0]) ** (1 / anos) - 1


def main():
    try:
        df = pd.read_csv(INPUT_PATH)
    except Exception as e:
        print("erro ao carregar CSV:", e)
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    kpi_total_clube  = df.groupby("clube")["faturamento"].sum().reset_index()
    kpi_total_estado = df.groupby("estado")["faturamento"].sum().reset_index()
    kpi_media_anual  = df.groupby("clube")["faturamento"].mean().reset_index()

    df_sorted = df.sort_values(["clube", "ano"])
    df_sorted["crescimento_yoy"] = df_sorted.groupby("clube")["faturamento"].pct_change()

    kpi_cagr = (
        df.groupby("clube", group_keys=False)
        .apply(lambda g: calcular_cagr(g.drop(columns=["clube"])))
        .reset_index(name="cagr")
    )

    kpi_total_clube.to_csv(os.path.join(OUTPUT_DIR, "kpi_total_clube.csv"),   index=False)
    kpi_total_estado.to_csv(os.path.join(OUTPUT_DIR, "kpi_total_estado.csv"), index=False)
    kpi_media_anual.to_csv(os.path.join(OUTPUT_DIR, "kpi_media_anual.csv"),   index=False)
    df_sorted.to_csv(os.path.join(OUTPUT_DIR, "kpi_yoy.csv"),                 index=False)
    kpi_cagr.to_csv(os.path.join(OUTPUT_DIR, "kpi_cagr.csv"),                 index=False)

    print(f"KPIs salvos em {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
