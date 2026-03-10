"""
Script para enviar o arquivo CSV completo para a tabela no PostgreSQL.

Funcionalidades:
- Lê o CSV informado via variável de ambiente;
- Conecta ao PostgreSQL usando variáveis de ambiente;
- Envia os dados para a tabela informada;
- Inclui tratamento de erros e mensagens claras.

"""

import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def main():

    # VARIÁVEIS DE AMBIENTE
    CSV_PATH = os.getenv("CSV_PATH")
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_PORT = os.getenv("PG_PORT", "5432")
    PG_DATABASE = os.getenv("PG_DATABASE")
    TABLE_NAME = os.getenv("TABLE_NAME", "faturamento_total")

    # Verificar variáveis obrigatórias
    required = {
        "CSV_PATH": CSV_PATH,
        "PG_USER": PG_USER,
        "PG_PASSWORD": PG_PASSWORD,
        "PG_DATABASE": PG_DATABASE,
    }

    missing = [var for var, value in required.items() if value is None]

    if missing:
        print(f"❌ ERRO: Variáveis de ambiente ausentes: {', '.join(missing)}")
        print("Configure-as no arquivo .env antes de rodar o script.")
        return

    # LEITURA DO CSV
    print("📥 Lendo arquivo CSV...")

    try:
        df = pd.read_csv(CSV_PATH)
        print(f"✔ CSV carregado com sucesso! {df.shape[0]} linhas.")
    except Exception as e:
        print(f"❌ ERRO ao ler CSV: {e}")
        return

    # CONEXÃO COM O POSTGRES
    print("🔌 Conectando ao PostgreSQL...")

    engine_url = (
        f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}"
        f"@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    )

    try:
        engine = create_engine(engine_url)
        print("✔ Conexão estabelecida!")
    except SQLAlchemyError as e:
        print(f"❌ ERRO ao conectar ao banco: {e}")
        return

    # UPLOAD PARA O BANCO
    print("📤 Enviando dados ao banco...")

    try:
        df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
        print(f"🎉 Upload concluído! Tabela '{TABLE_NAME}' atualizada.")
    except Exception as e:
        print(f"❌ ERRO ao enviar dados: {e}")


if __name__ == "__main__":
    main()
