import json
import time

import serial
import serial.tools.list_ports


YOYOSQ_KEYS = [
    "acceleration_avg",
    "acceleration_max",
    "exentric_power_max",
    "exentric_power_avg",
    "concentric_power_max",
    "concentric_power_avg",
    "concentric_force_max",
    "concentric_force_avg",
    "velocity_avg",
    "velocity_max",
    "exentric_force_max",
    "exentric_force_avg",
]

ENCODER_KEYS = [
    "force_max",
    "velocity_max_avg",
    "velocity_max",
    "acceleration_max",
    "power_max",
    "propulsive_power_avg",
    "power_avg",
    "impulse_max",
    "impulse_avg",
    "distance_max",
    "time_force_max",
    "time_impulse",
    "time_accel_max",
    "ideal_rm",
    "fatigue",
]


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
            print(f"Conectado a {port}")
            return True
        except Exception as e:
            print(f"Error USB: {e}")
            return False

    def read_data(self):
        """Leer y parsear una linea del puerto USB."""
        if not self.connection or not self.connection.is_open:
            return None

        try:
            raw_data = self.connection.readline().decode("utf-8", errors="ignore").strip()
            print(f"RAW DATA recibida: '{raw_data}'")

            if not raw_data:
                return None

            try:
                parsed = json.loads(raw_data)
                if isinstance(parsed, dict):
                    print(f"JSON valido: {parsed}")
                    return parsed
                if isinstance(parsed, (int, float)):
                    numeric_value = float(parsed)
                    print(f"Numero simple: {numeric_value}")
                    return {
                        "velocity_max": numeric_value,
                        "velocity_avg": numeric_value,
                    }
            except json.JSONDecodeError:
                pass

            if "," in raw_data:
                parts = [part.strip() for part in raw_data.split(",")]
                print(f"CSV parseado: {len(parts)} campos: {parts}")
                parsed_csv = self._parse_csv_parts(parts)
                print(f"Datos parseados: {parsed_csv}")
                return parsed_csv

            try:
                numeric_value = float(raw_data)
                print(f"Numero simple: {numeric_value}")
                return {
                    "velocity_max": numeric_value,
                    "velocity_avg": numeric_value,
                }
            except ValueError:
                print("Dato recibido como texto plano")
                return {"raw_text": raw_data}

        except Exception as e:
            print(f"Error USB read: {e}")
            return None

    def read_sample_for_window(self, window_seconds):
        """Esperar una muestra valida dentro de una ventana fija."""
        deadline = time.monotonic() + max(window_seconds, 0)

        while time.monotonic() < deadline:
            data = self.read_data()
            if data:
                return data

        return None

    def _parse_csv_parts(self, parts):
        parsed_parts = [float(part) if part else None for part in parts]
        parsed_data = {
            "raw_parts": parts,
            "field_count": len(parts),
        }

        if len(parsed_parts) >= len(ENCODER_KEYS):
            parsed_data.update(
                {key: parsed_parts[index] for index, key in enumerate(ENCODER_KEYS)}
            )
            return parsed_data

        if len(parsed_parts) >= len(YOYOSQ_KEYS):
            parsed_data.update(
                {key: parsed_parts[index] for index, key in enumerate(YOYOSQ_KEYS)}
            )
            return parsed_data

        if parsed_parts:
            parsed_data["velocity_max"] = parsed_parts[0]
            parsed_data["velocity_avg"] = parsed_parts[0]

        return parsed_data

    def close(self):
        """Cerrar conexion USB"""
        if self.connection:
            self.connection.close()
