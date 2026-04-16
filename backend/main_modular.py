import time

from database.connection import DatabaseConnection
from models.encoder import EncoderLineal
from models.polea_conica import PoleaConica
from models.usuario import Usuario
from models.yoyosq import YoyoSQ
from usb_handler.usb_reader import USBHandler


SAMPLE_WINDOW_SECONDS = 6
MAX_READINGS_PER_MINUTE = 10


class BioDashCollector:
    def __init__(self):
        self.db = DatabaseConnection()
        self.usb = USBHandler()

    def run(self):
        """Ejecutar recolector"""
        if not self.db.connect():
            return

        connection = self.db.get_connection()

        ports = self.usb.list_ports()
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

        if not self.usb.connect(port):
            return

        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        tipo = input("Tipo de maquina (1=yoyosq, 2=encoder, 3=polea): ")

        yoyo = YoyoSQ(connection)
        encoder = EncoderLineal(connection)
        polea = PoleaConica(connection)
        usuario = Usuario(connection)

        print("Recolectando solo 10 datos por minuto...")

        reading_count = 0
        collection_start = time.monotonic()

        try:
            while reading_count < MAX_READINGS_PER_MINUTE:
                window_number = reading_count + 1
                print(
                    f"Ventana {window_number}/{MAX_READINGS_PER_MINUTE}: "
                    f"esperando una muestra durante {SAMPLE_WINDOW_SECONDS} segundos..."
                )

                data = self.usb.read_sample_for_window(SAMPLE_WINDOW_SECONDS)
                if not data:
                    print("No llego una muestra valida en esta ventana. Reintentando...")
                    continue

                reading_count += 1
                print(f"Lectura {reading_count}/{MAX_READINGS_PER_MINUTE}: {data}")

                if tipo == "1":
                    machine_id = yoyo.save(data)
                    usuario.save(nombre, apellido, yoyosq_id=machine_id)
                elif tipo == "2":
                    machine_id = encoder.save(data)
                    usuario.save(nombre, apellido, encoder_id=machine_id)
                elif tipo == "3":
                    machine_id = polea.save(data)
                    usuario.save(nombre, apellido, polea_id=machine_id)
                else:
                    print("Tipo de maquina invalido")
                    break

                print("Guardado en BD")

            elapsed_seconds = int(time.monotonic() - collection_start)
            print(
                f"\nCompletado: {reading_count} lecturas guardadas "
                f"en {elapsed_seconds} segundos"
            )

        except KeyboardInterrupt:
            print("\nDetenido")
        finally:
            self.usb.close()
            self.db.close()


if __name__ == "__main__":
    collector = BioDashCollector()
    collector.run()
