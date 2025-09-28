@echo off
echo Play Store icin AAB Olusturucu
echo ===============================
echo.

echo Bu script Play Store'a uygun Android App Bundle (AAB) olusturur.
echo.

echo Gereksinimler:
echo - WSL Ubuntu kurulu olmali
echo - Linux ortaminda buildozer kurulu olmali
echo.

echo Devam etmek icin Enter'a basin...
pause > nul

echo.
echo WSL Ubuntu baslatiliyor...
echo.

REM WSL'de build script'ini çalıştır
wsl -d Ubuntu bash -c "cd /mnt/c/Users/cebra/OneDrive/Downloads/'video_coz' && chmod +x build_playstore.sh && ./build_playstore.sh"

if %errorlevel% == 0 (
    echo.
    echo ✅ Play Store AAB basariyla olusturuldu!
    echo.
    echo 📁 AAB dosyasi: bin\ klasorunde
    echo 🎯 Google Play Console'da yayinlayabilirsiniz
) else (
    echo.
    echo ❌ AAB olusturulurken hata olustu!
    echo WSL Ubuntu'da gerekli paketlerin kurulu oldugunu kontrol edin.
)

echo.
pause