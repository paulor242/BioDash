from usb_collector import USBDataCollector
from data_manager import DataManager
import time

def main():
    # Inicializar componentes
    collector = USBDataCollector()
    data_manager = DataManager()
    
    # Mostrar puertos disponibles
    print("Puertos USB disponibles:")
    ports = collector.list_available_ports()
    for i, (port, desc) in enumerate(ports):
        print(f"{i+1}. {port} - {desc}")
    
    if not ports:
        print("No se encontraron puertos USB")
        return
    
    # Seleccionar puerto
    try:
        selection = int(input("Selecciona un puerto (número): ")) - 1
        selected_port = ports[selection][0]
    except (ValueError, IndexError):
        print("Selección inválida")
        return
    
    # Conectar al puerto
    print(f"Conectando a {selected_port}...")
    if not collector.connect(selected_port):
        print("No se pudo establecer la conexión")
        return
    
    print("Conexión establecida. Recopilando datos... (Ctrl+C para detener)")
    
    collected_data = []
    
    try:
        while True:
            data = collector.read_data()
            if data and data['data']:
                print(f"Datos recibidos: {data['data']}")
                collected_data.append(data)
            
            time.sleep(0.1)  # Pausa breve
            
    except KeyboardInterrupt:
        print("\nDeteniendo recopilación...")
    
    finally:
        collector.disconnect()
        
        # Guardar datos recopilados
        if collected_data:
            json_file = data_manager.save_to_json(collected_data)
            csv_file = data_manager.save_to_csv(collected_data)
            
            print(f"Datos guardados:")
            if json_file:
                print(f"- JSON: {json_file}")
            if csv_file:
                print(f"- CSV: {csv_file}")
        else:
            print("No se recopilaron datos")

if __name__ == "__main__":
    main()