# Stokastik Kod vs. Deterministik Filtre: Yapay Zekâ Çağında Doğrulama Felsefesi

> *"Yapay zekâ istatistiksel bir hayal gücüdür; mühendislik ise matematiksel bir kesinlik arayışıdır."*

---

## 1. Temel Çelişki: Olasılık vs. Kesinlik

Büyük Dil Modelleri (LLM'ler) temelde bir sonraki kelimeyi (token) önceki bağlama göre en yüksek olasılıkla tahmin eden otoregresif sistemlerdir.  
Bu durum şu anlama gelir:
- Model **hiçbir zaman bir kodun gerçekten doğru olup olmadığını bilmez.**
- Model yalnızca o kodun insan yazımı kod havuzlarına **ne kadar benzediğini bilir.**

Oysa bir roket yönlendirme yazılımı, bir bankacılık ödeme hattı veya bir veri tabanı motoru *"doğru gibi görünen"* kodla çalışamaz. 0.0001'lik bir olasılıksal sapma bile sistemin çökmesi veya verinin bozulması demektir.

```
       +-------------------------------------------------+
       |           STOKASTİK DÜNYA (Yapay Zekâ)          |
       |  - Olasılıksal tahmin                           |
       |  - Sezgisel desen eşleştirme                    |
       |  - Yüksek hızda alternatif üretimi              |
       +-------------------------------------------------+
                               │
                               ▼  (Üretilen Kod)
       +─────────────────────────────────────────────────+
       |         DETERMİNİSTİK ELEK (Mühendislik)        |
       |  1. Katı Tip Denetimi (Strict Type Systems)     |
       |  2. Değişmezler (Property-Based Verification)   |
       |  3. Statik Analiz & Güvenlik Taraması           |
       |  4. Biçimsel Doğrulama (Formal State Invariants)|
       +─────────────────────────────────────────────────+
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
      [TÜM TESTLER GEÇTİ]               [EN UFAK İHLAL]
              │                                 │
              ▼                                 ▼
       (Üretime Alınır)            (Hata Bağlamı Olarak
                                    Modele Geri Beslenir)
```

---

## 2. Deterministik Filtre Katmanları

### A. Tip Seviyesi (Compile-Time Guarantees)
Zayıf tipli dillerde yapay zekâ çalıştırmak mayın tarlasında koşmaya benzer.  
Tip sistemi, modelin üretebileceği anlamsız durumları daha derleme aşamasında imkansız kılar (*Make illegal states unrepresentable*).
- `any` veya gevşek tipler kesinlikle yasaktır.
- Tüm sınır değerler ve discriminated union'lar açıkça belirtilmelidir.

### B. Property-Based Testing (Özellik Tabanlı Sınama)
Klasik birim testler sadece geliştiricinin aklına gelen 3-5 senaryoyu test eder. Oysa Property-Based Test (örn. Python Hypothesis):
- Sisteme 10.000 rastgele kombinasyon (negatif sayılar, devasa stringler, null değerler, unicode karakterler) yollar.
- Her kombinasyonda sistem değişmezinin (invariant) korunup korunmadığını matematiksel olarak denetler.

### C. Statik Güvenlik ve Linter Bariyerleri
Modelin bilmeden veya halüsinasyon sonucu eklediği güvenlik açıklarını (SQL enjeksiyonu, güvensiz regex'ler, hardcoded anahtarlar) yakalamak için Semgrep ve Trivy gibi deterministik kurallar işletilir.

---

## 3. Özet
Orkestra şefi yapay zekâya *"akıllı olduğu"* için güvenmez. Orkestra şefi yapay zekâyı, arkasına kurduğu **deterministik elek mekanizmasının deliksizliğine** güvendiği için tam gaz çalıştırır.
