# TSC Printer Python Backend

Bu proje, TSC printer'ları ile etiket yazdırma işlemlerini gerçekleştiren Python backend uygulamasıdır.

## Özellikler

- TSC printer'ları ile iletişim
- Bitmap etiket oluşturma
- Barkod oluşturma
- Metin ve ikon yerleştirme
- Bluetooth ve karton etiketleri için farklı ayarlar
- REST API endpoints
- SQLite veritabanı desteği
- React frontend (build edilmiş)

## Kurulum

### 1. Backend Kurulumu

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Environment dosyasını kopyala
cp env.example .env
```

### 2. Frontend Build

```bash
# Frontend'i build et (otomatik olarak backend'e kopyalanır)
python build_frontend.py

# Veya manuel olarak:
cd frontend
npm install
npm run build
```

## Çalıştırma

```bash
# Uygulamayı başlat
python run.py
```

Uygulama http://localhost:5000 adresinde çalışacak ve React frontend'i otomatik olarak serve edecektir.

## API Endpoints

- `POST /api/label/print` - Etiket yazdırma
- `GET /api/label/settings` - Printer ayarlarını getir
- `POST /api/label/settings` - Printer ayarlarını güncelle
- `GET /health` - Sağlık kontrolü

## Geliştirme

### Frontend Geliştirme

```bash
cd frontend
npm start
```

Frontend http://localhost:3000 adresinde çalışacak ve backend API'sine proxy üzerinden bağlanacaktır.

### Production Build

```bash
# Frontend'i build et
python build_frontend.py

# Backend'i başlat
python run.py
```

## Dosya Yapısı

```
TSCPrinterPython/
├── app.py                    # Ana Flask uygulaması
├── config.py                 # Konfigürasyon
├── models.py                 # Veritabanı modelleri
├── dto.py                    # Data Transfer Objects
├── tsc_printer_service.py    # TSC printer servisi
├── label_bitmap_generator.py # Bitmap oluşturma
├── build_frontend.py         # Frontend build script'i
├── run.py                    # Uygulama başlatma
├── requirements.txt          # Python bağımlılıkları
├── env.example              # Örnek environment
├── frontend/                # React uygulaması
│   ├── build/               # Build edilmiş dosyalar (otomatik oluşur)
│   ├── src/                 # React kaynak kodları
│   └── package.json         # Node.js bağımlılıkları
└── logs/                    # Log dosyaları
``` 