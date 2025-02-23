import json
import os
import re, unicodedata

def slugify(deger: str, unicode_izin=False) -> str:
    """
    'unicode_izin' False ise ASCII'ye dönüştürür.
    Boşlukları veya tekrarlanan kısa çizgileri tek tirelere dönüştürür.
    Alfasayısal, alt çizgi veya kısa çizgi olmayan karakterleri kaldırıp küçük harfe dönüştürür.
    Ayrıca baştaki ve sondaki beyaz boşlukları, tireleri ve alt çizgileri de çıkarır.
    """
    if unicode_izin:
        deger = unicodedata.normalize("NFKC", deger)
    else:
        deger = unicodedata.normalize("NFKD", deger).encode("ascii", "ignore").decode("ascii")
    
    # Alfanümerik olmayan karakterleri kaldır (alt çizgi ve tire hariç)
    deger = re.sub(r"[^\w\s-]", "", deger.lower())

    # Boşlukları ve tireleri tek tireye dönüştür
    deger = re.sub(r"\s+", "-", deger.strip())

    return deger

current_dir = os.getcwd()

EXTINF = "#EXTINF"

def create_m3us(channel_folder_path, data, master=False, base_url=""):
    os.makedirs(channel_folder_path, exist_ok=True)
    existing_entries = set()
    master_file = None
    if master:
        master_file, existing_entries = handle_master_file(channel_folder_path, existing_entries)
    for serie in data:
        if len(serie["episodes"]) > 0:
            handle_series(channel_folder_path, serie, master, base_url, existing_entries, master_file)
    if master and master_file:
        master_file.close()

def handle_master_file(channel_folder_path, existing_entries):
    master_path = os.path.join(channel_folder_path, "0.m3u")
    if os.path.isfile(master_path):
        with open(master_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith(EXTINF):
                    existing_entries.add(line.strip())
    master_file = open(master_path, "a+", encoding="utf-8")
    if not existing_entries:
        master_file.write("#EXTM3U\n")
    return master_file, existing_entries

def handle_series(channel_folder_path, serie, master, base_url, existing_entries, master_file):
    plist_name = slugify(serie["name"].lower()) + ".m3u"
    plist_path = os.path.join(channel_folder_path, plist_name)
    plist_entries = set()
    if os.path.isfile(plist_path):
        with open(plist_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(EXTINF):
                    plist_entries.add(line.strip())
    with open(plist_path, "a+", encoding="utf-8") as plist_file:
        if not plist_entries:
            plist_file.write("#EXTM3U\n")
        for episode in serie["episodes"]:
            extinf_line = '#EXTINF:1 tvg-logo="' + episode["img"] + '",' + episode["name"]
            if extinf_line not in plist_entries:
                plist_file.write(extinf_line + "\n")
                plist_file.write(episode.get("stream_url", "") + "\n")
                plist_entries.add(extinf_line)
        if master:
            handle_master_entry(serie, base_url, plist_name, existing_entries, master_file)

def handle_master_entry(serie, base_url, plist_name, existing_entries, master_file):
    master_extinf_line = '#EXTINF:0 tvg-logo="'
    if "img" in serie:
        master_extinf_line += serie["img"] + '", '
    else:
        master_extinf_line += '", '
    master_extinf_line += serie["name"]
    if master_extinf_line not in existing_entries:
        master_file.write(master_extinf_line + "\n")
        master_file.write(base_url + plist_name + "\n")
        existing_entries.add(master_extinf_line)

def create_single_m3u(channel_folder_path, data, custom_path="0"):
    master_path = os.path.join(channel_folder_path, custom_path + ".m3u")
    os.makedirs(channel_folder_path, exist_ok=True)
    existing_entries = load_existing_entries(master_path)

    with open(master_path, "a+", encoding="utf-8") as master_file:
        for serie in data:
            for episode in serie["episodes"]:
                if "stream_url" in episode:
                    extinf_line = generate_extinf_line(episode, serie["name"])
                    entry_key = (extinf_line, episode["stream_url"])  # Duplicate kontrolü için
                    if entry_key not in existing_entries:
                        if(episode["stream_url"]):
                            master_file.write(extinf_line + "\n")
                            master_file.write(episode["stream_url"] + "\n")
                            existing_entries.add(entry_key)  # Yeni ekleneni kaydet

def load_existing_entries(master_path):
    existing_entries = set()
    if os.path.isfile(master_path):
        with open(master_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith("#EXTINF"):
                    extinf_line = lines[i].strip()
                    if i + 1 < len(lines) and lines[i + 1].startswith("http"):
                        stream_url = lines[i + 1].strip()
                        entry_key = (extinf_line, stream_url)
                        existing_entries.add(entry_key)
                        i += 2  # İki satır ilerle
                    else:
                        i += 1  # Sadece bir satır ilerle
                else:
                    i += 1  # Sadece bir satır ilerle
                if i < len(lines) and i + 1 < len(lines):
                    extinf_line = lines[i].strip()
                    stream_url = lines[i + 1].strip()
                    if extinf_line.startswith("#EXTINF") and stream_url.startswith("http"):
                        name_match = re.search(r',(.+)$', extinf_line)
                        if name_match:
                            name = name_match.group(1).strip()
                            entry_key = (name, stream_url)
                            existing_entries.add(entry_key)
    return existing_entries

def generate_extinf_line(episode, serie_name):
    return '#EXTINF:1 tvg-logo="' + episode["img"] + '" group-title="' + serie_name.replace('"', "'") + '",' + episode["name"]

def create_json(file_path, data, indent=4):
    existing_entries = load_existing_json_entries(file_path)

    # Yeni ve eşsiz verileri saklamak için bir sözlük
    unique_series = {}

    for serie in data:
        serie_name = serie["name"]
        new_episodes = []

        for episode in serie["episodes"]:
            if "stream_url" in episode:
                entry_key = (episode["name"], episode["stream_url"])
                if entry_key not in existing_entries:
                    new_episodes.append(episode)
                    existing_entries.add(entry_key)

        if new_episodes:
            if serie_name in unique_series:
                unique_series[serie_name]["episodes"].extend(new_episodes)
            else:
                unique_series[serie_name] = {"name": serie_name, "episodes": new_episodes}

    # Eğer yeni ekleme yoksa, dosyayı değiştirme
    if not unique_series:
        return  

    # Duplicate kontrolü ve unique hale getirme
    for serie in unique_series.values():
        serie["episodes"] = list({(ep["name"], ep["stream_url"]): ep for ep in serie["episodes"]}.values())

    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(list(unique_series.values()), f, ensure_ascii=False, indent=indent)


def load_existing_json_entries(file_path):
    existing_entries = set()
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
            try:
                existing_data = json.load(f)
                for serie in existing_data:
                    for episode in serie["episodes"]:
                        entry_key = (episode["name"], episode["stream_url"])
                        existing_entries.add(entry_key)
            except json.JSONDecodeError:
                pass
    return existing_entries

def get_new_episodes(serie, existing_entries):
    new_episodes = []
    for episode in serie["episodes"]:
        entry_key = (episode["name"], episode["stream_url"])
        if entry_key not in existing_entries:
            new_episodes.append(episode)
            existing_entries.add(entry_key)
    return new_episodes
