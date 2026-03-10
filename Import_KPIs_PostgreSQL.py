import pandas as pd
import psycopg2
import os

# Caminho da pasta onde estão os CSVs (substitua pelo seu)
base_path = r"CAMINHO/DA/PASTA/KPIs"

# Lista dos arquivos CSV
files = {
    "kpi_total_clube": "kpi_total_clube.csv",
    "kpi_total_estado": "kpi_total_estado.csv",
    "kpi_media_anual": "kpi_media_anual.csv",
    "kpi_cagr": "kpi_cagr.csv",
    "kpi_yoy": "kpi_yoy.csv",
}

# Lendo os CSVs
dfs = {}
for key, filename in files.items():
    full_path = os.path.join(base_path, filename)
    print(f"Lendo {filename}...")
    dfs[key] = pd.read_csv(full_path)

# Conexão com o PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="SEU_BANCO",
        user="SEU_USUARIO",
        password="SUA_SENHA",
        host="SEU_HOST",
        port="SUA_PORTA",
    )
    cur = conn.cursor()
    print("\nConexão com PostgreSQL bem-sucedida!\n")

    # Inserindo KPI Total por Clube
    print("Inserindo KPI Total por Clube...")
    for _, row in dfs["kpi_total_clube"].iterrows():
        cur.execute(
            "INSERT INTO kpi_total_clube (clube, total_faturamento) VALUES (%s, %s)",
            (row["clube"], row["total_faturamento"]),
        )

    print("Inserindo KPI Total por Estado...")
    for _, row in dfs["kpi_total_estado"].iterrows():
        cur.execute(
            "INSERT INTO kpi_total_estado (estado, faturamento) VALUES (%s, %s)",
            (row["estado"], row["faturamento"]),
        )

    print("Inserindo KPI Média Anual...")
    for _, row in dfs["kpi_media_anual"].iterrows():
        cur.execute(
            "INSERT INTO kpi_media_anual (clube, faturamento) VALUES (%s, %s)",
            (row["clube"], row["faturamento"]),
        )

    print("Inserindo KPI CAGR...")
    for _, row in dfs["kpi_cagr"].iterrows():
        cur.execute(
            "INSERT INTO kpi_cagr (clube, cagr) VALUES (%s, %s)",
            (row["clube"], row["cagr"]),
        )

    print("Inserindo KPI YoY...")
    for _, row in dfs["kpi_yoy"].iterrows():
        cur.execute(
            """
            INSERT INTO kpi_yoy (clube, estado, ano, faturamento, yoy)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (row["clube"], row["estado"], row["ano"], row["faturamento"], row["yoy"]),
        )

    conn.commit()
    print("KPI YoY importado com sucesso!")

except Exception as e:
    print("ERRO:", e)

finally:
    if 'conn' in locals() and conn:
        cur.close()
        conn.close()