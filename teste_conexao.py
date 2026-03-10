from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# 🔑 Carrega as variáveis do arquivo .env
load_dotenv()

# 🗄️ Lê as credenciais do PostgreSQL a partir do .env
usuario = os.getenv("POSTGRES_USER")
senha = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST", "localhost")
porta = os.getenv("POSTGRES_PORT", "5432")
banco = os.getenv("POSTGRES_DB")

# Cria a engine de conexão
engine = create_engine(f'postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}')

# Testa a conexão
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("✅ Conexão bem-sucedida!")
        print("Versão do PostgreSQL:", result.fetchone()[0])
except Exception as e:
    print("❌ Erro ao conectar:", e)
