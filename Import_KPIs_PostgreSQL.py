# sobe os CSVs de KPI pro postgres

import os
import pandas as pd
import psycopg2

base_path = r"CAMINHO/DA/PASTA/KPIs"

files = {
    "kpi_total_clube":  "kpi_total_clube.csv",
    "kpi_total_estado": "kpi_total_estado.csv",
    "kpi_media_anual":  "kpi_media_anual.csv",
    "kpi_cagr":         "kpi_cagr.csv",
    "kpi_yoy":          "kpi_yoy.csv",
}

dfs = {key: pd.read_csv(os.path.join(base_path, f)) for key, f in files.items()}

try:
    conn = psycopg2.connect(
        dbname="SEU_BANCO", user="SEU_USUARIO", password="SUA_SENHA",
        host="SEU_HOST", port="SUA_PORTA"
    )
    cur = conn.cursor()

    for _, row in dfs["kpi_total_clube"].iterrows():
        cur.execute("INSERT INTO kpi_total_clube (clube, total_faturamento) VALUES (%s, %s)",
                    (row["clube"], row["total_faturamento"]))

    for _, row in dfs["kpi_total_estado"].iterrows():
        cur.execute("INSERT INTO kpi_total_estado (estado, faturamento) VALUES (%s, %s)",
                    (row["estado"], row["faturamento"]))

    for _, row in dfs["kpi_media_anual"].iterrows():
        cur.execute("INSERT INTO kpi_media_anual (clube, faturamento) VALUES (%s, %s)",
                    (row["clube"], row["faturamento"]))

    for _, row in dfs["kpi_cagr"].iterrows():
        cur.execute("INSERT INTO kpi_cagr (clube, cagr) VALUES (%s, %s)",
                    (row["clube"], row["cagr"]))

    for _, row in dfs["kpi_yoy"].iterrows():
        cur.execute("INSERT INTO kpi_yoy (clube, estado, ano, faturamento, yoy) VALUES (%s, %s, %s, %s, %s)",
                    (row["clube"], row["estado"], row["ano"], row["faturamento"], row["yoy"]))

    conn.commit()
    print("feito")

except Exception as e:
    print("erro:", e)

finally:
    if "conn" in locals() and conn:
        cur.close()
        conn.close()
