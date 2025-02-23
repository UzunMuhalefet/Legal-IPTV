import os
import re, unicodedata

def slugify(deger:str, unicode_izin=False) -> str:
    """
    'unicode_izin' False ise ASCII'ye dönüştürür.
    Boşlukları veya tekrarlanan kısa çizgileri tek tirelere dönüştürür.
    Alfasayısal, alt çizgi veya kısa çizgi olmayan karakterleri kaldırıp Küçük harfe dönüştür.
    Ayrıca baştaki ve sondaki beyaz boşlukları, tireleri ve alt çizgileri de çıkarır.
    """
    if unicode_izin:
        deger = unicodedata.normalize("NFKC", deger)
    else:
        deger = unicodedata.normalize("NFKD", deger).encode("ascii", "ignore").decode("ascii")
    deger = re.sub(r"[^\w\s-]", "", deger.lower())
    return re.sub(r"[-\s]+", "-", deger).strip("-_")

current_dir = os.getcwd()

def create_m3us(channel_folder_path, data, master=False, base_url=""):
    #channel_folder_name = slugify(channel_name.lower())
    #channel_folder_path = os.path.join(current_dir, channel_folder_name)
    os.makedirs(channel_folder_path, exist_ok=True)
    if master:
        master_path = os.path.join(channel_folder_path, "0.m3u")
        master_file = open(master_path, "a+")
        master_file.write("#EXTM3U\n")
    for serie in data:    
        if len(serie["episodes"]) > 0:
            plist_name = slugify(serie["name"].lower()) + ".m3u"
            plist_path = os.path.join(channel_folder_path, plist_name)
            if master:
                master_file.write('#EXTINF:0 tvg-logo="')
                if "img" in serie:
                    master_file.write(serie["img"] + '", ')
                else:
                    master_file.write('", ')
                master_file.write(serie["name"] + "\n")
                master_file.write(base_url + plist_name + "\n")
            plist_file = open(plist_path, "w+")
            plist_file.write("#EXTM3U\n")
            for episode in serie["episodes"]:
                plist_file.write('#EXTINF:1 tvg-logo="' + episode["img"] + '",' + episode["name"] + "\n")
                plist_file.write(episode["stream_url"] + "\n")
            plist_file.close()

def create_single_m3u(channel_folder_path, data, custom_path="0"):
    #channel_folder_name = slugify(channel_name.lower())
    #channel_folder_path = os.path.join(current_dir, channel_folder_name)
    master_path = os.path.join(channel_folder_path, custom_path + ".m3u")
    os.makedirs(channel_folder_path, exist_ok=True)
    flag = 0
    if not os.path.isfile(master_path):
        flag = 1
    master_file = open(master_path, "a+") 
    if flag:
        master_file.write("#EXTM3U\n")
    for serie in data:  
        for episode in serie["episodes"]:
            master_file.write('#EXTINF:1 tvg-logo="' + episode["img"] + '" group-title="' + serie["name"].replace('"', "'") + '",' + episode["name"] + "\n")
            master_file.write(episode["stream_url"] + "\n")
    master_file.close()