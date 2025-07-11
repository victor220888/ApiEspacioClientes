from config import get_connection

def test_oracle_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dual")
        result = cursor.fetchone()
        print("✅ Conexión exitosa! Resultado:", result)
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error de conexión:", e)

if __name__ == "__main__":
    test_oracle_connection()
