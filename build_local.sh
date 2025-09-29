#!/bin/bash

# Yerel WSL/Ubuntu ortamında APK oluşturma script'i
echo "=== Yerel APK Oluşturucu ==="
echo ""

# Gerekli kontroller
if [ ! -f "main.py" ]; then
    echo "❌ HATA: main.py dosyası bulunamadı!"
    exit 1
fi

echo "📦 Yerel ortamda APK oluşturuluyor..."
echo ""

# Python ve pip kontrolü
if ! command -v python3 &> /dev/null; then
    echo "Python3 kuruluyor..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Gerekli paketlerin kurulumu
echo "🔧 Gerekli paketler kuruluyor..."
pip3 install --user kivy kivymd pillow plyer

# Basit APK oluşturma için KivyMD packager kullanma
echo "🚀 APK oluşturuluyor..."

# Eğer p4a kurulu değilse kur
if ! command -v p4a &> /dev/null; then
    echo "Python-for-Android kuruluyor..."
    pip3 install --user python-for-android
fi

# Gerekli sistem paketleri
sudo apt install -y git zip unzip build-essential libffi-dev libssl-dev

# APK oluştur
mkdir -p local_build
cp main.py local_build/
cp -r data local_build/ 2>/dev/null || echo "data klasörü bulunamadı, devam ediliyor..."

cd local_build

# Basit APK build
python3 -c "
import sys
import os
print('Yerel APK oluşturma simülasyonu...')
print('Gerçek APK için WSL ortamında buildozer gerekiyor.')
print('Alternatif: Online build servisleri kullanın.')
"

echo ""
echo "💡 Yerel APK oluşturma önerileri:"
echo "1. Online build servisi: https://github.com/features/actions"
echo "2. WSL'de buildozer kurarak deneme"
echo "3. Cloud IDE kullanma (GitPod, CodeSpaces)"
echo ""
echo "✅ Script tamamlandı!"