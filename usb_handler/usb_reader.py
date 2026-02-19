import serial
import serial.tools.list_ports
import json

class USBHandler:
    def __init__(self):
        self.connection = None
    
    def list_ports(self):
        """Listar puertos USB disponibles"""
        ports = serial.tools.list_ports.comports()
        return [(port.device, port.description) for port in ports]
    
    def connect(self, port, baudrate=9600):
        """Conectar al puerto USB"""
        try:
            self.connection = serial.Serial(port, baudrate, timeout=1)
            print(f"✅ Conectado a {port}")
            return True
        except Exception as e:
            print(f"❌ Error USB: {e}")
            return False
    
    def read_data(self):
        """Leer datos del puerto USB"""
        if not self.connection or not self.connection.is_open:
            return None
        try:
            data = self.connection.readline().decode('utf-8').strip()
            if data:
                parsed = json.loads(data)
                # Si es un número simple, asumir que es velocidad
                if isinstance(parsed, (int, float)):
                    print(f"🔍 Datos recibidos (velocidad): {parsed}")
                    return {'velocity_max': parsed, 'velocity_avg': parsed}
                print(f"🔍 Datos recibidos: {parsed}")
                return parsed
        except json.JSONDecodeError:
            # Si no es JSON, intentar convertir a número (velocidad)
            try:
                num = float(data)
                print(f"🔍 Datos recibidos (velocidad): {num}")
                return {'velocity_max': num, 'velocity_avg': num}
            except:
                print(f"⚠️ Error leyendo: {data}")
                return None
        except json.JSONDecodeError as e:
            print(f"⚠️ Error JSON: {e} - Datos: {data}")
            return None
        except Exception as e:
            print(f"⚠️ Error leyendo: {e}")
            return None
    
    def close(self):
        """Cerrar conexión USB"""
        if self.connection:
            self.connection.close()