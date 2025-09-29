@echo off
echo Yerel APK Olusturucu
echo =====================
echo.

echo Bu script yerel bilgisayarda APK olusturma icin alternatif cozumler sunar.
echo.

echo Secenekler:
echo.
echo 1. Online Build Servisleri:
echo    - GitHub Codespaces
echo    - GitPod
echo    - Repl.it
echo.
echo 2. Cloud IDE Alternatifleri:
echo    - https://gitpod.io/#https://github.com/cebrailbagatarhan/video-upscaler
echo    - GitHub Codespaces (repository'de . tusuna basin)
echo.
echo 3. WSL Ubuntu'da Buildozer:
echo    wsl
echo    cd /mnt/c/Users/cebra/OneDrive/Downloads/video_coz
echo    sudo apt install python3-pip
echo    pip3 install buildozer
echo    buildozer android debug
echo.
echo 4. PyInstaller ile Windows EXE:
echo    pip install pyinstaller kivy
echo    pyinstaller --onefile main.py
echo.

choice /c 1234 /n /m "Hangi secenegi denemek istiyorsunuz? (1-4): "

if errorlevel 4 goto :exe
if errorlevel 3 goto :wsl
if errorlevel 2 goto :cloud
if errorlevel 1 goto :online

:online
echo.
echo GitHub Actions runner sorunlari icin online alternatifler:
echo.
echo 1. GitPod: https://gitpod.io/#https://github.com/cebrailbagatarhan/video-upscaler
echo 2. GitHub Codespaces: Repository'de . (nokta) tusuna basin
echo 3. Repl.it: https://replit.com (GitHub repo import edin)
echo.
goto :end

:cloud
echo.
echo Cloud IDE'lerde APK olusturma:
echo 1. GitPod.io'ya gidin
echo 2. Repository URL'nizi girin
echo 3. Terminal'de: buildozer android debug
echo.
goto :end

:wsl
echo.
echo WSL Ubuntu'da calistirilacak komutlar:
echo.
echo wsl
echo cd /mnt/c/Users/cebra/OneDrive/Downloads/video_coz
echo sudo apt update
echo sudo apt install -y python3-pip git zip unzip
echo pip3 install buildozer
echo buildozer android debug
echo.
goto :end

:exe
echo.
echo Windows EXE olusturuluyor...
echo.
pip install pyinstaller kivy kivymd pillow plyer
if %errorlevel% == 0 (
    pyinstaller --onefile --windowed main.py
    echo.
    echo ✅ EXE dosyasi dist klasorunde olusturuldu!
) else (
    echo ❌ Paket kurulumunda hata olustu!
)
goto :end

:end
echo.
pause