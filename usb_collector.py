import serial
import serial.tools.list_ports
import json
from datetime import datetime

class USBDataCollector:
    def __init__(self, port=None, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        
    def list_available_ports(self):
        """Lista todos los puertos USB disponibles"""
        ports = serial.tools.list_ports.comports()
        return [(port.device, port.description) for port in ports]
    
    def connect(self, port=None):
        """Establece conexión con el puerto USB"""
        if port:
            self.port = port
        
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
            return True
        except Exception as e:
            print(f"Error conectando: {e}")
            return False
    
    def read_data(self):
        """Lee datos del puerto USB"""
        if not self.connection or not self.connection.is_open:
            return None
            
        try:
            data = self.connection.readline().decode('utf-8').strip()
            return {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
        except Exception as e:
            print(f"Error leyendo datos: {e}")
            return None
    
    def disconnect(self):
        """Cierra la conexión USB"""
        if self.connection and self.connection.is_open:
            self.connection.close()