import re, requests, json
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
import json

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

base_url = "https://www.trtcocuk.net.tr"

def parse_episodes(path, limit, offset):
    all_items = []
    params = {
        "path": path,
        "limit": limit,
        "offset": offset
    }
    url = "https://www.trtcocuk.net.tr/api/detail"
    r = requests.get(url, params=params)
    data = r.json()
    episodes = data["videos"]
    for episode in episodes:
        item_name = episode["title"]
        item_img = episode["mainImageUrl"]
        item_url = base_url + episode["path"]
        stream_url = episode["video"]
        temp_episode = {
            "name": item_name,
            "img": item_img,
            "url": item_url,
            "stream_url": stream_url
        }
        all_items.insert(0, temp_episode)
    return all_items

def get_episodes(url):
    path = url.replace(base_url, "")
    all_items = []
    flag = True
    offset = 0
    limit = 100
    while flag:
        page_items = parse_episodes(path, limit, offset)
        all_items = page_items + all_items
        if len(page_items) < limit:
            flag = False
        else:
            offset = offset + 100
    return all_items

def get_all_items():
    item_list = []
    url = "https://www.trtcocuk.net.tr/api/list?type=show&limit=100&offset=0"
    r = requests.get(url)
    data = r.json()
    items = data["list"]
    for item in items:
        item_url = base_url + item["path"]
        item_img = item["logo"]
        item_name = item["title"]
        temp_item = {
            "name": item_name,
            "img": item_img,
            "url": item_url
        }
        item_list.append(temp_item)
    return item_list

def main(start=0, end=0):
    data = []
    item_list = get_all_items()
    if end == 0:
        end_index = len(item_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        item = item_list[i]
        print(i, item["name"])
        temp_item = item.copy()
        episodes = get_episodes(item["url"])
        temp_item["episodes"] = episodes
        data.append(temp_item)
    
    create_single_m3u("../../lists/video/sources/www-trtcocuk-net-tr", data, "all")
    f = open("www-trtcocuk-net-tr-video.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-trtcocuk-net-tr/video", data)

main()