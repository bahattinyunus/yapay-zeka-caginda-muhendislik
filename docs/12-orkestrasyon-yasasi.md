# 12 Orkestrasyon Yasası: Yapay Zekâ Çağında Yazılım Mühendisliği Amentüsü

Bu doküman, yapay zekânın kod üretimini devraldığı çağda yazılım mühendislerinin sistem inşa ederken uymak zorunda olduğu 12 sarsılmaz ilkeyi açıklar.

---

### 1. Yasa: Şartname Önceliği İlkesi (The Principle of Specification Primacy)
*Tasarımı, arayüz sözleşmeleri ve tip modelleri önceden kesin olarak tanımlanmamış hiçbir görev için modele tek satır kod ürettirilemez.*  
Eğer ne istediğinizi matematiksel veya yapısal olarak tarif edemiyorsanız, modelin üreteceği şey sadece rastgele istatistiksel bir gürültüdür.

### 2. Yasa: Doğrulama Bağımsızlığı İlkesi (The Independence of Verification)
*Kodu üreten akıl ile kodu denetleyen mekanizma asla aynı olamaz.*  
Yapay zekâ olasılıksal (stokastik) çalışır; mühendislik ise kesinlik (determinizm) talep eder. Modelin kendi kodunu gözle onaylamasına güvenilemez. Kod, modelden bağımsız deterministik test hatlarından (CI/CD, compiler, linter, property-based tests) geçmek zorundadır.

### 3. Yasa: Gözle Tarama Yasağı (The Anti-Vibe Rule)
*Modelin ürettiği yüzlerce satır kodu gözle satır satır okuyup hata aramak mühendislik değil, dijital ameleliktir.*  
Denetim insan gözüyle değil; sınır değerleri zorlayan otomatik testlerle, tiplerle ve linter kurallarıyla yapılır.

### 4. Yasa: Kalıcı Olan Sistemdir İlkesi (The Permanence of Architecture)
*Kod geçicidir; veri yapıları, şemalar, ilişkiler ve arayüz sözleşmeleri kalıcıdır.*  
Gelecek modeller bugünkü kodları saniyeler içinde baştan yazacaktır. Mühendisin zihinsel enerjisi kodun sentaksına değil, sistemin mimari kurgusuna ve veri modellerine vakfedilmelidir.

### 5. Yasa: Bilişsel İş Bölümü İlkesi (Agentic Topology)
*Karmaşık bir problemi tek bir süper-prompt oturumuna yıkmak mimari cehalettir.*  
Sistem; Mimar (Planner), Kodlayıcı (Worker), Eleştirmen (Red Team) ve Sentezci (Integrator) gibi sınırları ayrılmış ajan topolojilerine bölünmelidir.

### 6. Yasa: Kendi Kendini İyileştiren Döngü İlkesi (Self-Healing Feedback Loops)
*Model hata yaptığında insan araya girip klavyeyle kodu elle yamamaz.*  
Hata terminal çıktısı, stack trace veya test başarısızlığı olarak yakalanır; bu deterministik bağlam modele geri beslenir ve model hatasını kendi kendine düzeltir.

### 7. Yasa: Temiz Bağlam İlkesi (Context Hygiene)
*Modelin bağlam penceresini (context window) gereksiz kod tabanıyla doldurmak bilişsel felç yaratır.*  
Modele sadece ve sadece o an üzerinde çalıştığı sınırın doğrudan bağımlılıkları (Just-In-Time Context) verilmelidir.

### 8. Yasa: Fiziksel Gerçekliğin Üstünlüğü (The Primacy of Physics)
*Hiçbir yapay zekâ modeli donanımın, ağın ve dağıtık sistemlerin fizik kurallarını ihlal edemez.*  
Ağ gecikmesi, disk I/O darboğazları, concurrency kilitleri ve CAP teoremi modellerin halüsinasyonlarından daima üstündür. Mühendis bu fizik kanunlarını bilen kişidir.

### 9. Yasa: Determinizm İlkesi (The Deterministic Preference)
*Deterministik bir kütüphanenin, algoritmanın veya derleyicinin çözebileceği bir iş asla olasılıksal bir yapay zekâ modeline bırakılamaz.*  
Matematiksel kesinlik varken tahmin yürütülmez.

### 10. Yasa: Halüsinasyona Karşı Sıfır Güven (Zero-Trust Dependencies)
*Modelin önerdiği her yeni kütüphane, harici bağımlılık veya API çağrısı aksi kanıtlanana kadar şüpheli kabul edilir.*  
Paket halüsinasyonlarına ve zehirli açık kaynak tedarik zinciri saldırılarına karşı otomatik güvenlik bariyerleri şarttır.

### 11. Yasa: Mimari Zevk ve Sadelik (Architectural Taste)
*Yapay zekâ internetteki vasat kodların ortalamasını üretir; zarafet ve sadelik ise ancak insan iradesiyle dayatılabilir.*  
Sistemi gereksiz karmaşıklıktan arındırmak ve zarif sınırlarla donatmak orkestra şefinin zanaatıdır.

### 12. Yasa: İrade Mühendistedir (The Human in the Command)
*Yapay zekâ bir güç çarpanı ve üretim motorudur; fakat neyin inşa edileceğine, hangi risklerin alınacağına ve kalitenin nerede başlayıp bittiğine karar veren yegâne irade insandır.*
