import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class DatabaseConnection:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Conectar a la base de datos BioDash"""
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=3306
            )
            print("✅ Conectado a base de datos BioDash")
            return True
        except Exception as e:
            print(f"❌ Error conectando a BD: {e}")
            return False
    
    def close(self):
        """Cerrar conexión"""
        if self.connection:
            self.connection.close()
    
    def get_connection(self):
        """Obtener conexión activa"""
        return self.connection