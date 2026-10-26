# Vaka Çalışması: Finansal Ödeme Ağ Geçidi İnşası

Bu belgede; aynı iş gereksiniminin **Geleneksel Prompt Hamallığı (Çıraklık)** yaklaşımı ile **Orkestra Şefliği (Sistem Mimarisi)** yaklaşımı arasındaki somut farkı incelenmektedir.

---

## Görev
Bir e-ticaret platformu için Stripe üzerinden ödeme alan, sipariş durumunu güncelleyen ve webhook bildirimlerini işleyen bir mikroservis geliştirmek.

---

## 1. Yol: AI Çırağı Yaklaşımı (Vibe Coding)

### Adım 1: Prompt Gönderimi
> *"Bana Node.js ve Express ile Stripe ödemesi alan ve webhook dinleyen bir endpoint yaz."*

### Adım 2: Model Çıktısı
Model 70-80 satırlık, ilk bakışta çalışan bir Express kodu verir:
```javascript
app.post('/pay', async (req, res) => {
  const { amount, token } = req.body;
  const charge = await stripe.charges.create({
    amount,
    currency: 'usd',
    source: token,
  });
  await db.orders.update({ status: 'PAID' });
  res.json({ success: true });
});
```

### Adım 3: Ortaya Çıkan Felaketler
1. **Çift Çekim Riski:** Kullanıcı butona iki kez basarsa idempotency anahtarı olmadığı için iki defa para tahsil edilir.
2. **Kısmi Başarısızlık:** `stripe.charges.create` başarılı olup hemen ardından `db.orders.update` veritabanı hatasıyla patlarsa para çekilir ama sipariş ödenmedi görünür.
3. **Webhook Sahtekarlığı:** Webhook endpoint'inde Stripe imza doğrulaması (`stripe-signature`) olmadığı için saldırganlar sahte webhook yollayarak siparişleri bedavaya getirebilir.
4. **Zaman Kaybı:** Geliştirici durumu fark ettikçe:
   - *"Hata veriyor şurayı düzelt"*
   - *"Idempotency ekle"*
   - *"Webhook bozuldu şimdi ne yapayım"*  
   diyerek modelle 4 saat ping-pong oynar.

---

## 2. Yol: Orkestra Şefi Yaklaşımı (Sistem Mimarı)

Orkestra şefi modele serbest kod yazdırmaz. Önce sistemi ve sınırları modeller:

### Adım 1: Spesifikasyon ve Değişmezlerin Çizilmesi
```yaml
Modül: PaymentGateway
Invariants:
  - Idempotency-Key zorunlu (UUIDv4)
  - Tutar pozitif tamsayı (cents)
  - Distributed Lock: Aynı sipariş için eşzamanlı işlem engeli
  - Outbox Pattern veya İki Aşamalı İşlem: Stripe başarılı ise DB kaydı garanti
  - Webhook: HMAC SHA256 imza denetimi + timestamp replay koruması
```

### Adım 2: Deterministik Doğrulama Seti (Evals)
Geliştirici önce test senaryolarını ve property testlerini tanımlar:
- `test_double_charge_prevented_with_same_idempotency_key()`
- `test_network_timeout_triggers_proper_reversal()`
- `test_invalid_webhook_signature_returns_400()`
- `test_concurrent_payment_requests_execute_atomically()`

### Adım 3: Ajan Hattının Çalıştırılması
1. **Kodlayıcı Ajan:** Spesifikasyonu ve interface sözleşmesini alır, kodu yazar.
2. **Korkuluk Hattı:** Testleri çalıştırır. Eğer concurrency testinde race condition yakalarsa stack trace'i ajana geri besler.
3. **Ajan:** Geri beslemeyi kullanarak kodu günceller ve testleri yeşile döndürür.
4. **Mimar (İnsan):** Sadece sözleşmenin doğruluğunu ve test kapsamını onaylar.

### Sonuç
- **Harcanan Süre:** 20 dakika sistem tasarımı, 3 dakika ajan derlemesi.
- **Teknik Borç:** Sıfır.
- **Üretime Güven:** %100 deterministik.
