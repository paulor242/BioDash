import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from usb_handler.usb_reader import USBHandler

def test_usb_ports():
    """Probar listado de puertos USB"""
    print("🧪 Probando puertos USB...")
    
    usb = USBHandler()
    ports = usb.list_ports()
    
    if ports:
        print("✅ Puertos encontrados:")
        for i, (port, desc) in enumerate(ports):
            print(f"  {i+1}. {port} - {desc}")
        return True
    else:
        print("❌ No se encontraron puertos")
        return False

if __name__ == "__main__":
    test_usb_ports()