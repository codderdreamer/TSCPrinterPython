from PIL import Image, ImageDraw, ImageFont
import qrcode
from typing import List, Dict, Any, Tuple
import logging
import os

class LabelBitmapGenerator:
    def __init__(self):
        # Logger'ı UTF-8 encoding ile yapılandır
        self.logger = logging.getLogger(__name__)
        
        # Eğer handler yoksa ekle
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        self.mm_to_inches = 0.0393701
    
    def generate_label(self, file_path: str, texts: List[Dict], icons: List[Dict], 
                      barcodes: List[Dict], is_bluetooth_label: bool, settings: Dict[str, Any]):
        """Etiket bitmap'ini oluştur"""
        try:
            # Label boyutlarını belirle
            if is_bluetooth_label:
                label_width = settings['bluetooth_label_width']
                label_height = settings['bluetooth_label_height']
            else:
                label_width = settings['carton_label_width']
                label_height = settings['carton_label_height']
            
            dpi = settings['dpi']
            
            # Piksel boyutlarını hesapla
            width_in_pixels = int(label_width * self.mm_to_inches * dpi)
            height_in_pixels = int(label_height * self.mm_to_inches * dpi)
            
            # Bitmap oluştur
            bitmap = Image.new('RGB', (width_in_pixels, height_in_pixels), 'white')
            draw = ImageDraw.Draw(bitmap)
            
            # Barkodları çiz
            for barcode in barcodes:
                if barcode.get('data'):
                    self._draw_barcode(draw, barcode, dpi)
            
            # İkonları çiz
            for icon in icons:
                self._draw_icon(draw, icon, dpi)
            
            # Metinleri çiz
            for text in texts:
                self._draw_text(draw, text, dpi)
            
            # Monokrom bitmap'e dönüştür ve kaydet
            monochrome_bitmap = self._convert_to_monochrome(bitmap)
            monochrome_bitmap.save(file_path, 'BMP')
            
            self.logger.info(f"Etiket bitmap'i oluşturuldu: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Bitmap oluşturma sırasında hata: {e}")
            return False
    
    def _draw_barcode(self, draw: ImageDraw.Draw, barcode: Dict, dpi: int):
        """Barkod çiz"""
        try:
            # Barkod formatını belirle
            barcode_format = barcode.get('format', 'CODE_39')
            
            # QR kod oluştur
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(barcode['data'])
            qr.make(fit=True)
            
            # QR kod bitmap'ini oluştur
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Boyutları hesapla
            x_coord = int(barcode['x_coordinate'] * self.mm_to_inches * dpi)
            y_coord = int(barcode['y_coordinate'] * self.mm_to_inches * dpi)
            width = int(barcode['width'] * self.mm_to_inches * dpi)
            height = int(barcode['height'] * self.mm_to_inches * dpi)
            
            # QR kodu yeniden boyutlandır ve yerleştir
            qr_image = qr_image.resize((width, height))
            draw.bitmap((x_coord, y_coord), qr_image)
            
            # Metin ekle (eğer belirtilmişse)
            if barcode.get('text_alignment') != 'none':
                self._draw_barcode_text(draw, barcode, dpi)
                
        except Exception as e:
            self.logger.error(f"Barkod çizme sırasında hata: {e}")
    
    def _draw_barcode_text(self, draw: ImageDraw.Draw, barcode: Dict, dpi: int):
        """Barkod metnini çiz"""
        try:
            font_size = int(barcode.get('text_font_size', 12) * self.mm_to_inches * dpi)
            font_family = barcode.get('text_font_family', 'Arial')
            
            # Font oluştur - Türkçe karakterleri destekleyen font kullan
            font = None
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("C:/Windows/Fonts/calibri.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
            
            text = barcode['data']
            # Türkçe karakterleri güvenli hale getir
            safe_text = self._sanitize_text(text)
            
            text_bbox = draw.textbbox((0, 0), safe_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Metin pozisyonunu hesapla
            x_coord = int(barcode['x_coordinate'] * self.mm_to_inches * dpi)
            y_coord = int(barcode['y_coordinate'] * self.mm_to_inches * dpi)
            barcode_height = int(barcode['height'] * self.mm_to_inches * dpi)
            
            # Metni barkodun altına yerleştir
            text_x = x_coord
            text_y = y_coord + barcode_height + 5
            
            draw.text((text_x, text_y), safe_text, fill='black', font=font)
            
        except Exception as e:
            self.logger.error(f"Barkod metni çizme sırasında hata: {e}")
    
    def _draw_icon(self, draw: ImageDraw.Draw, icon: Dict, dpi: int):
        """İkon çiz"""
        try:
            # Base64 string'den image oluştur
            import base64
            from io import BytesIO
            
            icon_data = base64.b64decode(icon['base64_string'])
            icon_image = Image.open(BytesIO(icon_data))
            
            # Boyutları hesapla
            x_coord = int(icon['x_coordinate'] * self.mm_to_inches * dpi)
            y_coord = int(icon['y_coordinate'] * self.mm_to_inches * dpi)
            width = int(icon['width'] * self.mm_to_inches * dpi)
            height = int(icon['height'] * self.mm_to_inches * dpi)
            
            # İkonu yeniden boyutlandır ve yerleştir
            icon_image = icon_image.resize((width, height))
            draw.bitmap((x_coord, y_coord), icon_image)
            
        except Exception as e:
            self.logger.error(f"İkon çizme sırasında hata: {e}")
    
    def _draw_text(self, draw: ImageDraw.Draw, text: Dict, dpi: int):
        """Metin çiz"""
        try:
            font_size = int(text.get('font_size', 12) * self.mm_to_inches * dpi)
            font_family = text.get('font_family', 'Arial')
            
            # Font oluştur - Türkçe karakterleri destekleyen font kullan
            font = None
            try:
                # Önce Arial font'unu dene
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    # DejaVu Sans font'unu dene (Linux'ta yaygın)
                    font = ImageFont.truetype("DejaVuSans.ttf", font_size)
                except:
                    try:
                        # Windows'ta yaygın olan font'ları dene
                        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
                    except:
                        try:
                            font = ImageFont.truetype("C:/Windows/Fonts/calibri.ttf", font_size)
                        except:
                            # Hiçbiri bulunamazsa default font kullan
                            font = ImageFont.load_default()
            
            # Pozisyonu hesapla
            x_coord = int(text['x_coordinate'] * self.mm_to_inches * dpi)
            y_coord = int(text['y_coordinate'] * self.mm_to_inches * dpi)
            
            # Türkçe karakterleri güvenli hale getir
            safe_text = self._sanitize_text(text['content'])
            
            # Metni çiz
            draw.text((x_coord, y_coord), safe_text, fill='black', font=font)
            
        except Exception as e:
            self.logger.error(f"Metin çizme sırasında hata: {e}")
    
    def _sanitize_text(self, text: str) -> str:
        """Türkçe karakterleri güvenli hale getir"""
        try:
            # Türkçe karakterleri ASCII karşılıklarıyla değiştir
            turkish_chars = {
                'ç': 'c', 'Ç': 'C',
                'ğ': 'g', 'Ğ': 'G',
                'ı': 'i', 'I': 'I',
                'ö': 'o', 'Ö': 'O',
                'ş': 's', 'Ş': 'S',
                'ü': 'u', 'Ü': 'U'
            }
            
            sanitized_text = text
            for turkish_char, ascii_char in turkish_chars.items():
                sanitized_text = sanitized_text.replace(turkish_char, ascii_char)
            
            return sanitized_text
        except Exception as e:
            self.logger.warning(f"Metin temizleme sırasında hata: {e}")
            return text
    
    def _convert_to_monochrome(self, image: Image.Image) -> Image.Image:
        """RGB bitmap'i monokrom bitmap'e dönüştür"""
        try:
            # Gri tonlamaya çevir
            gray_image = image.convert('L')
            
            # Monokrom bitmap oluştur
            monochrome_image = Image.new('1', gray_image.size)
            
            # Piksel verilerini kopyala
            monochrome_image.putdata(gray_image.getdata())
            
            return monochrome_image
            
        except Exception as e:
            self.logger.error(f"Monokrom dönüştürme sırasında hata: {e}")
            return image 