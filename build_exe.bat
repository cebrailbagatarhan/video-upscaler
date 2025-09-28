@echo off
echo Video Upscaler EXE Olusturucu
echo ==============================
echo.

REM PyInstaller'i kur
echo PyInstaller kuruluyor...
pip install pyinstaller

echo.
echo Tkinter uygulamasindan EXE olusturuluyor...

REM Tkinter uygulamasından EXE oluştur
pyinstaller --onefile --windowed --name="VideoUpscaler" 1.py

if %errorlevel% == 0 (
    echo.
    echo ✅ EXE basariyla olusturuldu!
    echo 📁 EXE dosyasi: dist\VideoUpscaler.exe
    echo.
    echo EXE dosyasini calistirmadan once FFmpeg'in sisteminizde 
    echo kurulu oldugunu ve PATH'e eklendigini kontrol edin.
    echo.
    echo FFmpeg indirme: https://ffmpeg.org/download.html
) else (
    echo.
    echo ❌ EXE olusturulurken hata olustu!
    echo Hata mesajlarini inceleyin.
)

echo.
pause
