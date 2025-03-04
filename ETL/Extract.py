import pandas as pd

# === EXTRACCIÓN DE DATOS ===
def extract_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("✅ Datos extraídos con éxito.")
        return df
    except Exception as e:
        print(f"❌ Error al extraer los datos: {e}")
        return None