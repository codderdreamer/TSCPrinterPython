import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask ayarları
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Database ayarları - Aynı dizindeki labelPrint.db dosyasını kullan
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///labelPrint.db')
    
    # Printer ayarları
    PRINTER_SETTINGS = {
        'bluetooth_printer_name': os.getenv('BLUETOOTH_PRINTER_NAME', 'TSC TE310-btpincode'),
        'carton_printer_name': os.getenv('CARTON_PRINTER_NAME', 'TSC TE310-packaging'),
        'bluetooth_label_width': float(os.getenv('BLUETOOTH_LABEL_WIDTH', '100')),
        'bluetooth_label_height': float(os.getenv('BLUETOOTH_LABEL_HEIGHT', '29')),
        'carton_label_width': float(os.getenv('CARTON_LABEL_WIDTH', '100')),
        'carton_label_height': float(os.getenv('CARTON_LABEL_HEIGHT', '67')),
        'dpi': int(os.getenv('DPI', '300')),
        'orientation': os.getenv('ORIENTATION', 'portrait'),
        'density': int(os.getenv('DENSITY', '12')),
        'speed': int(os.getenv('SPEED', '4')),
        'gap_height': float(os.getenv('GAP_HEIGHT', '3.048')),
        'gap_offset': float(os.getenv('GAP_OFFSET', '0')),
        'tear_off': os.getenv('TEAR_OFF', 'True').lower() == 'true',
        'left_shift': float(os.getenv('LEFT_SHIFT', '2.032')),
        'right_shift': float(os.getenv('RIGHT_SHIFT', '2.032')),
        'is_app_development_mode': os.getenv('IS_APP_DEVELOPMENT_MODE', 'False').lower() == 'true'
    }
    
    # API ayarları
    API_SETTINGS = {
        'base_url': os.getenv('API_BASE_URL', 'https://10.254.240.20:50000/b1s/v1'),
        'company_db': os.getenv('COMPANY_DB', 'HERATEST03'),
        'username': os.getenv('API_USERNAME', 'manager'),
        'password': os.getenv('API_PASSWORD', '3944'),
        'select_serial_number_columns': os.getenv('SELECT_SERIAL_NUMBER_COLUMNS', 
            'DocEntry,ItemCode,ItemDescription,MfrSerialNo,SerialNumber,U_4GImei,U_BluetoothMAC,U_BLE_A_P,U_EthernetMAC,U_CPID,U_MRFID,U_KRFID,U_KRFID1'),
        'select_ean_columns': os.getenv('SELECT_EAN_COLUMNS', 
            'ItemCode,ItemName,ForeignName,BarCode,U_Model,U_System,U_RaletedVoltage,U_RaletedPower,U_BodyColor')
    }
    
    # Serial Port ayarları
    SERIAL_PORT_SETTINGS = {
        'port_name': os.getenv('SERIAL_PORT_NAME', 'COM6'),
        'baud_rate': int(os.getenv('SERIAL_BAUD_RATE', '9600')),
        'parity': os.getenv('SERIAL_PARITY', 'None'),
        'data_bits': int(os.getenv('SERIAL_DATA_BITS', '8')),
        'stop_bits': os.getenv('SERIAL_STOP_BITS', 'One'),
        'is_app_development_mode': os.getenv('SERIAL_IS_APP_DEVELOPMENT_MODE', 'False').lower() == 'true'
    } 