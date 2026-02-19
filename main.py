
import serial
import serial.tools.list_ports
import mysql.connector
import json
import time


class BioDashCollector:
    def __init__(self):
        self.connection = None
        self.db_connection = None
        
    def connect_database(self):
        """Conectar a la base de datos BioDash"""
        try:
            self.db_connection = mysql.connector.connect(
                host='localhost',
                user='root',
                port=3306,
                password='paulo3144615',  
                database='biodash'
            )
            print(" Conectado a base de datos BioDash")
            return True
        except Exception as e:
            print(f" Error conectando a BD: {e}")
            return False
    
    def list_ports(self):
        """Listar puertos USB disponibles"""
        ports = serial.tools.list_ports.comports()
        return [(port.device, port.description) for port in ports]
    
    def connect_usb(self, port, baudrate=9600):
        """Conectar al puerto USB"""
        try:
            self.connection = serial.Serial(port, baudrate, timeout=1)
            print(f" Conectado a {port}")
            return True
        except Exception as e:
            print(f" Error USB: {e}")
            return False
    
    def read_data(self):
        """Leer datos del puerto USB"""
        if not self.connection or not self.connection.is_open:
            return None
        try:
            data = self.connection.readline().decode('utf-8').strip()
            if data:
                # Intentar parsear como JSON primero
                try:
                    parsed = json.loads(data)
                    if isinstance(parsed, dict):
                        return parsed
                except:
                    pass
                
                # Si contiene comas, separar valores
                if ',' in data:
                    values = [float(v.strip()) for v in data.split(',')]
                    if len(values) >= 6:
                        return {
                            'velocity_max': values[0],
                            'velocity_avg': values[0],
                            'acceleration_max': values[1],
                            'acceleration_avg': values[1],
                            'concentric_force_max': values[2],
                            'concentric_force_avg': values[2],
                            'exentric_force_max': values[3],
                            'exentric_force_avg': values[3],
                            'concentric_power_max': values[4],
                            'concentric_power_avg': values[4],
                            'exentric_power_max': values[5],
                            'exentric_power_avg': values[5]
                        }
                return None
        except:
            return None
    
    def save_yoyosq(self, data):
        """Guardar datos en tabla yoyosq"""
        cursor = self.db_connection.cursor()
        query = """INSERT INTO yoyosq (
            Acceleration_avg, Acceleration_max, Exentric_power_Max, Exentric_power_Avg,
            Concentric_porwer_max, Consentric_power_Avg, Concentric_Force_max, 
            Concentric_force_Avg, Velocity_Avg, Velocity_max, Exentric_Force_Max, 
            Exentric_Force_Avg
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        values = (
            data.get('acceleration_avg'), data.get('acceleration_max'),
            data.get('exentric_power_max'), data.get('exentric_power_avg'),
            data.get('concentric_power_max'), data.get('concentric_power_avg'),
            data.get('concentric_force_max'), data.get('concentric_force_avg'),
            data.get('velocity_avg'), data.get('velocity_max'),
            data.get('exentric_force_max'), data.get('exentric_force_avg')
        )
        cursor.execute(query, values)
        self.db_connection.commit()
        return cursor.lastrowid
    
    def save_encoder(self, data):
        """Guardar datos en tabla encoder_lineal"""
        cursor = self.db_connection.cursor()
        query = """INSERT INTO encoder_lineal (
            Force_Max, Velocity_Max_Avg, Velocity_Max, Acceleration_Max, Power_Max,
            Propulsive_Power_avg, Power_Avg, Impulse_Max, Impulse_Avg, Distance_Max,
            Time_Force_Max, Time_impulse, Time_Accel_Max, Ideal_RM, Fatigue
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        values = (
            data.get('force_max'), data.get('velocity_max_avg'), data.get('velocity_max'),
            data.get('acceleration_max'), data.get('power_max'), data.get('propulsive_power_avg'),
            data.get('power_avg'), data.get('impulse_max'), data.get('impulse_avg'),
            data.get('distance_max'), data.get('time_force_max'), data.get('time_impulse'),
            data.get('time_accel_max'), data.get('ideal_rm'), data.get('fatigue')
        )
        cursor.execute(query, values)
        self.db_connection.commit()
        return cursor.lastrowid
    
    def save_polea_conica(self, data):
        """Guardar datos en tabla polea_conica"""
        cursor = self.db_connection.cursor()
        query = """INSERT INTO polea_conica (
            Acceleration_Avg, Acceleration_Max, Exentric_power_Max, Exentric_power_Avg,
            Concentric_porwer_max, Consentric_power_Avg, Concentric_Force_max,
            Concentric_force_Avg, Velocity_Avg, Velocity_max, Exentric_Force_Max,
            Exentric_Force_Avg
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        values = (
            data.get('acceleration_avg'), data.get('acceleration_max'),
            data.get('exentric_power_max'), data.get('exentric_power_avg'),
            data.get('concentric_power_max'), data.get('concentric_power_avg'),
            data.get('concentric_force_max'), data.get('concentric_force_avg'),
            data.get('velocity_avg'), data.get('velocity_max'),
            data.get('exentric_force_max'), data.get('exentric_force_avg')
        )
        cursor.execute(query, values)
        self.db_connection.commit()
        return cursor.lastrowid
    
    def save_usuario(self, nombre, apellido, yoyosq_id=None, encoder_id=None, polea_id=None):
        """Guardar usuario"""
        cursor = self.db_connection.cursor()
        query = """INSERT INTO usuario (nombre, apellido, FK_id_yoyosq, FK_id_encoder, FK_id_polea_conica) 
                   VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(query, (nombre, apellido, yoyosq_id, encoder_id, polea_id))
        self.db_connection.commit()
        return cursor.lastrowid
    
    def run(self):
        """Ejecutar recolector"""
        # Conectar BD
        if not self.connect_database():
            return
        
        # Mostrar puertos
        ports = self.list_ports()
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
        if not self.connect_usb(port):
            return
        
        # Datos usuario
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        tipo = input("Tipo de máquina (1=yoyosq, 2=encoder, 3=polea): ")
        
        print("📡 Recolectando 10 datos en 1 minuto...")
        
        start_time = time.time()
        timeout = 60
        max_readings = 10
        reading_count = 0
        interval = timeout / max_readings  # 6 segundos entre lecturas
        
        try:
            while time.time() - start_time < timeout and reading_count < max_readings:
                data = self.read_data()
                if data:
                    reading_count += 1
                    print(f"📊 Lectura {reading_count}/{max_readings}: {data}")
                    
                    # Guardar según tipo
                    if tipo == "1":
                        machine_id = self.save_yoyosq(data)
                        self.save_usuario(nombre, apellido, yoyosq_id=machine_id)
                    elif tipo == "2":
                        machine_id = self.save_encoder(data)
                        self.save_usuario(nombre, apellido, encoder_id=machine_id)
                    elif tipo == "3":
                        machine_id = self.save_polea_conica(data)
                        self.save_usuario(nombre, apellido, polea_id=machine_id)
                    
                    print("✅ Guardado en BD")
                    
                    # Esperar antes de la siguiente lectura
                    if reading_count < max_readings:
                        time.sleep(interval)
            
            print(f"\n⏱️ Completado: {reading_count} lecturas en {int(time.time() - start_time)} segundos")
        
        except KeyboardInterrupt:
            print("\n🛑 Detenido")
        finally:
            if self.connection:
                self.connection.close()
            if self.db_connection:
                self.db_connection.close()

if __name__ == "__main__":
    collector = BioDashCollector()
    collector.run()