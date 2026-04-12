import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection

def test_database_connection():
    """Probar conexión a base de datos"""
    print("🧪 Probando conexión a base de datos...")
    
    db = DatabaseConnection()
    if db.connect():
        print("✅ Conexión exitosa")
        db.close()
        return True
    else:
        print("❌ Fallo en conexión")
        return False

if __name__ == "__main__":
    test_database_connection()