import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import re
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

pattern = r'videoStreamURL=\"(.*?)\"'
img_pattern = r'posterURL=\"(.*?)\"'

def get_all_cameras():
    all_items = []
    url = "https://cwwp2.dot.ca.gov/vm/streamlist.htm"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    cameras = soup.find("table").find_all("a")
    for cam in cameras:
        temp_cam = {
            "name": cam.get_text().strip(),
            "url": cam.get("href")
        }
        all_items.append(temp_cam)
    return all_items

def get_stream_url(url):
    r = requests.get(url)
    results = re.findall(pattern, r.text)
    img_results = re.findall(img_pattern, r.text)
    if results:
        return results[0], img_results[0]
    else:
        return "", ""


def main():
    data = [
        {
            "name": "California - Traffic Cameras",
            "episodes": []
        }
    ]
    cameras = get_all_cameras()
    for camera in tqdm(cameras):
        stream_url, img = get_stream_url(camera["url"])
        if stream_url:
            camera["stream_url"] = stream_url
            camera["img"] = img
            data[0]["episodes"].append(camera)
    
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ca")
    f = open("cwwp2-dot-ca-gov.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)

main()
