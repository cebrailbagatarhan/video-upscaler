# GitHub Codespaces ile APK Oluşturma Rehberi

Bu yöntem Windows'ta sorun yaşıyorsanız en kolay çözümdür.

## Adım 1: GitHub'a Proje Yükleme

1. **GitHub hesabı açın** (eğer yoksa): https://github.com
2. **Yeni repository oluşturun**: "video-upscaler" adında
3. **Dosyaları yükleyin**:
   - main.py
   - buildozer.spec
   - requirements.txt
   - README.md

## Adım 2: Codespace Açma

1. **Repository sayfasında** yeşil "Code" butonuna tıklayın
2. **"Codespaces" sekmesini** seçin
3. **"Create codespace on main"** tıklayın
4. **2-3 dakika bekleyin** (otomatik kurulum)

## Adım 3: APK Oluşturma

Codespace açıldığında terminal'de şu komutları çalıştırın:

```bash
# Gerekli paketleri kur
sudo apt update
sudo apt install -y openjdk-8-jdk
pip install kivy buildozer cython

# APK oluştur
buildozer android debug
```

## Adım 4: APK İndirme

1. **Sol panelde** "Explorer" sekmesini açın
2. **bin/ klasörüne** gidin
3. **APK dosyasına sağ tıklayın**
4. **"Download"** seçin

## Avantajları:
✅ Windows'ta sorun yok
✅ Otomatik kurulum
✅ Ücretsiz (aylık 120 saat)
✅ Güçlü sunucu
✅ Hızlı build

## Dosya Yapısı:
```
repository/
├── main.py
├── buildozer.spec
├── requirements.txt
├── README.md
└── bin/ (oluşacak)
    └── *.apk
```

Bu yöntem %100 çalışır ve Windows'ta herhangi bir kurulum gerektirmez!