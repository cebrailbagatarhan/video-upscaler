# Video Resolution Scaler — FFmpeg/Lanczos

Yerel video ve fotoğraf dosyalarının çıktı çözünürlüğünü FFmpeg'in Lanczos filtresiyle değiştiren deneysel masaüstü/Android arayüzü.

> [!IMPORTANT]
> Bu proje **AI upscaler veya super-resolution modeli değildir**. Kodda Real-ESRGAN, SwinIR ya da öğrenilmiş bir restorasyon ağı yoktur. `scale=...:flags=lanczos` ile klasik yeniden örnekleme yapar. 720p bir videoyu 4K boyutlarına çıkarmak yeni gerçek detay üretmez.

## Ne yapıyor?

| Alan | Mevcut uygulama |
| --- | --- |
| Video ölçekleme | FFmpeg `scale` filtresi + Lanczos |
| Fotoğraf ölçekleme | FFmpeg `scale` filtresi + Lanczos |
| UI | Kivy; ayrıca eski Tkinter prototipi (`1.py`) |
| İşleme | Yerel cihazda subprocess ile FFmpeg |
| AI inference | Yok |
| Kalite benchmark'ı | Henüz yok |

Desteklenen formatlar kullanılan FFmpeg build'ine bağlıdır. UI; MP4/AVI/MKV/MOV/WMV ve JPG/JPEG/PNG/BMP/TIFF uzantılarını seçmeye izin verir, fakat codec uyumluluğu ayrıca test edilmelidir.

## Yerel kullanım

Python ve FFmpeg kurulu olmalıdır:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

FFmpeg'in `PATH` üzerinde olduğunu doğrulayın:

```bash
ffmpeg -version
```

## Android build durumu

GitHub Actions akışı APK üretildiğini iddia etmez; yalnızca kaynak sentaksını ve release-secret hijyenini doğrular. Android/Kivy paketleme için Linux/WSL, Java, Android SDK/NDK ve Buildozer gerekir.

Debug build:

```bash
buildozer android debug
```

Release build için imzalama bilgileri repoda tutulmaz. `build_playstore.sh` şu ortam değişkenlerini zorunlu kılar:

```bash
export P4A_RELEASE_KEYSTORE=/secure/outside-repo/upload-key.keystore
export P4A_RELEASE_KEYSTORE_PASSWD='...'
export P4A_RELEASE_KEYALIAS='...'
export P4A_RELEASE_KEYALIAS_PASSWD='...'
./build_playstore.sh
```

Değerleri shell history'ye yazmak yerine yerel secret manager veya CI secret store kullanın. Keystore dosyasını repo dışında saklayın. Üretilen `.apk`/`.aab` dosyaları kaynak kontrolüne değil release artifact alanına gönderilmelidir.

## Güvenlik

Release keystore, signing password veya imzalı binary commit edilmemelidir. Kontrol:

```bash
python scripts/check_release_secrets.py
```

Geçmişte repoya eklenmiş bir signing key yalnızca son commit'ten silinerek güvenli hale gelmez; kullanıldıysa compromised kabul edilmeli ve rotate edilmelidir. Ayrıntı için [`SECURITY.md`](SECURITY.md) dosyasına bakın.

## Kaliteyi nasıl ölçmeli?

Lanczos için dürüst baseline:

- aynı kaynak klip/fotoğraf ve aynı hedef çözünürlük
- süre, CPU/RAM kullanımı ve çıktı boyutu
- bilinen yüksek çözünürlüklü referanstan oluşturulan düşük çözünürlüklü giriş
- PSNR ve SSIM; algısal karşılaştırma için LPIPS

AI özelliği eklenecekse Real-ESRGAN/SwinIR gibi model adı, ağırlık lisansı, checkpoint hash'i ve cihaz açıkça yazılmalı; aynı girişlerde Lanczos'a karşı kalite ve hız tablosu yayımlanmalıdır. Bu ölçümler yapılmadan “professional enhancement” veya “AI quality” iddiası kullanılmamalıdır.

## Sınırlamalar

- Klasik scaling sıkıştırma artefaktlarını veya bulanıklığı güvenilir biçimde geri getirmez.
- Büyük çözünürlükler işlem süresi ve depolama maliyetini ciddi biçimde artırabilir.
- Android cihazda FFmpeg binary/codec bulunabilirliği build'e bağlıdır.
- Repo şu anda doğrulanmış APK/AAB üretim pipeline'ı sunmaz.
- Kalite ve hız için commit edilmiş benchmark sonucu yoktur.

