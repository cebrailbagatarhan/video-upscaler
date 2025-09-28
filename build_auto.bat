@echo off
echo Windows APK/AAB Olusturucu - Otomatik Kurulum
echo =============================================
echo.

echo 1. WSL Ubuntu baslatiliyor...
wsl -d Ubuntu -e bash -c "echo 'Ubuntu baslatildi'"

if %errorlevel% neq 0 (
    echo ❌ WSL Ubuntu baslatma hatasi!
    echo.
    echo Cozum onerileri:
    echo 1. WSL'yi yeniden baslatin: wsl --restart
    echo 2. Ubuntu'yu manuel baslatin: wsl -d Ubuntu
    echo 3. WSL'yi sifirlatin: wsl --unregister Ubuntu
    pause
    exit /b 1
)

echo ✅ WSL Ubuntu baslatildi
echo.

echo 2. Proje klasorunu kopyalaniyor...
wsl -d Ubuntu -e bash -c "cp -r /mnt/c/Users/cebra/OneDrive/Downloads/'vıdeo coz' ~/video-upscaler 2>/dev/null || echo 'Klasor zaten mevcut'"

echo 3. Gerekli paketler kuruluyor...
echo Bu islem 5-10 dakika surebilir...
wsl -d Ubuntu -e bash -c "
cd ~/video-upscaler
sudo apt update -y
sudo apt install -y python3 python3-pip openjdk-8-jdk git
pip3 install --user kivy buildozer cython
echo 'Paketler kuruldu'
"

if %errorlevel% neq 0 (
    echo ❌ Paket kurulum hatasi!
    pause
    exit /b 1
)

echo ✅ Paketler basariyla kuruldu
echo.

echo 4. APK/AAB olusturuluyor...
echo Bu islem 30-60 dakika surebilir...
echo.

wsl -d Ubuntu -e bash -c "
cd ~/video-upscaler
export PATH=\$PATH:\$HOME/.local/bin
buildozer android debug
"

if %errorlevel% == 0 (
    echo.
    echo ✅ APK basariyla olusturuldu!
    echo.
    echo 📁 APK dosyasi WSL'de: ~/video-upscaler/bin/
    echo Windows'ta erismek icin: \\wsl$\Ubuntu\home\[kullanici-adi]\video-upscaler\bin\
    echo.
    echo APK dosyasini Windows'a kopyalaniyor...
    wsl -d Ubuntu -e bash -c "cp ~/video-upscaler/bin/*.apk /mnt/c/Users/cebra/OneDrive/Downloads/'vıdeo coz'/ 2>/dev/null || echo 'APK kopyalanamadi'"
    
    echo.
    echo APK dosyalari:
    dir *.apk 2>nul
) else (
    echo.
    echo ❌ APK olusturulurken hata olustu!
    echo.
    echo Hata giderme:
    echo 1. WSL Ubuntu'da manuel kontrol: wsl -d Ubuntu
    echo 2. Hata loglarini inceleyin
    echo 3. Tekrar deneyin: buildozer android clean
)

echo.
pause