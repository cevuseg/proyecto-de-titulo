# test_db.py
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Construir la URL de conexión desde el .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear motor de conexión
engine = create_engine(DATABASE_URL)

# Intentar conectar
try:
    conn = engine.connect()
    print("✅ Conexión exitosa a la base de datos PostgreSQL.")
    conn.close()
except Exception as e:
    print("❌ Error al conectar con la base de datos:")
    print(e)
