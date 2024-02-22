import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

filmler_url = "https://puhutv.com/filmler"

pattern = r'video_id\":\"(.*?)\"'

def get_stream_url(url):
    r = requests.get(url)
    results = re.findall(pattern, r.text)
    if results:
        stream_url = "https://dygvideo.dygdigital.com/api/redirect?PublisherId=29&ReferenceId={}&SecretKey=NtvApiSecret2014*&.m3u8".format(results[0])
        return stream_url
    else:
        return ""


def get_all_content(url):
    all_items = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    contents = soup.find_all("div", {"class": "bwIpNg"})
    for item in tqdm(contents):
        item_path = item.find("a").get("href").replace("detay", "izle")
        item_url = urljoin(url, item_path)
        item_img = item.find("img").get("src")
        item_name = item.find("img").get("title").strip()
        stream_url = get_stream_url(item_url)
        if stream_url:
            temp_item = {
                "name": item_name,
                "img": item_img,
                "url": item_url,
                "stream_url": stream_url
            }
            all_items.append(temp_item)
    return all_items

def main():
    data = [
        {
            "name": "Filmler",
            "episodes": get_all_content(filmler_url)
        }
    ]
    f = open("puhutv-com-filmler.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/video/sources/puhutv-com", data, "filmler")


if __name__=="__main__": 
    main() 

