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
            print(f"📡 RAW DATA recibida: '{data}'")  # SIEMPRE log raw
            if not data:
                return None
                
            # Intentar JSON
            try:
                parsed = json.loads(data)
                if isinstance(parsed, dict):
                    print(f"✅ JSON válido: {parsed}")
                    return parsed
                elif isinstance(parsed, (int, float)):
                    print(f"✅ Número simple: {parsed}")
                    return {'velocity_max': float(parsed), 'velocity_avg': float(parsed)}
            except json.JSONDecodeError:
                pass
            
            # Intentar CSV comma-separated
            if ',' in data:
                try:
                    parts = [p.strip() for p in data.split(',')]
                    print(f"📡 CSV parseado: {len(parts)} campos: {parts}")
                    generic_data = {
                        'raw_parts': parts,
                        'field_count': len(parts)
                    }
                    # Mapear a campos comunes basados en máquina
                    if len(parts) >= 12:  # YoyoSQ/Polea full
                        generic_data.update({
                            'acceleration_avg': float(parts[0]) if parts[0] else None,
                            'acceleration_max': float(parts[1]) if len(parts)>1 and parts[1] else None,
                            'exentric_power_max': float(parts[2]) if len(parts)>2 and parts[2] else None,
                            # ... más mappings
                            'velocity_max': float(parts[9]) if len(parts)>9 and parts[9] else None,
                        })
                    elif len(parts) >=1:
                        generic_data['velocity_max'] = float(parts[0]) if parts[0] else None
                        generic_data['velocity_avg'] = generic_data['velocity_max']
                    print(f"✅ Datos genéricos: {generic_data}")
                    return generic_data
                except ValueError as ve:
                    print(f"⚠️ Error parse números CSV: {ve}")
            
            # Número simple
            try:
                num = float(data)
                print(f"✅ Número simple: {num}")
                return {'velocity_max': num, 'velocity_avg': num}
            except ValueError:
                pass
            
            # Raw text
            print(f"📄 Datos raw como texto")
            return {'raw_text': data}
            
        except Exception as e:
            print(f"❌ Error USB read: {e}")
            return None
    
    def close(self):
        """Cerrar conexión USB"""
        if self.connection:
            self.connection.close()