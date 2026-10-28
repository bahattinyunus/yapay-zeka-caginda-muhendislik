# Çoklu Ajan İş Akışı Orkestratörü (Multi-Agent Workflow Orchestrator)

Bu referans proje; **Mimar (Planner)**, **Kodlayıcı (Worker)**, **Red Team (Reviewer)** ve **Doğrulayıcı (Verifier)** ajanlarının
deterministik bir geri besleme döngüsünde nasıl otonom çalışabileceğini simüle eden çalışan bir Python motorudur.

---

## Çalışma Mantığı
```
[Gereksinim / Şartname]
         │
         ▼
[1. Mimar Ajan] ➔ İş Planı ve Sözleşmeleri Üretir
         │
         ▼
[2. Kodlayıcı Ajan] ➔ Sözleşmeye Uygun Kodu Yazar
         │
         ▼
[3. Red Team Ajanı] ➔ Sınır Değerleri ve Kötü Niyetli Girdileri Üretir
         │
         ▼
[4. Deterministik Doğrulayıcı] ➔ Testleri Koşar
         ├── ❌ Başarısız ➔ Hata Bağlamını Kodlayıcı Ajana İletir (Otonom İyileştirme)
         └── ✅ Başarılı  ➔ Kodu Onaylar ve Üretime Sevk Eder
```

Çalıştırmak için:
```bash
python workflow.py
```
