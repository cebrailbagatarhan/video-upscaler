#!/bin/bash

# GitHub Codespaces için APK oluşturma script'i
echo "=== Video & Fotoğraf Yükseltici APK Oluşturucu ==="
echo ""

# Sistem güncellemesi
echo "Sistem güncelleniyor..."
sudo apt update -y

# Gerekli paketleri kur
echo "Gerekli paketler kuruluyor..."
sudo apt install -y python3 python3-pip git zip unzip openjdk-8-jdk
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y autoconf libtool pkg-config zlib1g-dev libncurses5-dev
sudo apt install -y libncursesw5-dev libtinfo5 cmake

# Python paketlerini kur
echo "Python paketleri kuruluyor..."
pip3 install --upgrade pip
pip3 install kivy buildozer cython

# Buildozer ile APK oluştur
echo ""
echo "APK oluşturuluyor... (Bu işlem 20-30 dakika sürebilir)"
echo ""

buildozer android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ APK başarıyla oluşturuldu!"
    echo ""
    echo "📁 APK dosyası: bin/ klasöründe"
    echo "📱 Dosya adı: videoupscaler-0.1-armeabi-v7a-debug.apk"
    echo ""
    echo "APK'yı indirmek için:"
    echo "1. Sol paneldeki 'Explorer' sekmesini açın"
    echo "2. bin/ klasörüne gidin"
    echo "3. APK dosyasına sağ tıklayıp 'Download' seçin"
    echo ""
    ls -la bin/
else
    echo ""
    echo "❌ APK oluşturulurken hata oluştu!"
    echo "Hata detayları için buildozer loglarını kontrol edin"
fi