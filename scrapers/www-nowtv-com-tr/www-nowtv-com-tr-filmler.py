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

api_url = "https://www.nowtv.com.tr/ajax/programs"

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
                movie_slug = url.split("/")[-2]
                stream_url = "https://uzunmuhalefet.serv00.net/nowtv.php?serie={}&episode=1&.m3u8".format(movie_slug)
                temp_item = {
                    "name": name,
                    "img": img,
                    "url": url,
                    "stream_url": stream_url
                }
                item_list.append(temp_item)
        else:
            flag = False
    return item_list

def main():
    data = [
        {
            "name": "Filmler",
            "episodes": get_all_items("movies")
        }
    ]
    f = open("www-nowtv-com-tr-filmler.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/video/sources/www-nowtv-com-tr", data, "filmler")

if __name__=="__main__": 
    main() 