import ctypes
import os
from typing import Dict, Any
import logging

class TSCPrinterService:
    def __init__(self):
        # Logger'ı UTF-8 encoding ile yapılandır
        self.logger = logging.getLogger(__name__)
        
        # Eğer handler yoksa ekle
        if not self.logger.handlers:
            import sys
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # TSCLIB.dll fonksiyonlarını yükle
        try:
            self.tsc_lib = ctypes.CDLL("TSCLIB.dll")
            self._setup_function_signatures()
        except Exception as e:
            self.logger.error(f"TSCLIB.dll yüklenemedi: {e}")
            self.tsc_lib = None
    
    def _setup_function_signatures(self):
        """TSCLIB.dll fonksiyon imzalarını ayarla"""
        if self.tsc_lib:
            # openport
            self.tsc_lib.openport.argtypes = [ctypes.c_char_p]
            self.tsc_lib.openport.restype = None
            
            # sendcommand
            self.tsc_lib.sendcommand.argtypes = [ctypes.c_char_p]
            self.tsc_lib.sendcommand.restype = None
            
            # clearbuffer
            self.tsc_lib.clearbuffer.argtypes = []
            self.tsc_lib.clearbuffer.restype = None
            
            # closeport
            self.tsc_lib.closeport.argtypes = []
            self.tsc_lib.closeport.restype = None
            
            # downloadbmp
            self.tsc_lib.downloadbmp.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
            self.tsc_lib.downloadbmp.restype = None
    
    def print_label(self, file_path: str, settings: Dict[str, Any], is_bluetooth_label: bool = False):
        """Etiket yazdırma işlemi"""
        if not self.tsc_lib:
            self.logger.error("TSCLIB.dll yüklenemedi, yazdırma işlemi yapılamıyor")
            return False
        
        try:
            # Printer adını belirle
            printer_name = (settings['bluetooth_printer_name'] if is_bluetooth_label 
                          else settings['carton_printer_name'])
            
            # Printer'a bağlan
            self._open_port(printer_name)
            
            # Buffer'ı temizle
            self._clear_buffer()
            
            # Printer'ı konfigüre et
            self._configure_printer(settings, is_bluetooth_label)
            
            # Bitmap'i yükle ve yazdır
            self._download_bmp(file_path, "label.bmp")
            self._send_command('PUTBMP 0,0,"label.bmp",8,80')
            self._send_command('PRINT 1,1')
            
            # Bağlantıyı kapat
            self._close_port()
            
            self.logger.info(f"Etiket başarıyla yazdırıldı: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Yazdırma işlemi sırasında hata: {e}")
            return False
    
    def _open_port(self, printer_name: str):
        """Printer portunu aç"""
        if self.tsc_lib:
            self.tsc_lib.openport(printer_name.encode('utf-8'))
    
    def _send_command(self, command: str):
        """Printer'a komut gönder"""
        if self.tsc_lib:
            self.tsc_lib.sendcommand(command.encode('utf-8'))
    
    def _clear_buffer(self):
        """Printer buffer'ını temizle"""
        if self.tsc_lib:
            self.tsc_lib.clearbuffer()
    
    def _close_port(self):
        """Printer portunu kapat"""
        if self.tsc_lib:
            self.tsc_lib.closeport()
    
    def _download_bmp(self, file_path: str, image_name: str):
        """Bitmap dosyasını printer'a yükle"""
        if self.tsc_lib:
            self.tsc_lib.downloadbmp(file_path.encode('utf-8'), image_name.encode('utf-8'))
    
    def _configure_printer(self, settings: Dict[str, Any], is_bluetooth_label: bool):
        """Printer ayarlarını yapılandır"""
        # Label boyutlarını belirle
        label_width = (settings['bluetooth_label_width'] if is_bluetooth_label 
                      else settings['carton_label_width'])
        label_height = (settings['bluetooth_label_height'] if is_bluetooth_label 
                       else settings['carton_label_height'])
        
        # Printer komutlarını gönder
        direction = 0 if settings['orientation'].lower() == 'landscape' else 1
        self._send_command(f'DIRECTION {direction}')
        self._send_command(f'DENSITY {settings["density"]}')
        self._send_command(f'SPEED {settings["speed"]}')
        self._send_command(f'SIZE {label_width} mm, {label_width} mm')
        self._send_command(f'GAP {settings["gap_height"]} mm, {settings["gap_offset"]} mm')
        self._send_command('TEAR ON' if settings['tear_off'] else 'TEAR OFF')
        self._send_command('AUTO CALIBRATION')
        self._send_command(f'SHIFT -{settings["left_shift"]} mm')
    
    def is_development_mode(self, settings: Dict[str, Any]) -> bool:
        """Geliştirme modunda olup olmadığını kontrol et"""
        return settings.get('is_app_development_mode', False) 