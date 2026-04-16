import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection
from models.yoyosq import YoyoSQ
from models.encoder import EncoderLineal
from models.polea_conica import PoleaConica
from models.usuario import Usuario

def test_models():
    """Probar modelos de datos"""
    print("🧪 Probando modelos...")
    
    # Conectar BD
    db = DatabaseConnection()
    if not db.connect():
        print("❌ No se pudo conectar a BD")
        return False
    
    connection = db.get_connection()
    
    # Datos de prueba
    test_data = {
        'acceleration_avg': '10.5',
        'acceleration_max': '15.2',
        'velocity_avg': '8.3',
        'velocity_max': '12.1'
    }
    
    try:
        # Probar YoyoSQ
        yoyo = YoyoSQ(connection)
        yoyo_id = yoyo.save(test_data)
        print(f"✅ YoyoSQ guardado con ID: {yoyo_id}")
        
        # Probar Usuario
        usuario = Usuario(connection)
        user_id = usuario.save("Test", "User", yoyosq_id=yoyo_id)
        print(f"✅ Usuario guardado con ID: {user_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_models()