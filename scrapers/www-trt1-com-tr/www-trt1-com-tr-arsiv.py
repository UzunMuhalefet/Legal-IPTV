import re, requests, json
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
import json
import time

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

mp4_pattern = r'src: \'(.*?)\''
img_pattern = r'poster: \'(.*?)\''
title_pattern = r'<h1>(.*?)</h1>'

img_base_url = "https://www.trt1.com.tr/"
base_url = "https://www.trt1.com.tr"

def url_fixer(url):
    if url[:2] == "//":
        return "https:" + url
    elif url[:1] == "/":
        return base_url + url
    else:
        return url

def find_src(text, pattern):
    matches = re.findall(pattern, text)
    return matches

def parse_episode_page(episode_url):
    r = requests.get(episode_url)
    streams = find_src(r.text, mp4_pattern)
    episode = {
        "name": find_src(r.text, title_pattern)[0].strip(),
        "url": episode_url,
        "stream_url": "",
        "img": ""
    }
    if len(streams) > 0:
        episode["stream_url"] = url_fixer(streams[0])
        episode["img"] = img_base_url + find_src(r.text, img_pattern)[0]

    return episode

def get_all_episodes(last_episode_url):
    all_items = []
    last_episode = parse_episode_page(last_episode_url)
    if last_episode["stream_url"]:
        all_items.append(last_episode)
    
    r = requests.get(last_episode_url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    items = soup.find("ul", {"class": "paging"}).find_all("li")
    for i in tqdm(range(0, len(items))):
        item = items[i]
        if i % 15 == 0:
            time.sleep(5)
        url = img_base_url + item.find("a").get("href")
        episode = parse_episode_page(url)
        if episode["stream_url"]:
            all_items.insert(0, episode)
    
    return all_items

def get_last_episode(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    bolumler_section = soup.find(attrs={"id": "bolumler"})
    if bolumler_section:
        bolumler = bolumler_section.find_all("li")
        if len(bolumler) != 0:
            son_bolum_url = bolumler[0].find("a").get("href")
            return img_base_url + son_bolum_url
    return ""

def get_all_items(url):
    all_items = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    diziler = soup.find("ul", {"class": "paging"}).find_all("li")
    for dizi in diziler:
        dizi_url = dizi.find("a").get("href")
        dizi_url = base_url + dizi_url
        dizi_adi = dizi.find("div", {"class": "category-title"}).get_text().strip()
        dizi_img = img_base_url + dizi.find("img").get("src")
        temp_dizi = {
            "name": dizi_adi,
            "url": dizi_url,
            "img": dizi_img
        }
        all_items.append(temp_dizi)

    return all_items

def main(url, name, start=0, end=0):
    data = []
    series_list = get_all_items(url)
    if end == 0:
        end_index = len(series_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        serie = series_list[i]
        print(i, serie["name"])
        last_episode_url = get_last_episode(serie["url"])
        if last_episode_url:
            temp_serie = serie.copy()
            temp_serie["episodes"] = get_all_episodes(last_episode_url)
            if len(temp_serie["episodes"]) > 0:
                data.append(temp_serie)
    f = open("www-trt1-com-tr-" + name + ".json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/video/sources/www-trt1-com-tr", data, name)
    create_m3us("../../lists/video/sources/www-trt1-com-tr/" + name, data)
        

archive_url = "https://www.trt1.com.tr/tv/arsiv"

if __name__=="__main__": 
    main(archive_url, "arsiv")
    main("https://www.trt1.com.tr/tv/programlar", "programlar")