import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

base_url = "https://www.tv8.com.tr"
img_base_url = "https://img.tv8.com.tr/"
api_base_url = "https://www.tv8.com.tr/Ajax/icerik/haberler/ITEM_NO/PAGE_NO?tip=videolar&sayfa=1&tip=videolar"

videos_path = "/videolar"

def parse_episodes(url):
    item_list = []
    r = requests.get(url)
    if r.text != "false":
        data = json.loads(r.text)
        for item in data:
            images = json.loads(item["resim"])
            item_img = ""
            for key in images:
                item_img = img_base_url + images[key]
                break
            item_name = item["baslik"].strip()
            if len(item["tip_deger"].split(",")) == 1:
                item_url = item["tip_deger"].replace(".mp4", ".smil/playlist.m3u8")
                temp_item = {
                    "name": item_name,
                    "img": item_img,
                    "stream_url": item_url
                }
                item_list.insert(0,temp_item)
    return item_list

def get_episodes(content_episodes_id):
    all_items = []
    page_no = 1
    flag = True
    url = api_base_url.replace("ITEM_NO", content_episodes_id)
    while flag:
        page_url = url.replace("PAGE_NO", str(page_no))
        page_items = parse_episodes(page_url)
        if len(page_items) == 0:
            flag = False
        else:
            all_items = page_items + all_items
        page_no = page_no + 1
    
    return all_items
    

def parse_videos_page(content_url):
    videos_url = content_url + videos_path
    r = requests.get(videos_url, allow_redirects=False)
    type_id = ""
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        video_types = soup.find_all("li", {"role": "presentation"})
        for video_type in video_types:
            type_name = video_type.find("a").get_text().strip()
            if type_name == "Tüm Bölümler":
                type_id = video_type.find("a").get("data-id")
                return type_id
    return type_id

def get_main_page():
    item_list = []
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")
    content_types = soup.find_all("li", {"class": "dropdown"})
    for content_type in content_types:
        #text = content_type.find("a").get_text().strip()
        contents = content_type.find("div", {"class": "row"}).find_all("li")
        for content in contents:
            content_url = content.find("a").get("href")
            content_name = content.find("a").get_text().strip()
            content_img = img_base_url + content.find("a").get("data-image")
            temp_item = {
                "name": content_name,  
                "url": content_url,
                "img": content_img
            }
            item_list.append(temp_item)
    return item_list

def main(start=0, end=0):
    data = []
    content_list = get_main_page()
    if end == 0:
        end_index = len(content_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        content = content_list[i]
        content_episodes_id = parse_videos_page(content["url"])
        if content_episodes_id:
            episodes = get_episodes(content_episodes_id)
            temp_content = content.copy()
            temp_content["episodes"] = episodes
            #print(json.dumps(episodes, indent=4, ensure_ascii=False))
            data.append(temp_content)
    
    create_single_m3u("../../lists/video/sources/www-tv8-com-tr", data, "all")
    f = open("www-tv4-com-tr-all.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-tv8-com-tr/all", data)


   
main()