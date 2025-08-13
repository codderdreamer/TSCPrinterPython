#!/usr/bin/env python3
"""
TSC Printer Python Backend
Bu dosya uygulamayı başlatmak için kullanılır.
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Logs dizinini oluştur
    os.makedirs('logs', exist_ok=True)
    
    # Uygulamayı başlat
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    ) 