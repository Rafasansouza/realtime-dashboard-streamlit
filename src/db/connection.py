from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carrega o arquivo .env automaticamente
load_dotenv()

# Busca as variáveis
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    # Lembre de ajustar a URL para o seu banco (no meu foi com PostgreSQL)
    url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)
    return engine.connect()
