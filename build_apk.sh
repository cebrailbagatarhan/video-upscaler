#!/bin/bash

# APK (Android Application Package) oluşturma script'i
echo "=== APK Builder ==="
echo ""

# Gerekli kontroller
if [ ! -f "buildozer.spec" ]; then
    echo "❌ HATA: buildozer.spec dosyası bulunamadı!"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ HATA: main.py dosyası bulunamadı!"
    exit 1
fi

echo "📦 APK dosyası oluşturuluyor..."
echo ""

# Önceki build'leri temizle
echo "🧹 Önceki build dosyaları temizleniyor..."
buildozer android clean

# Debug APK oluştur
echo "🚀 Debug APK oluşturuluyor..."
echo "⚠️  Bu işlem 5-15 dakika sürebilir!"
echo ""

buildozer android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ APK başarıyla oluşturuldu!"
    echo ""
    echo "📁 APK dosyası: bin/ klasöründe"
    echo "📱 Dosya formatı: .apk (Android Application Package)"
    echo ""
    echo "🎯 Telefona yükleme adımları:"
    echo "1. Telefonunuzda 'Geliştirici Seçenekleri'ni açın."
    echo "2. 'USB Hata Ayıklama'yı etkinleştirin."
    echo "3. Telefonu bilgisayara bağlayın."
    echo "4. APK dosyasını telefonunuza kopyalayın."
    echo "5. Dosya yöneticisinden APK'yı bulup yükleyin."
    echo ""
    ls -la bin/*.apk
else
    echo ""
    echo "❌ APK oluşturulurken hata oluştu!"
    echo ""
    echo "🔧 Sorun giderme önerileri:"
    echo "1. Java 8 kurulu olduğundan emin olun"
    echo "2. Android SDK güncel olduğundan emin olun"
    echo "3. buildozer android clean komutu ile temizleyin"
    echo "4. Hata loglarını inceleyin"
fi

echo ""
echo "📚 Daha fazla bilgi:"
echo "- Buildozer: https://buildozer.readthedocs.io/"