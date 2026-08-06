# Güç Sistemleri Günlük & Haftalık Akademik Yayın Tarama Otomasyonu

Bu proje; Akıllı Şebekelerde Koruma Sistemleri, P2P Enerji Ticareti ve Elektrikli Araçların Şebekeye Etkileri alanlarındaki yeni bilimsel yayınları taranıp Türkçe özetleyen ve e-posta olarak teslim eden bir otomasyon sistemidir.

## Özellikler
- ⚡ **Günlük Raporlar**: Son 48 saatte yayınlanan makalelerin Türkçe başlık, 3 maddelik özet, önemli katkı ve orijinal linkleri.
- 📊 **Haftalık İstatistikler & Trend Raporu (Pazar Günleri)**: Hot topics, son 7 günün yayın istatistikleri ve genel değerlendirme.
- 🎓 **Öğrencilere Tez Önerileri**: Lisans bitirme projeleri ve Yüksek Lisans / Doktora tezleri için yayın kaynaklı konu fikirleri.
- 🕒 **GitHub Actions Entegrasyonu**: Her gün sabah 08:00'de (TSİ) sıfır maliyetle otomatik çalışma.

---

## 🛠️ GitHub Actions Kurulum Adımları (E-posta Almak İçin)

Projeyi GitHub'a yükledikten sonra repository'nizin **Settings > Secrets and variables > Actions** bölümüne gidip şu gizli değişkenleri (Secrets) eklemeniz yeterlidir:

| Secret Adı | Açıklama | Örnek Değer |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google AI Studio'dan alınan ücretsiz API Key | `AIzaSy...` |
| `SENDER_EMAIL` | Raporu gönderecek Gmail/Outlook adresi | `ornek@gmail.com` |
| `SENDER_PASSWORD` | Gmail 2 adımlı doğrulama "Uygulama Şifresi" | `xxxx yyyy zzzz tttt` |
| `RECIPIENT_EMAIL` | Raporların geleceği e-posta adresiniz | `hedef@gmail.com` |
| `SMTP_SERVER` | SMTP Sunucusu (Gmail için varsayılan) | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP Portu (Gmail TLS varsayılan) | `587` |

---

## 💻 Yerel Bilgisayarda Test Etme

Sistemi kendi bilgisayarınızda test etmek için terminalde şu komutları çalıştırabilirsiniz:

```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. Günlük testi çalıştırın (Rapor reports/ klasörüne kaydedilir)
python main.py --mode daily

# 3. Haftalık testi çalıştırın
python main.py --mode weekly
```

---

## ⚙️ Yeni Konu Ekleme veya Özelleştirme

`config.py` dosyasındaki `TOPICS` sözlüğünü düzenleyerek yeni konular veya alternatif arama kelimeleri ekleyebilirsiniz:

```python
TOPICS["bms"] = {
    "title": "Batarya Yönetim Sistemleri (BMS)",
    "description": "Battery Management Systems, State of Charge & Health Estimation",
    "arxiv_query": 'cat:eess.SY AND (abs:"battery management system" OR abs:"soc estimation")',
    "openalex_query": "battery management system OR SOC estimation",
    "keywords": ["bms", "battery management", "soc estimation", "soh estimation"]
}
```
