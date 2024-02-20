import re, requests, json
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin
import sys
import json
import time

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

domain = "https://www.dot.ri.gov"

pattern = r'"openVideoPopup2\(\'(.*?)\''

def get_sub_page(url):
    all_items = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    cameras = soup.find_all("a", {"class": "open-player"})
    for cam in cameras:
        name = cam.find("img").get("alt").strip()
        img = cam.find("img").get("src")
        results = re.findall(pattern, str(cam))
        if results:
            temp_cam = {
                "name": name,
                "img": urljoin(url, img),
                "stream_url": results[0]
            }
            all_items.append(temp_cam)
    return all_items

def get_all_cameras():
    all_items = []
    url = domain + "/travel/index.php"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    cameras = soup.find_all("a", {"class": "open-player"})
    for cam in cameras:
        name = cam.find("img").get("alt").strip()
        img = cam.find("img").get("src")
        results = re.findall(pattern, str(cam))
        if results:
            temp_cam = {
                "name": name,
                "img": urljoin(url, img),
                "stream_url": results[0]
            }
            all_items.append(temp_cam)

    subpages = soup.find_all("option")
    for subpage in subpages:
        subpage_url = domain + subpage.get("value")
        all_items += get_sub_page(subpage_url)

    return all_items

def main():
    data = [
        {
            "name": "Rhode Island - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("www-dot-ri-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ri")


if __name__=="__main__": 
    main() 