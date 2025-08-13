from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
import tempfile
import base64
import sqlite3
from datetime import datetime

from config import Config
from tsc_printer_service import TSCPrinterService
from label_bitmap_generator import LabelBitmapGenerator
from dto import UserInputModel, UserInputModelSchema

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

# Konfigürasyon
app.config.from_object(Config)

# Servisler
tsc_printer_service = TSCPrinterService()
label_generator = LabelBitmapGenerator()

# Schema
user_input_schema = UserInputModelSchema()

def get_db_connection():
    """SQLite veritabanı bağlantısı oluştur"""
    return sqlite3.connect('labelPrint.db')

# React uygulamasını serve et
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/debug/database', methods=['GET'])
def debug_database():
    """Veritabanı bağlantısını test et"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # InputInfo tablosunu kontrol et
        cursor.execute("SELECT COUNT(*) FROM InputInfo")
        input_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM InputInfo LIMIT 5")
        input_items = cursor.fetchall()
        
        # IconInfo tablosunu kontrol et
        cursor.execute("SELECT COUNT(*) FROM IconInfo")
        icon_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM IconInfo LIMIT 5")
        icon_items = cursor.fetchall()
        
        # BarcodeInfo tablosunu kontrol et
        cursor.execute("SELECT COUNT(*) FROM BarcodeInfo")
        barcode_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM BarcodeInfo LIMIT 5")
        barcode_items = cursor.fetchall()
        
        # LabelSetting tablosunu kontrol et
        cursor.execute("SELECT COUNT(*) FROM LabelSetting")
        setting_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM LabelSetting LIMIT 5")
        setting_items = cursor.fetchall()
        
        result = {
            'database_url': Config.DATABASE_URL,
            'input_info': {
                'count': input_count,
                'items': [
                    {
                        'id': item[0],
                        'text': item[1],
                        'font_size': item[2],
                        'font_family': item[3],
                        'x_coordinate': item[4],
                        'y_coordinate': item[5]
                    } for item in input_items
                ]
            },
            'icon_info': {
                'count': icon_count,
                'items': [
                    {
                        'id': item[0],
                        'base64_string': item[1],
                        'x_coordinate': item[2],
                        'y_coordinate': item[3],
                        'width': item[4],
                        'height': item[5]
                    } for item in icon_items
                ]
            },
            'barcode_info': {
                'count': barcode_count,
                'items': [
                    {
                        'id': item[0],
                        'x_coordinate': item[1],
                        'y_coordinate': item[2],
                        'width': item[3],
                        'height': item[4],
                        'barcode_sequence': item[5],
                        'barcode_format': item[6],
                        'text_alignment': item[7],
                        'text_font_size': item[8],
                        'text_font_family': item[9]
                    } for item in barcode_items
                ]
            },
            'label_setting': {
                'count': setting_count,
                'items': [
                    {
                        'id': item[0],
                        'width': item[1],
                        'height': item[2],
                        'dpi': item[3]
                    } for item in setting_items
                ]
            }
        }
        
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Database debug error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/input-items', methods=['GET'])
def get_input_items():
    """Veritabanından input item'ları getir"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT Id, Text, FontSize, FontFamily, XCoordinate, YCoordinate FROM InputInfo")
        items = cursor.fetchall()
        
        result = []
        for item in items:
            result.append({
                'id': item[0],
                'text': item[1],
                'x': item[4],
                'y': item[5],
                'fontSize': item[2],
                'fontFamily': item[3]
            })
        
        logging.info(f"Retrieved {len(result)} input items from database")
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Get input items error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/icon-items', methods=['GET'])
def get_icon_items():
    """Veritabanından icon item'ları getir"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT Id, Base64String, XCoordinate, YCoordinate, Width, Height FROM IconInfo")
        items = cursor.fetchall()
        
        result = []
        for item in items:
            result.append({
                'id': item[0],
                'x': item[2],
                'y': item[3],
                'width': item[4],
                'height': item[5],
                'base64String': item[1]
            })
        
        logging.info(f"Retrieved {len(result)} icon items from database")
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Get icon items error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/barcode-items', methods=['GET'])
def get_barcode_items():
    """Veritabanından barcode item'ları getir"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT Id, XCoordinate, YCoordinate, Width, Height, BarcodeSequence, BarcodeFormat, TextAlignment, TextFontSize, TextFontFamily FROM BarcodeInfo")
        items = cursor.fetchall()
        
        result = []
        for item in items:
            result.append({
                'id': item[0],
                'x': item[1],
                'y': item[2],
                'width': item[3],
                'height': item[4],
                'barcodeData': f"Barcode_{item[0]}",  # Örnek data
                'barcodeSequence': item[5],
                'barcodeFormat': item[6],
                'textAlignment': item[7],
                'textFontSize': item[8],
                'textFontFamily': item[9]
            })
        
        logging.info(f"Retrieved {len(result)} barcode items from database")
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Get barcode items error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/label-settings', methods=['GET'])
def get_label_settings():
    """Veritabanından label ayarlarını getir"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT Id, Width, Height, DPI FROM LabelSetting LIMIT 1")
        settings = cursor.fetchone()
        
        if settings:
            result = {
                'id': settings[0],
                'width': float(settings[1]),
                'height': float(settings[2]),
                'dpi': int(settings[3])
            }
        else:
            result = {
                'width': 100,
                'height': 100,
                'dpi': 300
            }
        
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Get label settings error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/create-bitmap', methods=['POST'])
def create_bitmap():
    """Bitmap oluştur ve base64 olarak döndür"""
    try:
        data = request.get_json()
        if not data or 'textEntries' not in data:
            return jsonify({'error': 'Invalid input data'}), 400
        
        text_entries = data['textEntries']
        icon_entries = data.get('iconEntries', [])
        barcode_entries = data.get('barcodeEntries', [])
        
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Text entries'i dönüştür
            texts = []
            for entry in text_entries:
                texts.append({
                    'content': entry['text'],
                    'font_family': entry['fontFamily'],
                    'font_size': entry['fontSize'],
                    'x_coordinate': entry['x'],
                    'y_coordinate': entry['y']
                })
            
            # Icon entries'i dönüştür
            icons = []
            for entry in icon_entries:
                icons.append({
                    'base64_string': entry.get('base64String', ''),
                    'x_coordinate': entry['x'],
                    'y_coordinate': entry['y'],
                    'width': entry['width'],
                    'height': entry['height']
                })
            
            # Barcode entries'i dönüştür
            barcodes = []
            for entry in barcode_entries:
                barcodes.append({
                    'data': entry.get('barcodeData', ''),
                    'x_coordinate': entry['x'],
                    'y_coordinate': entry['y'],
                    'width': entry['width'],
                    'height': entry['height'],
                    'format': entry.get('barcodeFormat', 'CODE_39'),
                    'text_alignment': entry.get('textAlignment', 'none'),
                    'text_font_size': entry.get('textFontSize', 8),
                    'text_font_family': entry.get('textFontFamily', 'Arial')
                })
            
            # Bitmap oluştur
            success = label_generator.generate_label(
                temp_path, texts, icons, barcodes, 
                is_bluetooth_label=False, 
                settings=Config.PRINTER_SETTINGS
            )
            
            if not success:
                return jsonify({'error': 'Bitmap creation failed'}), 500
            
            # Bitmap'i base64'e çevir
            with open(temp_path, 'rb') as f:
                bitmap_data = f.read()
                base64_bitmap = base64.b64encode(bitmap_data).decode('utf-8')
            
            return jsonify({
                'bitmap': base64_bitmap,
                'message': 'Bitmap created successfully'
            }), 200
            
        finally:
            # Geçici dosyayı temizle
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logging.error(f"Create bitmap error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/save-settings', methods=['POST'])
def save_settings():
    """Bitmap ayarlarını veritabanına kaydet"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid settings data'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Input items'ları kaydet
            if 'textEntries' in data:
                for entry in data['textEntries']:
                    if 'id' in entry and entry['id']:
                        # Update existing
                        cursor.execute("""
                            UPDATE InputInfo 
                            SET Text = ?, FontSize = ?, FontFamily = ?, XCoordinate = ?, YCoordinate = ?
                            WHERE Id = ?
                        """, (entry['text'], entry['fontSize'], entry['fontFamily'], entry['x'], entry['y'], entry['id']))
                    else:
                        # Create new
                        import uuid
                        new_id = str(uuid.uuid4())
                        cursor.execute("""
                            INSERT INTO InputInfo (Id, Text, FontSize, FontFamily, XCoordinate, YCoordinate)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (new_id, entry['text'], entry['fontSize'], entry['fontFamily'], entry['x'], entry['y']))
            
            # Icon items'ları kaydet
            if 'iconEntries' in data:
                for entry in data['iconEntries']:
                    if 'id' in entry and entry['id']:
                        # Update existing
                        cursor.execute("""
                            UPDATE IconInfo 
                            SET Base64String = ?, XCoordinate = ?, YCoordinate = ?, Width = ?, Height = ?
                            WHERE Id = ?
                        """, (entry.get('base64String', ''), entry['x'], entry['y'], entry['width'], entry['height'], entry['id']))
                    else:
                        # Create new
                        import uuid
                        new_id = str(uuid.uuid4())
                        cursor.execute("""
                            INSERT INTO IconInfo (Id, Base64String, XCoordinate, YCoordinate, Width, Height)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (new_id, entry.get('base64String', ''), entry['x'], entry['y'], entry['width'], entry['height']))
            
            # Barcode items'ları kaydet
            if 'barcodeEntries' in data:
                for entry in data['barcodeEntries']:
                    if 'id' in entry and entry['id']:
                        # Update existing
                        cursor.execute("""
                            UPDATE BarcodeInfo 
                            SET XCoordinate = ?, YCoordinate = ?, Width = ?, Height = ?, 
                                BarcodeSequence = ?, BarcodeFormat = ?, TextAlignment = ?, 
                                TextFontSize = ?, TextFontFamily = ?
                            WHERE Id = ?
                        """, (entry['x'], entry['y'], entry['width'], entry['height'], 
                              entry.get('barcodeSequence', 1), entry.get('barcodeFormat', 'CODE_39'),
                              entry.get('textAlignment', 'none'), entry.get('textFontSize', 8),
                              entry.get('textFontFamily', 'Arial'), entry['id']))
                    else:
                        # Create new
                        import uuid
                        new_id = str(uuid.uuid4())
                        cursor.execute("""
                            INSERT INTO BarcodeInfo (Id, XCoordinate, YCoordinate, Width, Height, 
                                                   BarcodeSequence, BarcodeFormat, TextAlignment, 
                                                   TextFontSize, TextFontFamily)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (new_id, entry['x'], entry['y'], entry['width'], entry['height'],
                              entry.get('barcodeSequence', 1), entry.get('barcodeFormat', 'CODE_39'),
                              entry.get('textAlignment', 'none'), entry.get('textFontSize', 8),
                              entry.get('textFontFamily', 'Arial')))
            
            conn.commit()
            
            return jsonify({
                'message': 'Settings saved successfully',
                'saved_entries': len(data.get('textEntries', [])) + len(data.get('iconEntries', [])) + len(data.get('barcodeEntries', []))
            }), 200
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        
    except Exception as e:
        logging.error(f"Save settings error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/print', methods=['POST'])
def print_label():
    """Etiket yazdırma endpoint'i"""
    try:
        # Request verilerini doğrula
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input data'}), 400
        
        # UserInputModel oluştur
        user_input = UserInputModel(
            input_value_pairs=data.get('textEntries', []),
            barcode_data_list=data.get('barcodeEntries', []),
            icon_info_list=data.get('iconEntries', [])
        )
        
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Bluetooth etiketi oluştur ve yazdır
            success = generate_and_print_bluetooth_label(user_input, temp_path)
            if not success:
                return jsonify({'error': 'Bluetooth label generation failed'}), 500
            
            # Karton etiketi oluştur ve yazdır
            success = generate_and_print_carton_label(user_input, temp_path)
            if not success:
                return jsonify({'error': 'Carton label generation failed'}), 500
            
            return jsonify({'message': 'Labels printed successfully'}), 200
            
        finally:
            # Geçici dosyayı temizle
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logging.error(f"Print request error: {e}")
        return jsonify({'error': str(e)}), 500

def generate_and_print_bluetooth_label(user_input: UserInputModel, temp_path: str):
    """Bluetooth etiketi oluştur ve yazdır"""
    try:
        # Metin elemanlarını hazırla
        texts = []
        if user_input.input_value_pairs:
            for pair in user_input.input_value_pairs:
                texts.append({
                    'content': pair.get('text', ''),
                    'font_family': pair.get('fontFamily', 'Arial'),
                    'font_size': pair.get('fontSize', 8),
                    'x_coordinate': pair.get('x', 0),
                    'y_coordinate': pair.get('y', 0)
                })
        
        # Barkod elemanlarını hazırla
        barcodes = []
        if user_input.barcode_data_list:
            for barcode_data in user_input.barcode_data_list:
                barcodes.append({
                    'data': barcode_data.get('barcodeData', ''),
                    'x_coordinate': barcode_data.get('x', 10),
                    'y_coordinate': barcode_data.get('y', 10),
                    'width': barcode_data.get('width', 50),
                    'height': barcode_data.get('height', 20),
                    'format': barcode_data.get('barcodeFormat', 'CODE_39'),
                    'text_alignment': barcode_data.get('textAlignment', 'none'),
                    'text_font_size': barcode_data.get('textFontSize', 8),
                    'text_font_family': barcode_data.get('textFontFamily', 'Arial')
                })
        
        # İkon elemanlarını hazırla
        icons = []
        if user_input.icon_info_list:
            for icon_info in user_input.icon_info_list:
                icons.append({
                    'base64_string': icon_info.get('base64String', ''),
                    'x_coordinate': icon_info.get('x', 0),
                    'y_coordinate': icon_info.get('y', 0),
                    'width': icon_info.get('width', 50),
                    'height': icon_info.get('height', 50)
                })
        
        # Bitmap oluştur
        success = label_generator.generate_label(
            temp_path, texts, icons, barcodes, 
            is_bluetooth_label=True, 
            settings=Config.PRINTER_SETTINGS
        )
        
        if not success:
            return False
        
        # Yazdır (geliştirme modunda değilse)
        if not Config.PRINTER_SETTINGS['is_app_development_mode']:
            success = tsc_printer_service.print_label(
                temp_path, Config.PRINTER_SETTINGS, is_bluetooth_label=True
            )
            return success
        
        return True
        
    except Exception as e:
        logging.error(f"Bluetooth label generation error: {e}")
        return False

def generate_and_print_carton_label(user_input: UserInputModel, temp_path: str):
    """Karton etiketi oluştur ve yazdır"""
    try:
        # Metin elemanlarını hazırla
        texts = []
        if user_input.input_value_pairs:
            for pair in user_input.input_value_pairs:
                texts.append({
                    'content': pair.get('text', ''),
                    'font_family': pair.get('fontFamily', 'Arial'),
                    'font_size': pair.get('fontSize', 8),
                    'x_coordinate': pair.get('x', 0),
                    'y_coordinate': pair.get('y', 0)
                })
        
        # Barkod elemanlarını hazırla
        barcodes = []
        if user_input.barcode_data_list:
            for barcode_data in user_input.barcode_data_list:
                barcodes.append({
                    'data': barcode_data.get('barcodeData', ''),
                    'x_coordinate': barcode_data.get('x', 10),
                    'y_coordinate': barcode_data.get('y', 10),
                    'width': barcode_data.get('width', 50),
                    'height': barcode_data.get('height', 20),
                    'format': barcode_data.get('barcodeFormat', 'CODE_39'),
                    'text_alignment': barcode_data.get('textAlignment', 'none'),
                    'text_font_size': barcode_data.get('textFontSize', 8),
                    'text_font_family': barcode_data.get('textFontFamily', 'Arial')
                })
        
        # İkon elemanlarını hazırla
        icons = []
        if user_input.icon_info_list:
            for icon_info in user_input.icon_info_list:
                icons.append({
                    'base64_string': icon_info.get('base64String', ''),
                    'x_coordinate': icon_info.get('x', 0),
                    'y_coordinate': icon_info.get('y', 0),
                    'width': icon_info.get('width', 50),
                    'height': icon_info.get('height', 50)
                })
        
        # Bitmap oluştur
        success = label_generator.generate_label(
            temp_path, texts, icons, barcodes, 
            is_bluetooth_label=False, 
            settings=Config.PRINTER_SETTINGS
        )
        
        if not success:
            return False
        
        # Yazdır (geliştirme modunda değilse)
        if not Config.PRINTER_SETTINGS['is_app_development_mode']:
            success = tsc_printer_service.print_label(
                temp_path, Config.PRINTER_SETTINGS, is_bluetooth_label=False
            )
            return success
        
        return True
        
    except Exception as e:
        logging.error(f"Carton label generation error: {e}")
        return False

@app.route('/api/label/settings', methods=['GET'])
def get_printer_settings():
    """Printer ayarlarını getir"""
    try:
        return jsonify(Config.PRINTER_SETTINGS), 200
    except Exception as e:
        logging.error(f"Get settings error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/label/settings', methods=['POST'])
def update_printer_settings():
    """Printer ayarlarını güncelle"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid settings data'}), 400
        
        # Ayarları güncelle (gerçek uygulamada veritabanına kaydedilir)
        for key, value in data.items():
            if key in Config.PRINTER_SETTINGS:
                Config.PRINTER_SETTINGS[key] = value
        
        return jsonify({'message': 'Settings updated successfully'}), 200
    except Exception as e:
        logging.error(f"Update settings error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Sağlık kontrolü"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    # Logs dizinini oluştur
    os.makedirs('logs', exist_ok=True)
    
    # Uygulamayı başlat
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    ) 