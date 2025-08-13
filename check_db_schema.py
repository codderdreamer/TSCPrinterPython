import sqlite3
import os

# Veritabanı dosyasının yolunu kontrol et
db_path = "labelPrint.db"
if not os.path.exists(db_path):
    print(f"Veritabanı dosyası bulunamadı: {db_path}")
    exit(1)

print(f"Veritabanı dosyası bulundu: {db_path}")

# Veritabanına bağlan
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tüm tabloları listele
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\nMevcut tablolar:")
for table in tables:
    print(f"  - {table[0]}")

# InputInfo tablosunun şemasını kontrol et
print("\nInputInfo tablosu şeması:")
try:
    cursor.execute("PRAGMA table_info(InputInfo);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
except Exception as e:
    print(f"InputInfo tablosu bulunamadı: {e}")

# IconInfo tablosunun şemasını kontrol et
print("\nIconInfo tablosu şeması:")
try:
    cursor.execute("PRAGMA table_info(IconInfo);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
except Exception as e:
    print(f"IconInfo tablosu bulunamadı: {e}")

# BarcodeInfo tablosunun şemasını kontrol et
print("\nBarcodeInfo tablosu şeması:")
try:
    cursor.execute("PRAGMA table_info(BarcodeInfo);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
except Exception as e:
    print(f"BarcodeInfo tablosu bulunamadı: {e}")

# LabelSetting tablosunun şemasını kontrol et
print("\nLabelSetting tablosu şeması:")
try:
    cursor.execute("PRAGMA table_info(LabelSetting);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
except Exception as e:
    print(f"LabelSetting tablosu bulunamadı: {e}")

# InputInfo tablosundaki verileri kontrol et
print("\nInputInfo tablosundaki veriler:")
try:
    cursor.execute("SELECT * FROM InputInfo LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  - {row}")
except Exception as e:
    print(f"InputInfo verileri okunamadı: {e}")

conn.close() 