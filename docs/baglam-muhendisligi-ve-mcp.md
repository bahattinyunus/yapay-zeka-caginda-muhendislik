# Bağlam Mühendisliği ve Model Context Protocol (MCP)

> *"Bir modele tüm kütüphaneyi ezberletmek zeka değil; modele sadece o an ihtiyaç duyduğu kesin bilgiyi en az gürültüyle sunmak mühendisliktir."*

---

## 1. Bağlam Pencerelerinin Gerçek Maliyeti (The Needle-In-A-Haystack Problemi)

Modern modeller 1M+ veya 2M token bağlam pencereleri sunsa da, **bağlam boyutu arttıkça modelin muhakeme keskinliği ve dikkat (attention) doğruluğu logaritmik olarak düşer.**
- 20.000 satırlık bir kod tabanını doğrudan prompt penceresine yapıştırmak, modelin odak noktasını dağıtır.
- Model, gereksiz fonksiyon detaylarına takılarak asıl çözmesi gereken mimari değişmezi gözden kaçırır.

---

## 2. Just-In-Time (JIT) Bağlam Mimarisi

Bir orkestra şefi modele bağlamı şu katmanlarla sunar:

```
[Katman 0: Çekirdek Kısıtlar] ➔ Şartname, Sözleşmeler, Değişmezler (Her zaman bağlamda, ~1k token)
[Katman 1: Arayüz Tanımları]   ➔ Bağımlı servislerin sadece Type/Interface tanımları (~2k token)
[Katman 2: İhtiyaç Anında Çekim]➔ MCP (Model Context Protocol) araçları ile dinamik dosya okuma
```

---

## 3. Model Context Protocol (MCP) Standardı

Model Context Protocol (MCP); yapay zekâ modellerinin harici veri kaynaklarına, derleyicilere, veritabanlarına ve test hatlarına **standart bir JSON-RPC protokolü** üzerinden erişmesini sağlar.

### Neden MCP?
1. **İzolasyon:** Model rastgele işletim sistemi komutları çalıştırmaz; yalnızca tanımlı MCP tool'larını çağırır.
2. **Determinizm:** Model bir dosya okumak veya test çalıştırmak istediğinde, MCP sunucusu deterministik ve filtrelenmiş bir çıktı döner.
3. **Güvenlik:** API anahtarları veya veritabanı şifreleri asla modelin bağlamına sızmaz; MCP sunucusu arka planda yetkilendirmeyi yönetir.

📘 *Şablon sözleşme için:* [`templates/mcp-server-contract.json`](../templates/mcp-server-contract.json)
