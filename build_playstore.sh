#!/bin/bash

# Play Store için AAB (Android App Bundle) oluşturma script'i
echo "=== Play Store Release Builder ==="
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

echo "📦 Play Store uyumlu AAB dosyası oluşturuluyor..."
echo ""

# Önceki build'leri temizle
echo "🧹 Önceki build dosyaları temizleniyor..."
buildozer android clean

# Release AAB oluştur (Play Store için)
echo "🚀 Release AAB oluşturuluyor..."
echo "⚠️  Bu işlem 30-60 dakika sürebilir!"
echo ""

buildozer android release

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Play Store uyumlu AAB başarıyla oluşturuldu!"
    echo ""
    echo "📁 AAB dosyası: bin/ klasöründe"
    echo "📱 Dosya formatı: .aab (Android App Bundle)"
    echo ""
    echo "🎯 Play Store'a yükleme adımları:"
    echo "1. Google Play Console'a giriş yapın"
    echo "2. Yeni uygulama oluşturun"
    echo "3. AAB dosyasını yükleyin"
    echo "4. Store listing bilgilerini doldurun"
    echo "5. İnceleme için gönderin"
    echo ""
    echo "📋 Gerekli Play Store bilgileri:"
    echo "- Uygulama adı: Video Photo Upscaler"
    echo "- Kategori: Photography"
    echo "- Hedef kitle: 13+ yaş"
    echo "- Açıklama: README.md dosyasında mevcut"
    echo ""
    ls -la bin/*.aab
else
    echo ""
    echo "❌ AAB oluşturulurken hata oluştu!"
    echo ""
    echo "🔧 Sorun giderme önerileri:"
    echo "1. Java 8 kurulu olduğundan emin olun"
    echo "2. Android SDK güncel olduğundan emin olun"
    echo "3. buildozer android clean komutu ile temizleyin"
    echo "4. Hata loglarını inceleyin"
fi

echo ""
echo "📚 Daha fazla bilgi:"
echo "- Play Console: https://play.google.com/console"
echo "- AAB Rehberi: https://developer.android.com/guide/app-bundle"