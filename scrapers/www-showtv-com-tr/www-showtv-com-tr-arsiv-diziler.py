import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys
import re

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

site_url = "https://www.showtv.com.tr"
dizi_arsiv = "https://www.showtv.com.tr/diziler/arsivdeki-diziler"

def parse_bolum_page(url):
    try:
        r = requests.get(url)
        match = re.search(r'data-hope-video=\'(.*?)\'', r.text)
        if match:
            video_data = json.loads(match.group(1).replace('&quot;', '"'))
            m3u8_list = video_data.get("media", {}).get("m3u8", [])
            for item in m3u8_list:
                if "src" in item and item["src"].endswith(".m3u8"):
                    return item["src"]
    except Exception as e:
        print(url, str(e))

    return None

def parse_episodes_page(url):
    item_list = []
    r = requests.get(url)
    data = r.json()["episodes"]
    for item in data:
        item_name = item["title"]
        item_img = item["image"]
        item_url = site_url + item["link"]
        temp_item = {
            "name": item_name,
            "img": item_img,
            "url": item_url
        }
        item_list.insert(0, temp_item)
    return item_list


def get_episodes_page(serie_url):
    all_items = []
    base_url = "https://www.showtv.com.tr/dizi/pagination/SERIE_ID/2/"
    serie_id = serie_url.split("/")[-1]
    url = base_url.replace("SERIE_ID", serie_id)
    flag = True
    page_no = 0
    while flag:
        page_url = url + str(page_no)
        page_items = parse_episodes_page(page_url)
        if len(page_items) == 0:
            flag = False
        else:
            all_items = page_items + all_items
        page_no = page_no + 1
    return all_items


def get_arsiv_page(url):
    item_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    items = soup.find_all("div", {"data-name": "box-type6"})
    for item in items:
        item_url = site_url + item.find("a").get("href")
        item_img = item.find("img").get("src")
        item_name = item.find("span", {"class": "line-clamp-3"}).get_text().strip()
        item_id = item_url.split("/")[-1]
        temp_item = {
            "name": item_name,
            "img": item_img,
            "url": item_url,
            "id": item_id
        }
        item_list.append(temp_item)
    return item_list


def main(start=0, end=0):
    data = []
    series_list = get_arsiv_page(dizi_arsiv)
    if end == 0:
        end_index = len(series_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        serie = series_list[i]
        print(i, serie["name"])
        episodes = get_episodes_page(serie["url"])
        if episodes:
            temp_serie = serie.copy()
            temp_serie["episodes"] = []
            for j in tqdm(range(0, len(episodes))):
                episode = episodes[j]
                stream_url = parse_bolum_page(episode["url"])
                episode["stream_url"] = stream_url
                if stream_url:
                    temp_serie["episodes"].append(episode)
            data.append(temp_serie)
    create_single_m3u("showtv", data)
    create_single_m3u("../../lists/video/sources/www-showtv-com-tr", data, "arsiv-diziler")
    f = open("www-showtv-com-tr-arsiv-diziler.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-showtv-com-tr/video", data)

main(0,0)
