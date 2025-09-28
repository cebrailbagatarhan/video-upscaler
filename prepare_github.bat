@echo off
echo GitHub icin Dosya Hazirlama
echo ===========================
echo.

echo Gerekli dosyalar ZIP'leniyor...

REM Gerekli dosyaları belirle
set FILES=main.py buildozer.spec requirements.txt README.md playstore_metadata.md

REM ZIP dosyası oluştur (PowerShell ile)
powershell -Command "Compress-Archive -Path main.py,buildozer.spec,requirements.txt,README.md,playstore_metadata.md -DestinationPath github_upload.zip -Force"

if %errorlevel% == 0 (
    echo ✅ Dosyalar github_upload.zip olarak hazirland!
    echo.
    echo GitHub'a yukleme adimlari:
    echo 1. https://github.com sitesine gidin
    echo 2. Yeni repository olusturun: "video-upscaler"
    echo 3. github_upload.zip dosyasini acin
    echo 4. Icindeki dosyalari GitHub'a yukleyin
    echo 5. Code ^> Codespaces ^> Create codespace tiklayin
    echo 6. Terminalda: buildozer android debug
    echo.
    echo ZIP dosyasi hazir: github_upload.zip
) else (
    echo ❌ ZIP olusturulamadi!
)

echo.
pause