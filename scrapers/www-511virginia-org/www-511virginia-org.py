import requests
from tqdm import tqdm
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

def get_all_cameras():
    all_items = []
    url = "https://www.511virginia.org/data/geojson/icons.cameras.geojson"
    r = requests.get(url)
    data = r.json()["features"]
    for item in data:
        temp_cam = {
            "name": item["properties"]["description"],
            "img": item["properties"]["image_url"],
            "stream_url": item["properties"]["https_url"]
        }
        if temp_cam["stream_url"]:
            all_items.append(temp_cam)
    
    return all_items

def main():
    data = [
        {
            "name": "Virginia - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("www-511virginia-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "va")



if __name__=="__main__": 
    main() 
