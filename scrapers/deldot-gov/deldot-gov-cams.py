import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import re
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

def get_all_cameras():
    all_items = []
    url = "https://tmc.deldot.gov/json/videocamera.json?id=4yte"
    r = requests.get(url)
    data = r.json()["videoCameras"]
    for cam in data:
        temp_cam = {
            "name": cam["title"],
            "img": "",
            "stream_url": cam["urls"]["m3u8s"]
        }
        all_items.append(temp_cam)
    return all_items

def main():
    data = [
        {
            "name": "Delaware - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("deldot-gov.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "de")
    


if __name__=="__main__": 
    main() 