import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys
import re

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

pattern = r'"apiUrl\\":\\"(.*?)\\"'
base_url = "https://www.startv.com.tr"
img_base_url = "https://media.startv.com.tr/star-tv"

dizi_url = "https://www.startv.com.tr/dizi"

api_params = {
    "sort": "episodeNo asc",
    "limit": "100"
}

def get_items_page(url):
    item_list = []
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    items = soup.find_all("div", {"class": "poster-card"})
    
    for item in items:
        item_name = item.find("div", {"class":"text-left"}).get_text().strip()
        item_img = item.find("img").get("src")
        item_url = base_url + item.find("a").get("href")
        temp_item = {
            "name": item_name, 
            "img": item_img,
            "url": item_url
        }
        item_list.append(temp_item)
    return item_list

def get_item_api_url(url):
    api_path = ""
    url = url + "/bolumler"
    r = requests.get(url)
    results = re.findall(pattern, r.text)
    if results:
        api_path = results[0]
    return api_path

def get_item_api(path):
    item_list = []
    params = api_params
    flag = True
    url = base_url + path
    skip = 0
    while flag:
        params["skip"] = skip
        try:
            r = requests.get(url, params=params)
            data = r.json()
            items = data["items"]
            for item in items:
                name = item["heading"] + " - " + item["title"]
                if item["image"]:
                    img = img_base_url + item["image"]["fullPath"]
                else:
                    img = ""
                if "video" in item:
                    stream_url = "https://dygvideo.dygdigital.com/api/redirect?PublisherId=1&ReferenceId=StarTV_{}&SecretKey=NtvApiSecret2014*&.m3u8".format(item["video"]["referenceId"])
                else:
                    stream_url = ""
                temp_item = {
                    "name": name,
                    "img": img,
                    "stream_url": stream_url
                }
                if temp_item["stream_url"]:
                    item_list.append(temp_item)
            if len(items) < 100:
                flag = False
            else:
                skip += 100
        except:
            flag = False
    return item_list

def main(start=0, end=0):
    data = []
    series_list = get_items_page(dizi_url)
    if end == 0:
        end_index = len(series_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        serie = series_list[i]
        print(i, serie["name"])
        api_path = get_item_api_url(serie["url"])
        episodes = get_item_api(api_path)
        temp_serie = serie.copy()
        temp_serie["episodes"] = episodes
        data.append(temp_serie)
    f = open("www-startv-com-tr-arsiv.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/video/sources/www-startv-com-tr", data, "arsiv")
    create_m3us("../../lists/video/sources/www-startv-com-tr/arsiv", data)

if __name__=="__main__": 
    main()