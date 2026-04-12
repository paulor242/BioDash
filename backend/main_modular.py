from database.connection import DatabaseConnection
from usb_handler.usb_reader import USBHandler
from models.yoyosq import YoyoSQ
from models.encoder import EncoderLineal
from models.polea_conica import PoleaConica
from models.usuario import Usuario
import time

class BioDashCollector:
    def __init__(self):
        self.db = DatabaseConnection()
        self.usb = USBHandler()
        
    def run(self):
        """Ejecutar recolector"""
        # Conectar BD
        if not self.db.connect():
            return
        
        connection = self.db.get_connection()
        
        # Mostrar puertos
        ports = self.usb.list_ports()
        if not ports:
            print("❌ No hay puertos USB")
            return
        
        print("Puertos disponibles:")
        for i, (port, desc) in enumerate(ports):
            print(f"{i+1}. {port} - {desc}")
        
        # Seleccionar puerto
        try:
            sel = int(input("Selecciona puerto: ")) - 1
            port = ports[sel][0]
        except:
            print("❌ Selección inválida")
            return
        
        # Conectar USB
        if not self.usb.connect(port):
            return
        
        # Datos usuario
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        tipo = input("Tipo de máquina (1=yoyosq, 2=encoder, 3=polea): ")
        
        # Inicializar modelos
        yoyo = YoyoSQ(connection)
        encoder = EncoderLineal(connection)
        polea = PoleaConica(connection)
        usuario = Usuario(connection)
        
        print("📡 Recolectando 10 datos en 1 minuto...")
        
        start_time = time.time()
        timeout = 60
        max_readings = 10
        reading_count = 0
        interval = timeout / max_readings  # 6 segundos entre lecturas
        
        try:
            while time.time() - start_time < timeout and reading_count < max_readings:
                data = self.usb.read_data()
                if data:
                    reading_count += 1
                    print(f"📊 Lectura {reading_count}/{max_readings}: {data}")
                    
                    # Guardar según tipo
                    if tipo == "1":
                        machine_id = yoyo.save(data)
                        usuario.save(nombre, apellido, yoyosq_id=machine_id)
                    elif tipo == "2":
                        machine_id = encoder.save(data)
                        usuario.save(nombre, apellido, encoder_id=machine_id)
                    elif tipo == "3":
                        machine_id = polea.save(data)
                        usuario.save(nombre, apellido, polea_id=machine_id)
                    
                    print("✅ Guardado en BD")
                    
                    # Esperar antes de la siguiente lectura
                    if reading_count < max_readings:
                        time.sleep(interval)
            
            print(f"\n⏱️ Completado: {reading_count} lecturas en {int(time.time() - start_time)} segundos")
        
        except KeyboardInterrupt:
            print("\n🛑 Detenido")
        finally:
            self.usb.close()
            self.db.close()

if __name__ == "__main__":
    collector = BioDashCollector()
    collector.run()