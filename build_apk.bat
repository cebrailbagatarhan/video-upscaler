@echo off
echo APK Olusturucu
echo ===============================
echo.

echo Bu script APK olusturur.
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
wsl -d Ubuntu bash -c "cd /mnt/c/Users/cebra/OneDrive/Downloads/'video_coz' && chmod +x build_apk.sh && ./build_apk.sh"

if %errorlevel% == 0 (
    echo.
    echo ✅ APK basariyla olusturuldu!
    echo.
    echo 📁 APK dosyasi: bin\ klasorunde
) else (
    echo.
    echo ❌ APK olusturulurken hata olustu!
    echo WSL Ubuntu'da gerekli paketlerin kurulu oldugunu kontrol edin.
)

echo.
pause
