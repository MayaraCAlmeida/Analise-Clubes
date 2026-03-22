# testa conexão com o postgres via .env

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

try:
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).fetchone()[0]
        print("conectado:", version)
except Exception as e:
    print("erro:", e)
