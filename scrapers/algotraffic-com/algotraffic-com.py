import requests
from tqdm import tqdm
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

### ACCESS OVER USA

def get_all_cameras():
    all_items = []
    r = requests.get('https://api.algotraffic.com/v3.0/Cameras')
    data = r.json()
    for cam in data:
        name = cam["location"]["displayRouteDesignator"] + " " + cam["location"]["displayCrossStreet"]
        stream_url = cam["hlsUrl"]
        img = cam["imageUrl"]
        temp_cam = {
            "name": name,
            "img": img,
            "stream_url": stream_url
        }
        if temp_cam["stream_url"].strip():
            all_items.append(temp_cam)
    return all_items

def main():
    data = [
        {
            "name": "Alabama - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("algotraffic-com.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "al")


if __name__=="__main__": 
    main() 