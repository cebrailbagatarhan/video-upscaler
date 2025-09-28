@echo off
echo APK Olusturma Rehberi (Windows)
echo ================================
echo.
echo 1. WSL Ubuntu Baslatma:
echo    wsl -d Ubuntu
echo.
echo 2. Ubuntu'da su komutlari calistirin:
echo.
echo # Proje klasorunu kopyala
echo cp -r /mnt/c/Users/cebra/OneDrive/Downloads/"video_coz" ~/video-upscaler
echo cd ~/video-upscaler
echo.
echo # Gerekli paketleri kur
echo sudo apt update
echo sudo apt install -y python3-pip git openjdk-8-jdk
echo pip3 install kivy buildozer cython
echo.
echo # APK olustur
echo buildozer android debug
echo.
echo 3. APK dosyasi ~/video-upscaler/bin/ klasorunde olusacak
echo.
echo WSL'yi baslatmak icin Enter'a basin...
pause > nul

wsl -d Ubuntu