@echo off
echo Docker ile APK Olusturucu
echo =========================
echo.

REM Docker'in calisip calismadigini kontrol et
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Docker bulunamadi!
    echo Lutfen Docker Desktop'i kurun: https://docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker bulundu, APK olusturuluyor...
echo Bu islem 30-45 dakika surebilir...
echo.

REM Docker container ile build
docker-compose up

if %errorlevel% == 0 (
    echo.
    echo ✅ APK basariyla olusturuldu!
    echo 📁 APK dosyasi: bin\ klasorunde
    echo.
    dir bin\*.apk
) else (
    echo.
    echo ❌ APK olusturulurken hata olustu!
    echo Docker loglarini kontrol edin.
)

echo.
pause