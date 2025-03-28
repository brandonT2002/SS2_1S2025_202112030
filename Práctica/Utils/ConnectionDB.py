import pyodbc
from dotenv import load_dotenv
import os
load_dotenv()

# === CONEXION DB ===
def connect_to_db():
    try:
        connection = pyodbc.connect(
            f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')}"
        )
        print("✅ Conexión a la base de datos establecida.")
        return connection
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None
