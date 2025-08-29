# UzunMuhalefet Legal IPTV

Merhabalar,
FTA (Free-to-air veya ücretsiz uydu yayınları) ve internetten ücretsiz olarak izlenebilen içerikler için listeler oluşturup paylaşmaktayım. 

Atıfta bulunulması ve ticari bir eyleme dönüştürülmemesi şartlarıyla çalışmalarımı paylaşabilirsiniz.

**UYARILAR**

- Paylaşımlar içerisinde herhangi bir ücretli platforma ait içerikler veya direkt ücretli içerikler bulunmamaktadır.
- Proje içerisinde herhangi bir içeriğin yayını tarafımca yapılmamakta olup farklı kaynaklardan alınan içeriklere IPTV playerlarının destekleyeceği şekilde yönlendirme yapılmaktadır.

Merak edenler için alt kısımda yaptığım çalışmaların detayları mevcuttur.

**ADLANDIRMALAR**

Ülke bazlı içeriklerin klasör ve link yapısında sırasıyla aşağıdaki standartlar kullanılmaktadır.

- [ISO-3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- [UN/LOCODE Code List by Country and Territory](https://unece.org/trade/cefact/unlocode-code-list-country-and-territory)

Belirli bir kaynağa ait içeriklerde ise ilgili kaynağın website alan adı ve site içerisinde taranan kısmın bilgisi kullanılmaktadır.

## Yapılan Çalışmalar

Sistemin ayağa kaldırılması ve kurulumlar tarafındaki desteği için limonsikacagi61 'e teşekkürler.

<details>
  <summary>Detaylar</summary>

### Canlı Kanalların Yönetimi

- Ön-tanımsız (Headless) bir CMS (İYS) çözümü olan [Directus](https://directus.io/) sistemi ayağa kaldırılmıştır.
- Directus üzerinde gereken veri tipleri (Kanal, Yayın, Kategori vb.) oluşturulup. 450+ kanal için logo, yayın, kaynak vb. bilgiler girilmiştir. ![enter image description here](https://i.imgur.com/a2E1HAQ.png)
- Python ile geliştirilen sistem günlük olarak verileri [CMS API](https://docs.directus.io/reference/introduction.html) üzerinden çekip, yayınları denetleyip en yüksek öncelikli linke yönlendirme yapmaktadır.
- Yayınların denetiminde basit istek atılıp cevap kontrol edilmektedir. FFmpeg çözümleri denenmiş fakat işlem süresini çok arttırması sebebiyle basit istek şekline geri döndürülmüştür.

### YT, DM, Twitch Yayınlarının Sabit Linkleri
- Python [Streamlink](https://streamlink.github.io/) kütüphanesi kullanılarak Youtube, Dailymotion ve Twitch üzerinden yayın yapan kanallar için sabit link oluşturan bir sistem geliştirilmiştir.
- Sistem kendisine tanımlanan konfigürasyon dosyaları üzerinden [Github Actions](https://github.com/features/actions) kullanarak 2 saat aralıklar ile yayınları Multivariant (Master) ve Best (En Yüksek Kalite) listeleri güncellemektedir.

```
https://github.com/UzunMuhalefet/yayinlar
```

### YT, DM, Twitch Yayınlarının Dinamik Linkleri

- [Query Streamlink](https://github.com/BellezaEmporium/query-streamlink/tree/flask) reposu [Render](https://render.com/) platformu üzerinde ücretsiz hesap ile aktif edilmiştir.
- Streamlink desteği olan sitelere ait yayının bulunduğu linkler *url* sorgu parametresi ile geçilerek sonuç alınabilir. 
- NOT: IP adresi bazlı link koruması bulunan sitelerde çalışmaz. Youtube, Dailymotion, Twitch siteleri için çalışmaktadır fakat ülke bazlı kısıtlama bulunan içeriklerde çalışmayabilir.

```
https://tvcdn.onrender.com/iptv-query?url={ICERIK_ADRESI}&.m3u8
```

### Ticket (Secure Token) İçeren Sistemler

- Stabil clean (saf) linki bulunmayan platform ve yayınları listelere ekleyebilmek için PHP ve Regex kullanılarak son kullanıcı için link elde eden basit scriptler geliştirilmiş ve [serv00](https://www.serv00.com/) platformu üzerinde ücretsiz hesap ile çalıştırılmaktadır.

<details>
  <summary>Detaylar</summary>

#### Click2Stream (click2stream.com)

Pattern:
```
https://uzunmuhalefet.serv00.net/angelcam.php?id={SUBDOMAIN}&.m3u8
```

Örnek Yayın:
`https://abana-belediyesi.click2stream.com/`

Yayın URL:
`https://uzunmuhalefet.serv00.net/angelcam.php?id=abana-belediyesi&.m3u8`

#### IPCamLive (ipcamlive.com)

Pattern:
```
https://uzunmuhalefet.serv00.net/ipcamlive.php?id={ALIAS/ID}&.m3u8
```

Örnek Yayın:
`https://ipcamlive.com/player/player.php?alias=655b2fd67214e`

Yayın URL:
`https://uzunmuhalefet.serv00.net/ipcamlive.php?id=655b2fd67214e&.m3u8`

#### RTSP Me (rtsp.me)

Pattern:
```
https://uzunmuhalefet.serv00.net/rtspme.php?id={ID}&.m3u8
```

Örnek Yayın:
`https://rtsp.me/embed/QRHD7Y2Q/`

Yayın URL:
`https://uzunmuhalefet.serv00.net/rtspme.php?id=QRHD7Y2Q&.m3u8`

#### Earth TV (www.earthtv.com)

Pattern:
```
https://uzunmuhalefet.serv00.net/earthtv.php?id={NAME}&.m3u8
```

Örnek Yayın:
`https://www.earthtv.com/en/webcam/rotterdam-holland-amerikakade`

Yayın URL:
`https://uzunmuhalefet.serv00.net/earthtv.php?id=rotterdam-holland-amerikakade&.m3u8`

#### Bursa Büyükşehir Belediyesi (www.bursabuyuksehir.tv)

Pattern:
```
https://uzunmuhalefet.serv00.net/bursa.php?id={ID}&.m3u8
```

Örnek Yayın:
`https://www.bursabuyuksehir.tv/canli-yunus-emre-kavsagi-yeni-23542.html`

Yayın URL:
`https://uzunmuhalefet.serv00.net/bursa.php?id=23542&.m3u8`

#### Kocaeli Büyükşehir Belediyesi (kocaeliyiseyret.com)

Pattern:
```
https://uzunmuhalefet.serv00.net/kocaeli.php?id={ID}&.m3u8
```

Örnek Yayın:
`https://kocaeliyiseyret.com/Kamera/Index/cumhuriyet-bulvari2/2035`

Yayın URL:
`https://uzunmuhalefet.serv00.net/kocaeli.php?id=2035&.m3u8`

</details>

### EPG (Elektronik Program Rehberi)

IPTV Org ekibinin geliştirdiği [EPG](https://github.com/iptv-org/epg) yazılımı kurulup devreye alınmıştır.
Destekleyen playerlarda aşağıdaki URL eklenip kullanılabilir.

```
http://epg.tvcdn.net/guide/tr-guide.xml
```

</details>

## Listeler

### Canlı Yayınlar

#### 🇹🇷 Türkçe - Canlı Kanallar Listesi

M3U formatının standartlarının keskin olmaması sebebiyle 3 farklı çıktı üretilmektedir. Kullandığınız IPTV playerın formatına uyan halini seçebilirsiniz. Listelerin içeriği değişmemektedir.

**Standard Liste**

```
http://stream.tvcdn.net/lists/tr.m3u
```

**Alternatif Liste**

```
http://stream.tvcdn.net/lists/tr-alt.m3u
```

**SS-IPTV Listesi**

```
http://stream.tvcdn.net/lists/tr-ss.m3u
```

### Kameralar

<details>
  <summary>Detaylar</summary>


#### 🇹🇷 Türkiye - Canlı Kameralar Listesi

Türkiye ve KKTC'de bulunan aktif canlı yayın yapan kameraları içerir.

**Liste URL**
```
http://stream.tvcdn.net/lists/tr-cam.m3u
```

#### 🌎 Dünya - Havaalanları Kameraları Listesi
Dünya genelinden canlı yayın yapan havaalanlarına ait kameraları içerir.
Kameralar ülke bazlı gruplanmıştır, eğer var ise IATA kodları belirtilmiştir.
Kaynak: https://airportwebcams.net/

**Liste URL**
```
https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/categories/airports.m3u
```

#### 🇺🇸 Amerika - Trafik Kameraları
Amerika'da yer alan trafik kameralarını içermektedir.

<details>
  <summary>Listeler</summary>

| Eyalet | Liste URL |
|--|--|
| Alabama | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/al.m3u</code> |
| California | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ca.m3u</code> |
| Colorado | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/co.m3u</code> |
| Delaware | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/de.m3u</code> |
| Georgia | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ga.m3u</code> |
| Hawaii | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/hi.m3u</code> |
| Iowa | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ia.m3u</code> |
| Kansas | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ks.m3u</code>|
| Louisana | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/la.m3u</code> |
| Minnesota | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/mn.m3u</code> |
| Mississippi | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ms.m3u</code> |
| Nevada | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/nv.m3u</code>|
| New York | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ny.m3u</code> |
| Oklahoma | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ok.m3u</code> |
| Rhode Island | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/ri.m3u</code> |
| South Carolina | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/sc.m3u</code> |
| Tennessee | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/tn.m3u</code>|
| Virginia | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/va.m3u</code> |
| West Virginia | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/wv.m3u</code>|
| Wisconsin | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/cameras/countries/us/traffic/wi.m3u</code> |
</details>

</details>

### Video İçerikler

Türkçe yayın gösteren televizyon kanalları ve platformlardan kazınan içerikleri içermektedir. Yayın linkleri direkt olarak resmi yayıncıdan alınmıştır. Herhangi bir şekilde indirme veya tekrardan işleyip dağıtma söz konusu değildir.

- Her bir kaynakta belirli bir alt başlığa göre toplu liste(ler) bulunmaktadır.
- Haricen alt klasörler aracılığıyla tekil içeriklerin listelerine erişilebilmektedir.

<details>
<summary> Detaylar </summary>

| İçerik | Liste URL |
|--|--|
| TRT 1 - Arşiv | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-trt1-com-tr/arsiv.m3u</code>|
| TRT 1 - Programlar | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-trt1-com-tr/programlar.m3u</code>|
| Kanal D - Dizi Arşivi | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-kanald-com-tr/arsiv-diziler.m3u</code>|
| Kanal D - Program Arşivi | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-kanald-com-tr/arsiv-programlar.m3u</code>|
| Kanal D - Evde Sinema | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-kanald-com-tr/evde-sinema.m3u</code>|
| Show TV - Dizi Arşivi | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-showtv-com-tr/arsiv-diziler.m3u</code>|
| Show TV - Program Arşivi | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-showtv-com-tr/arsiv-programlar.m3u</code>|
| Now TV - Dizi Arşivi | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-nowtv-com-tr/dizi-arsivi.m3u</code>|
| Now TV - Program Arşivi | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-nowtv-com-tr/program-arsivi.m3u</code>|
| Now TV - Filmler | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-nowtv-com-tr/filmler.m3u</code>|
| Star TV - Arşiv | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-startv-com-tr/arsiv.m3u</code> |
| TV8 | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-tv8-com-tr/all.m3u</code>|
| Puhu TV - Filmler | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/puhutv-com/filmler.m3u</code> |
| teve2 - Diziler | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-teve2-com-tr/diziler.m3u</code>|
| teve2 - Programlar | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-teve2-com-tr/programlar.m3u</code>|
| DMAX | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-dmax-com-tr/all.m3u</code>|
| TLC | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-tlctv-com-tr/all.m3u</code>|
| TV 360 - Arşiv | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-tv360-com-tr/arsiv.m3u</code>|
| TV 360 - Programlar | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-tv360-com-tr/programlar.m3u</code>|
| TV 4 | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-tv4-com-tr/all.m3u</code>|
| CNN Türk - Belgeseller | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-cnnturk-com/belgeseller.m3u</code>|
| TRT Çocuk | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-trtcocuk-net-tr/all.m3u</code>
| Cartoon Network | <code>https://github.com/UzunMuhalefet/Legal-IPTV/raw/main/lists/video/sources/www-cartoonnetwork-com-tr/videolar.m3u</code>|

</details>


## Planlanan Çalışmalar

<details>
  <summary>Detaylar</summary>

### 🌎 Dünya Kameraları

Belirli konseptlere, ülke, bölge ve platform (websitesi) özelinde listeler çıkartmayı planlıyorum. Talep ettiğiniz bir konsept var ise belirtebilirsiniz.

**Planlanan Playlistler**

1. Türki Cumhuriyetler - TV Kanalları
2. Avrupa Ülkeleri - TV Kanalları
3. Dünya - Şehir Kameraları


### 🇹🇷 Türkiye - Video İçerikler

Bu sitelerin içeriklerine bir talep olduğu takdirde içeriklere ait liste çıkartma işlemi gerçekleştirilebilir.
| İçerik | Site URL|
|--|--|
| CNN Türk - Arşiv | https://www.cnnturk.com/tv-cnn-turk/arsiv/ |
| 24 TV - Programlar | https://www.yirmidort.tv/televizyon/tum-programlar |
| TVNET - Programlar | https://www.tvnet.com.tr/ |
| Power App - Videocast | https://www.powerapp.com.tr/videocast/ |
| Tarım TV | https://www.tarimtv.gov.tr/tr/ |
| Bloomberg HT - Programlar | https://www.bloomberght.com/video |
| Vav TV | https://vavtv.com.tr/ |

</details>
