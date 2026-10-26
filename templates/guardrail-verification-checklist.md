# Deterministik Doğrulama ve Korkuluklar Kontrol Listesi (Guardrail Verification Checklist)

> Bir yapay zekâ modelinin veya ajanının ürettiği kodun ana depoya (main branch) ya da canlı ortama girmeden önce geçmek zorunda olduğu kapılar.

---

## 🚦 Kapı 1: Statik Tip ve Sözleşme Uyumu
- [ ] **Sıfır Tip Hatası:** `tsc --strict`, `mypy --strict` veya dilin derleyicisi sıfır hata/uyarı ile tamamlandı mı?
- [ ] **Şema Doğrulama:** Girdi ve çıktılar (Pydantic / Zod / JSON Schema) ile çalışma zamanında sıkı şekilde doğrulanıyor mu?
- [ ] **Unknown Property Koruması:** Tanımlanmayan ekstra payload alanları otomatik olarak reddediliyor mu?

---

## 🧪 Kapı 2: Test Hatları ve Değişmezler (Invariants)
- [ ] **Birim Testler:** Temel başarı yolları (happy path) ve beklenen hata durumları kapsandı mı?
- [ ] **Sınır Değer Testleri (Boundary Conditions):** Boş string, 0, negatif sayılar, maksimum integer, geçersiz karakterler test edildi mi?
- [ ] **Eşzamanlılık (Concurrency & Race Conditions):** Aynı kaynağa eşzamanlı gelen 50+ istekte veri bozulması önlendi mi (Locking / Transaction Isolation)?
- [ ] **Idempotency Doğrulaması:** Aynı payload iki kez gönderildiğinde yan etki (side-effect) oluşmadığı kanıtlandı mı?

---

## 🔒 Kapı 3: Güvenlik ve Uyumluluk
- [ ] **Enjeksiyon Koruması:** SQLi, NoSQLi, Command Injection, XSS açıkları SAST aracıyla tarandı mı?
- [ ] **Gizli Anahtar Sızıntısı:** Kod tabanında hardcoded API key, token, şifre bulunmadığı doğrulandı mı (`trufflehog` / `gitleaks`)?
- [ ] **Bağımlılık Güvenliği:** Yeni eklenen bağımlılıklar CVE taramasından geçti mi (`npm audit` / `pip-audit`)?

---

## ⏱️ Kapı 4: Performans ve Kaynak Yönetimi
- [ ] **Bellek Sızıntısı:** Asenkron abonelikler, dosya handle'ları ve veritabanı bağlantıları düzgün kapatılıyor mu?
- [ ] **N+1 Sorgu Problemi:** İlişkisel sorgularda ORM kaynaklı gizli N+1 sorguları bulunmadığı kontrol edildi mi?
- [ ] **Timeout Politikası:** Dış dünyayla yapılan tüm HTTP/gRPC çağrılarında açık timeout tanımlandı mı?

---

## 🤖 Kapı 5: Model Halüsinasyon ve Kütüphane Taraması
- [ ] **Hayali Paket Taraması:** Model var olmayan (halüsinasyon ürünü) bir paket veya kütüphane import etmiş mi?
- [ ] **Deprecated API:** Kullanımdan kaldırılmış metotlar veya geçersiz parametreler kullanılmış mı?
