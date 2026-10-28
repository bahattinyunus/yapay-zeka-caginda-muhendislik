# Eval-Güdümlü Geliştirme (Eval-Driven Development - EDD)

> *"Geleneksel dünyada Test-Driven Development (TDD) ne idiyse, yapay zekâ çağında Eval-Driven Development (EDD) odur. Ancak aradaki fark şudur: TDD insan hatalarını yakalar; EDD ise olasılıksal makinelerin stokastik sapmalarını evcilleştirir."*

---

## 1. TDD'den EDD'ye Evrim

Klasik yazılım mühendisliğinde TDD (Test-Driven Development) döngüsü üç adımdan oluşurdu:
1. **Red:** Önce başarısız bir test yaz.
2. **Green:** Testi geçecek asgari kodu yaz.
3. **Refactor:** Kodu temizle.

Yapay zekâ modellerinin kod ürettiği çağda bu döngü yetersiz kalmaktadır. Çünkü model, tekil bir testi geçecek şekilde "kurnaz" (overfitted) bir kod üretebilir; ancak sınır durumlarda dağılabilir.

### EDD Döngüsü (Eval-Driven Development):
```
[1. Değişmezler & Veri Seti] ➔ Binlerce rastgele ve sınır durum senaryosu tanımla
           │
           ▼
[2. Otonom Üretim]          ➔ Ajanlara şartnameyi ve eval kriterlerini ver
           │
           ▼
[3. İstatistiki Sınama]     ➔ Modeli %99.99 başarı oranına kadar iterasyona sok
           │
           ▼
[4. Kendi Kendini İyileştirme]➔ Hata çıktısını (diff & failure trace) ajana geri besle
```

---

## 2. Deterministik Evals vs. LLM-as-a-Judge

Piyasada sıkça önerilen *"Bir LLM'in yazdığı kodu başka bir LLM'e denetletme (LLM-as-a-judge)"* yaklaşımı, profesyonel mühendislik için yetersizdir:
- **İki olasılıksal modelin anlaşması kesinlik üretmez; sadece ortak bir halüsinasyon riski doğurur.**
- Mühendislikte kabul kriteri deterministik olmak zorundadır: **Derleyici, Property Testleri, Zaman Aşımı Sınırları ve Değişmez Matematiksel Eşitlikler.**

📘 *Örnek eval harness için:* [`templates/eval_harness_example.py`](../templates/eval_harness_example.py)
