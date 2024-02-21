import requests
from tqdm import tqdm
import json
import sys
from math import ceil

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

headers = {
    'ApiKey': '8d3b7a82635d476795c09b2c41facc60',
    'Origin': 'https://smartway.tn.gov',
    'Referer': 'https://smartway.tn.gov/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

def get_all_cameras():
    all_items = []
    url = "https://www.tdot.tn.gov/opendata/api/public/RoadwayCameras"
    r = requests.get(url, headers=headers)
    data = r.json()
    for cam in data:
        temp_cam = {
            "name": cam["title"],
            "img": cam["thumbnailUrl"],
            "stream_url": cam["httpsVideoUrl"]
        }
        if temp_cam["stream_url"]:
            all_items.append(temp_cam)
    
    return all_items

def main():
    data = [
        {
            "name": "Tennessee - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("smartway-tn-gov.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "tn")

if __name__=="__main__": 
    main() 