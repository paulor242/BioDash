import json
import csv
from datetime import datetime
import os

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Crea el directorio de datos si no existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_to_json(self, data, filename=None):
        """Guarda datos en formato JSON"""
        if not filename:
            filename = f"usb_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return filepath
        except Exception as e:
            print(f"Error guardando JSON: {e}")
            return None
    
    def save_to_csv(self, data_list, filename=None):
        """Guarda lista de datos en formato CSV"""
        if not data_list:
            return None
            
        if not filename:
            filename = f"usb_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data_list[0].keys())
                writer.writeheader()
                writer.writerows(data_list)
            return filepath
        except Exception as e:
            print(f"Error guardando CSV: {e}")
            return None
    
    def load_json(self, filename):
        """Carga datos desde archivo JSON"""
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando JSON: {e}")
            return None