# UzunMuhalefet Legal IPTV

Merhabalar,
FTA (Free-to-air veya ücretsiz uydu yayınları) ve internetten ücretsiz olarak izlenebilen içerikler için listeler oluşturup paylaşmaktayım. 

Atıfta bulunulması ve ticari bir eyleme dönüştürülmemesi şartlarıyla çalışmalarımı paylaşabilirsiniz.

**UYARILAR**
 - Paylaşımlar içerisinde herhangi bir ücretli platforma ait içerikler veya direkt ücretli içerikler bulunmamaktadır.
 - Proje içerisinde herhangi bir içeriğin yayını tarafımca yapılmamakta olup farklı kaynaklardan alınan içeriklere IPTV playerlarının destekleyeceği şekilde yönlendirme yapılmaktadır.

Merak edenler için en alt kısımda yaptığım çalışmaların detayları mevcuttur.

# Yapılan Çalışmalar

Sistemin ayağa kaldırılması ve kurumlar tarafındaki desteği için limonsikacagi61 'e teşekkürler.
<details>
  <summary>Detaylar</summary>

## Canlı Kanalların Yönetimi

 - Ön-tanımsız (Headless) bir CMS (İYS) çözümü olan [Directus](https://directus.io/) sistemi ayağa kaldırılmıştır. 
 - Directus üzerinde gereken veri tipleri (Kanal, Yayın, Kategori vb.) oluşturulup. 450+ kanal için logo, yayın, kaynak vb. bilgiler girilmiştir. ![enter image description here](https://i.imgur.com/a2E1HAQ.png)
- Python ile geliştirilen sistem günlük olarak verileri [CMS API](https://docs.directus.io/reference/introduction.html) üzerinden çekip, yayınları denetleyip en yüksek öncelikli linke yönlendirme yapmaktadır.
- Yayınların denetiminde basit istek atılıp cevap kontrol edilmektedir. FFmpeg çözümleri denenmiş fakat işlem süresini çok arttırması sebebiyle basit istek şekline geri döndürülmüştür.

## YT, DM, Twitch Yayınlarının Sabit Linkleri
- Python [Streamlink](https://streamlink.github.io/) kütüphanesi kullanılarak Youtube, Dailymotion ve Twitch üzerinden yayın yapan kanallar için sabit link oluşturan bir sistem geliştirilmiştir.
- Sistem kendisine tanımlanan konfigürasyon dosyaları üzerinden [Github Actions](https://github.com/features/actions) kullanarak 2 saat aralıklar ile yayınları Multivariant (Master) ve Best (En Yüksek Kalite) listeleri güncellemektedir.

`https://github.com/UzunMuhalefet/yayinlar`

## YT, DM, Twitch Yayınlarının Dinamik Linkleri
- [Query Streamlink](https://github.com/BellezaEmporium/query-streamlink/tree/flask) reposu [Render](https://render.com/) platformu üzerinde ücretsiz hesap ile aktif edilmiştir.
- Streamlink desteği olan sitelere ait yayının bulunduğu linkler *url* sorgu parametresi ile geçilerek sonuç alınabilir. 
- NOT: IP adresi bazlı link koruması bulunan sitelerde çalışmaz. Youtube, Dailymotion, Twitch siteleri için çalışmaktadır fakat ülke bazlı kısıtlama bulunan içeriklerde çalışmayabilir.

`https://tvcdn.onrender.com/iptv-query?url={ICERIK_ADRESI}&.m3u8`

## Ticket (Secure Token) İçeren Sistemler
- Stabil clean (saf) linki bulunmayan platform ve yayınları listelere ekleyebilmek için PHP ve Regex kullanılarak son kullanıcı için link elde eden basit scriptler geliştirilmiş ve [serv00](https://www.serv00.com/) platformu üzerinde ücretsiz hesap ile çalıştırılmaktadır.

### Click2Stream (click2stream.com)
Pattern:
`https://uzunmuhalefet.serv00.net/angelcam.php?id={SUBDOMAIN}&.m3u8`

Örnek Yayın:
`https://abana-belediyesi.click2stream.com/`

Yayın URL:
`https://uzunmuhalefet.serv00.net/angelcam.php?id=abana-belediyesi&.m3u8`

### IPCamLive (ipcamlive.com)
Pattern:
`https://uzunmuhalefet.serv00.net/ipcamlive.php?id={ALIAS/ID}&.m3u8`

Örnek Yayın:
`https://ipcamlive.com/player/player.php?alias=655b2fd67214e`

Yayın URL:
`https://uzunmuhalefet.serv00.net/ipcamlive.php?id=655b2fd67214e&.m3u8`

### RTSP Me (rtsp.me)
Pattern:
`https://uzunmuhalefet.serv00.net/rtspme.php?id={ID}&.m3u8`

Örnek Yayın:
`https://rtsp.me/embed/QRHD7Y2Q/`

Yayın URL:
`https://uzunmuhalefet.serv00.net/rtspme.php?id=QRHD7Y2Q&.m3u8`

### Bursa Büyükşehir Belediyesi
Pattern:
`https://uzunmuhalefet.serv00.net/bursa.php?id={ID}&.m3u8`

Örnek Yayın:
`https://www.bursabuyuksehir.tv/canli-yunus-emre-kavsagi-yeni-23542.html`

Yayın URL:
`https://uzunmuhalefet.serv00.net/bursa.php?id=23542&.m3u8`

### Kocaeli Büyükşehir Belediyesi
Pattern:
`https://uzunmuhalefet.serv00.net/kocaeli.php?id={ID}&.m3u8`

Örnek Yayın:
`https://kocaeliyiseyret.com/Kamera/Index/cumhuriyet-bulvari2/2035`

Yayın URL:
`https://uzunmuhalefet.serv00.net/kocaeli.php?id=2035&.m3u8`

## EPG (Elektronik Program Rehberi)
IPTV Org ekibinin geliştirdiği [EPG](https://github.com/iptv-org/epg) yazılımı kurulup devreye alınmıştır.
Destekleyen playerlarda aşağıdaki URL eklenip kullanılabilir.

`http://epg.tvcdn.net/guide/tr-guide.xml`

</details>

# Listeler

## 🇹🇷 Türkçe - Canlı Kanallar Listesi
M3U formatının standartlarının keskin olmaması sebebiyle 3 farklı çıktı üretilmektedir. Kullandığınız IPTV playerın formatına uyan halini seçebilirsiniz. Listelerin içeriği değişmemektedir.

 **Standard Liste**
`http://stream.tvcdn.net/lists/tr.m3u`

**Alternatif Liste**
`http://stream.tvcdn.net/lists/tr-alt.m3u`

**SS-IPTV Listesi**
`http://stream.tvcdn.net/lists/tr-ss.m3u`

## 🇹🇷 Türkiye - Canlı Kameralar Listesi

Türkiye ve KKTC'de bulunan aktif canlı yayın yapan kameraları içerir.

**Liste URL**
`http://stream.tvcdn.net/lists/tr-cam.m3u`

# Planlanan Çalışmalar
<details>
  <summary>Detaylar</summary>

## 🇹🇷 Türkçe - TV İçerikleri 
Türkiye'de faaliyet gösteren TV kanallarına ait içeriklerin kanalların sitelerindeki yayın adresleri (mp4 ve m3u8 uzantılı) kullanılarak servis edilmesi.
Python ile BeautifulSoup ve Regex kullanılarak içerikler çıkarılmaktadır.

**Planlanan Siteler**
| Kanal Adı | Site URL |
|--|--|
| TRT 1 - Arşiv | https://www.trt1.com.tr/tv/arsiv  |
| Kanal D - Dizi Arşivi | https://www.kanald.com.tr/diziler/arsiv  |
| Kanal D - Program Arşivi | https://www.kanald.com.tr/programlar/arsiv  |
| teve2 - Dizi Arşivi | https://www.teve2.com.tr/diziler/arsiv  |
| teve2 - Program Arşivi | https://www.teve2.com.tr/programlar/arsiv  |
| Show TV - Dizi Arşivi | https://www.showtv.com.tr/diziler/arsivdeki-diziler  |
| Show TV - Program Arşivi | https://www.showtv.com.tr/programlar/arsivdeki-programlar  |
| TV 8 - Programlar | https://www.tv8.com.tr/programlar  |
| TRT Çocuk - Videolar | https://www.trtcocuk.net.tr/video  |
| 360 TV - Programlar | https://www.tv360.com.tr/yasam-programlar  |
| TV 4 - Programlar | https://www.tv4.com.tr/yasam-programlar  |
| CNN Türk - Belgeseller | https://www.tv4.com.tr/yasam-programlar  |

## 🌎 Dünya Kameraları

Belirli konseptlere, ülke, bölge ve platform (websitesi) özelinde listeler çıkartmayı planlıyorum. Talep ettiğiniz bir konsept var ise belirtebilirsiniz.

**Planlanan Playlistler**
1. Havaalanı kameraları

</details>
