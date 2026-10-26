# Spesifikasyon Tabanlı Geliştirme Şablonu (Spec-First Architecture)

> Bu şablon, yapay zekâ modellerine veya otonom kodlama ajanlarına görev vermeden önce sistem mimarı (orkestra şefi) tarafından doldurulması gereken şartname belgesidir.

---

## 1. Problem Tanımı ve Kapsam
- **Modül / Servis Adı:** `[Servis veya Modül Adı]`
- **Amaç:** `[Bu servis neyi çözer? İş değeri nedir?]`
- **Kapsam Dışı (Out of Scope):** `[Neleri KESİNLİKLE yapmayacak?]`

---

## 2. API ve Veri Sözleşmeleri (Contracts)

### 2.1 Girdi / Çıktı Şemaları (TypeScript / JSON Schema / Pydantic)
```typescript
// Girdi Modeli
interface ServiceRequest {
  idempotencyKey: string; // UUIDv4
  userId: string;
  amountInCents: number;  // Pozitif tamsayı
  currency: "TRY" | "USD" | "EUR";
  timestamp: string;      // ISO 8601 UTC
}

// Çıktı Modeli
interface ServiceResponse {
  transactionId: string;
  status: "SUCCESS" | "FAILED" | "PENDING";
  processedAt: string;
  errorCode?: string;
}
```

---

## 3. Sistemin Değişmezleri (Invariants & Business Rules)
Bu kurallar her ne olursa olsun ASLA ihlal edilemez:
1. **Değişmez 1:** `amountInCents` değeri her zaman `> 0` olmalıdır.
2. **Değişmez 2:** Aynı `idempotencyKey` ile gelen ikinci bir istek yeni bir işlem yaratamaz; ilk işlemin sonucunu döndürmelidir.
3. **Değişmez 3:** Durum makinesi geçişleri kesinlikle deterministiktir:
   - `INITIAL` ➔ `PENDING` ➔ `CONFIRMED`
   - `INITIAL` ➔ `PENDING` ➔ `REJECTED`
   - Başka hiçbir geçişe izin verilmez.

---

## 4. Arıza Modları ve Dayanıklılık (Failure Modes & Resilience)
- **Ağ Zaman Aşımı (Network Timeout):** 3000ms üzeri istekler iptal edilmeli, exponential backoff ile en fazla 3 kez denenmelidir.
- **Veritabanı Kilitlenmesi:** Deadlock durumunda işlem `TRANSACTION_ROLLBACK` ile geri alınmalıdır.
- **Üçüncü Parti Servis Kesintisi:** Circuit Breaker devreye girmeli ve fallback mekanizması çalışmalıdır.

---

## 5. Doğrulama ve Kabul Kriterleri (Acceptance Criteria)
Modelin yazdığı kodun tamamlanmış sayılması için aşağıdaki test suitlerini hatasız geçmesi zorunludur:
- [ ] Birim test kapsama oranı en az %90 olmalıdır.
- [ ] Property-based testing (örn. Hypothesis) ile 1.000 rastgele kombinasyonda değişmezler ihlal edilmemelidir.
- [ ] Statik tip denetleyicisi (`mypy --strict` veya `tsc --noEmit`) sıfır hata vermelidir.
- [ ] Hiçbir hassas anahtar (secret/API key) loglarda veya hata mesajlarında yer almamalıdır.
