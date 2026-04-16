import argparse
import json
import random
import time

import mysql.connector
import serial
import serial.tools.list_ports


SAMPLE_WINDOW_SECONDS = 6
MAX_READINGS_PER_MINUTE = 10

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


class BioDashCollector:
    def __init__(self):
        self.connection = None
        self.db_connection = None

    def connect_database(self):
        """Conectar a la base de datos BioDash"""
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                port=3306,
                password="paulo3144615",
                database="biodash",
            )
            print("Conectado a base de datos BioDash")
            return True
        except Exception as e:
            print(f"Error conectando a BD: {e}")
            return False

    def list_ports(self):
        """Listar puertos USB disponibles"""
        ports = serial.tools.list_ports.comports()
        return [(port.device, port.description) for port in ports]

    def connect_usb(self, port, baudrate=9600):
        """Conectar al puerto USB"""
        try:
            self.connection = serial.Serial(port, baudrate, timeout=1)
            print(f"Conectado a {port}")
            return True
        except Exception as e:
            print(f"Error USB: {e}")
            return False

    def read_data(self):
        """Leer una linea y convertirla a un diccionario utilizable."""
        if not self.connection or not self.connection.is_open:
            return None

        try:
            raw_data = self.connection.readline().decode("utf-8", errors="ignore").strip()
            if not raw_data:
                return None

            try:
                parsed = json.loads(raw_data)
                if isinstance(parsed, dict):
                    return parsed
                if isinstance(parsed, (int, float)):
                    numeric_value = float(parsed)
                    return {
                        "velocity_max": numeric_value,
                        "velocity_avg": numeric_value,
                    }
            except json.JSONDecodeError:
                pass

            if "," in raw_data:
                parts = [part.strip() for part in raw_data.split(",")]
                return self._parse_csv_parts(parts)

            try:
                numeric_value = float(raw_data)
                return {
                    "velocity_max": numeric_value,
                    "velocity_avg": numeric_value,
                }
            except ValueError:
                return {"raw_text": raw_data}
        except Exception:
            return None

    def read_sample_for_window(self, window_seconds):
        deadline = time.monotonic() + max(window_seconds, 0)
        while time.monotonic() < deadline:
            data = self.read_data()
            if data:
                return data
        return None

    def _parse_csv_parts(self, parts):
        parsed_parts = [float(part) if part else None for part in parts]

        if len(parsed_parts) >= len(ENCODER_KEYS):
            return {key: parsed_parts[index] for index, key in enumerate(ENCODER_KEYS)}

        if len(parsed_parts) >= len(YOYOSQ_KEYS):
            return {key: parsed_parts[index] for index, key in enumerate(YOYOSQ_KEYS)}

        if parsed_parts:
            return {
                "velocity_max": parsed_parts[0],
                "velocity_avg": parsed_parts[0],
            }

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
            data.get("acceleration_avg"), data.get("acceleration_max"),
            data.get("exentric_power_max"), data.get("exentric_power_avg"),
            data.get("concentric_power_max"), data.get("concentric_power_avg"),
            data.get("concentric_force_max"), data.get("concentric_force_avg"),
            data.get("velocity_avg"), data.get("velocity_max"),
            data.get("exentric_force_max"), data.get("exentric_force_avg"),
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
            data.get("force_max"), data.get("velocity_max_avg"), data.get("velocity_max"),
            data.get("acceleration_max"), data.get("power_max"), data.get("propulsive_power_avg"),
            data.get("power_avg"), data.get("impulse_max"), data.get("impulse_avg"),
            data.get("distance_max"), data.get("time_force_max"), data.get("time_impulse"),
            data.get("time_accel_max"), data.get("ideal_rm"), data.get("fatigue"),
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
            data.get("acceleration_avg"), data.get("acceleration_max"),
            data.get("exentric_power_max"), data.get("exentric_power_avg"),
            data.get("concentric_power_max"), data.get("concentric_power_avg"),
            data.get("concentric_force_max"), data.get("concentric_force_avg"),
            data.get("velocity_avg"), data.get("velocity_max"),
            data.get("exentric_force_max"), data.get("exentric_force_avg"),
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

    def generate_fake_data(self, tipo):
        if tipo == "2":
            values = [round(random.uniform(8, 15), 2) for _ in range(len(ENCODER_KEYS))]
            return {key: values[index] for index, key in enumerate(ENCODER_KEYS)}

        values = [round(random.uniform(8, 15), 2) for _ in range(len(YOYOSQ_KEYS))]
        return {key: values[index] for index, key in enumerate(YOYOSQ_KEYS)}

    def collect_and_store(self, nombre, apellido, tipo, use_fake_data=False):
        print("Recolectando solo 10 datos por minuto...")

        reading_count = 0
        collection_start = time.monotonic()

        while reading_count < MAX_READINGS_PER_MINUTE:
            if use_fake_data:
                data = self.generate_fake_data(tipo)
                time.sleep(SAMPLE_WINDOW_SECONDS)
            else:
                print(
                    f"Ventana {reading_count + 1}/{MAX_READINGS_PER_MINUTE}: "
                    f"esperando una muestra durante {SAMPLE_WINDOW_SECONDS} segundos..."
                )
                data = self.read_sample_for_window(SAMPLE_WINDOW_SECONDS)

            if not data:
                print("No llego una muestra valida en esta ventana. Reintentando...")
                continue

            reading_count += 1
            print(f"Lectura {reading_count}/{MAX_READINGS_PER_MINUTE}: {data}")

            if tipo == "1":
                machine_id = self.save_yoyosq(data)
                self.save_usuario(nombre, apellido, yoyosq_id=machine_id)
            elif tipo == "2":
                machine_id = self.save_encoder(data)
                self.save_usuario(nombre, apellido, encoder_id=machine_id)
            elif tipo == "3":
                machine_id = self.save_polea_conica(data)
                self.save_usuario(nombre, apellido, polea_id=machine_id)
            else:
                print("Tipo de maquina invalido")
                break

            print("Guardado en BD")

        elapsed_seconds = int(time.monotonic() - collection_start)
        print(
            f"\nCompletado: {reading_count} lecturas guardadas "
            f"en {elapsed_seconds} segundos"
        )

    def test_mode(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        tipo = input("Tipo de maquina (1=yoyosq, 2=encoder, 3=polea): ")
        self.collect_and_store(nombre, apellido, tipo, use_fake_data=True)

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--test", action="store_true", help="Modo test con datos simulados")
        args = parser.parse_args()

        if not self.connect_database():
            return

        if args.test:
            try:
                self.test_mode()
            finally:
                if self.db_connection:
                    self.db_connection.close()
            return

        ports = self.list_ports()
        if not ports:
            print("No hay puertos USB")
            return

        print("Puertos disponibles:")
        for i, (port, desc) in enumerate(ports):
            print(f"{i + 1}. {port} - {desc}")

        try:
            sel = int(input("Selecciona puerto: ")) - 1
            port = ports[sel][0]
        except Exception:
            print("Seleccion invalida")
            return

        if not self.connect_usb(port):
            return

        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        tipo = input("Tipo de maquina (1=yoyosq, 2=encoder, 3=polea): ")

        try:
            self.collect_and_store(nombre, apellido, tipo)
        except KeyboardInterrupt:
            print("\nDetenido")
        finally:
            if self.connection:
                self.connection.close()
            if self.db_connection:
                self.db_connection.close()


if __name__ == "__main__":
    collector = BioDashCollector()
    collector.run()
