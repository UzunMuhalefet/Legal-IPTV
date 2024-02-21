import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

img_url = "https://transportation.wv.gov/Turnpike/travel_resources/safety/Documents/511%20logo.jpg"

def get_all_cameras():
    all_items = []
    r = requests.get("https://wv511.org/wsvc/gmap.asmx/buildCamerasJSONjs")
    response = r.text
    data_to_load = response.split("var camera_data = ")[-1]
    data = json.loads(data_to_load)
    for cam in data["cams"]:
        soup = BeautifulSoup(cam["description"], "html.parser")
        name = soup.get_text().strip().replace("West Virginia DOT", "").strip()
        temp_cam = {
            "stream_url": "https://sfs1.roadsummary.com/rtplive/{}/playlist.m3u8".format(cam["md5"]),
            "name": name,
            "img": img_url
        }
        all_items.append(temp_cam)
    return all_items

def main():
    data = [
        {
            "name": "West Virginia - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("oktraffic-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "wv")


if __name__=="__main__": 
    main() 