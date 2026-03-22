# lê o CSV e sobe pra tabela no postgres

import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def main():
    CSV_PATH    = os.getenv("CSV_PATH")
    PG_USER     = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_HOST     = os.getenv("PG_HOST", "localhost")
    PG_PORT     = os.getenv("PG_PORT", "5432")
    PG_DATABASE = os.getenv("PG_DATABASE")
    TABLE_NAME  = os.getenv("TABLE_NAME", "faturamento_total")

    missing = [k for k, v in {"CSV_PATH": CSV_PATH, "PG_USER": PG_USER,
               "PG_PASSWORD": PG_PASSWORD, "PG_DATABASE": PG_DATABASE}.items() if not v]
    if missing:
        print(f"variáveis ausentes: {', '.join(missing)}")
        return

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        print("erro ao ler CSV:", e)
        return

    try:
        engine = create_engine(
            f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
        )
    except SQLAlchemyError as e:
        print("erro ao conectar:", e)
        return

    try:
        df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
        print(f"tabela '{TABLE_NAME}' atualizada com {len(df)} linhas")
    except Exception as e:
        print("erro ao enviar dados:", e)


if __name__ == "__main__":
    main()
