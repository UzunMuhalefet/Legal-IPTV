import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    'X-Requested-With': 'XMLHttpRequest'
}

api_url = 'https://www.nowtv.com.tr/ajax/archive'
video_url = 'https://www.nowtv.com.tr/ajax/videos'
str_pattern = 'https://uzunmuhalefet.serv00.net/nowtv.php?serie=SERIE_SLUG&episode=EPISODE_NO&.m3u8'

def get_all_videos(id, serie_name=""):
    body = {
        'filter': 'season',
        'season': 1,
        'program_id': id,
        'page': 0,
        'type': 2,
        'count': 45,
        'orderBy': "id",
        "sorting": "asc"
    }
    video_list = []
    flag = True
    total = 0
    while flag:
        page_list = []
        r = requests.post(video_url, body, headers=headers)
        html = r.json()['data']
        data_count = r.json()["count"]
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", {"class": "list-item"})
        for item in items:
            name = serie_name+ " "  +  item.find("strong").get_text().strip()
            img = item.find("img").get("src")
            url = item.find("a").get("href")
            parts = url.split("/")
            temp_item = {
                "name": name,
                "img": img,
                "url": url,
                "stream_url": str_pattern.replace("SERIE_SLUG", parts[3]).replace("EPISODE_NO", parts[-1])
            }
            page_list.insert(0, temp_item)
        if len(items) == 0:
            flag = False
            break
        elif body["count"] >= data_count:
            body["season"] += 1
            total = 0
        elif data_count > total:
            body["page"] += 1
            total += len(items)
        if body['season'] > 1:
            video_list += page_list
        else:
            page_list = page_list + video_list
    return video_list

def get_all_items(content_type):
    body = {
        'page': 0,
        'type': content_type,
        'count': '50',
        'orderBy': 'id',
        "sorting": 'desc'
    }
    item_list = []
    flag = True
    while flag:
        r = requests.post(api_url, body, headers=headers)
        html = r.json()["data"]
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", {"class": "list-item"})
        if items:
            body['page'] += 1
            for item in items:
                name =  item.find("strong").get_text().strip()
                img = item.find("img").get("src")
                url = item.find("a").get("href")
                temp_item = {
                    "name": name,
                    "img": img,
                    "url": url
                }
                item_list.append(temp_item)
        else:
            flag = False
    return item_list

def main(content_type, name, start=0, end=0):
    data = []
    series_list = get_all_items(content_type)
    if end == 0:
        end_index = len(series_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        serie = series_list[i]
        print(i, serie["name"])
        serie_id = serie["img"].split("/")[-1]
        episodes = get_all_videos(serie_id, serie["name"])
        temp_serie = serie.copy()
        temp_serie["episodes"] = episodes
        data.append(temp_serie)
    
    f = open("www-nowtv-com-tr-" + name + ".json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/video/sources/www-nowtv-com-tr", data, name)
    create_m3us("../../lists/video/sources/www-nowtv-com-tr/" + name, data)


if __name__=="__main__": 
    main("series", "dizi-arsivi")
    main("programs", "program-arsivi") 
