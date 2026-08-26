# Video Photo Resizer

Kivy tabanlı bir Lanczos yeniden örnekleme uygulaması. Bu proje bir yapay zekâ
veya super-resolution modeli içermez; yeni ayrıntı üretmez. Fotoğrafları Pillow
ile, masaüstündeki videoları ise sistemde kurulu FFmpeg ile daha büyük ya da
daha küçük çözünürlüklere ölçekler.

## Gerçek yetenekler

- Fotoğraf: JPG, JPEG, PNG, BMP ve TIFF; Pillow/Lanczos ile en-boy oranını korur.
- Video (masaüstü): FFmpeg bulunduğunda MP4, AVI, MKV, MOV, WMV ve FLV girdileri;
  Lanczos ölçekleme, H.264 video ve AAC ses çıktısı.
- İşlem cihazda çalışır; uygulama kodunda yükleme veya analiz servisi yoktur.
- Tek dosya işlenir. Batch processing, AI enhancement ve gerçek zamanlı
  ilerleme göstergesi henüz yoktur.

Ölçekleme, kaynak görüntünün gerçek ayrıntısını artırmaz. Düşük çözünürlüklü
girdiler büyütüldüğünde daha fazla piksel elde edilir; daha fazla gerçek bilgi
elde edilmez.

## Masaüstünde çalıştırma

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Video işleme için `ffmpeg` çalıştırılabilir dosyası ayrıca kurulmalı ve PATH
içinde bulunmalıdır. Fotoğraf işleme FFmpeg gerektirmez.

## Android durumu

Android paketi deneyseldir. Fotoğraf yeniden boyutlandırma Pillow ile paketlenir;
video işleme ise APK içinde bir FFmpeg çalıştırılabilir dosyası bulunmadığından
Android'de bilerek devre dışıdır. Uygulama bu durumu işlem başlamadan açıkça
bildirir. Dosya erişimi ve mağaza dağıtımı fiziksel cihaz üzerinde ayrıca test
edilmelidir.

`buildozer.spec` API 36'yı hedefler. Güncel Google Play gereksinimlerini ve
python-for-android uyumluluğunu her sürüm öncesinde tekrar doğrulayın.

```bash
buildozer android debug
```

CI şu anda APK üretmiş gibi davranmaz; yalnızca Python sözdizimini ve repoda
imzalama/build artifact'i bulunmadığını doğrular.

## Release güvenliği

Release anahtarı veya parolası repoya eklenmemelidir. Önceden yayınlanmış anahtar
compromised kabul edilmelidir. Rotasyon ve history purge adımları için
[`SECURITY.md`](SECURITY.md) dosyasını okuyun.

## Lisans

MIT License.
