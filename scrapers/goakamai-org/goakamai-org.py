import requests
from tqdm import tqdm
import json
import re
import sys
import time
from math import floor

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us


headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=utf-8',
    'Origin': 'http://goakamai.org',
    'Pragma': 'no-cache',
    'Referer': 'http://goakamai.org/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'x-icx-copyright': 'ICxTransportationGroup',
    "X-Icx-Ts": str(round(time.time() * 1000))
}

print(headers["X-Icx-Ts"])

def get_all_cameras():
    all_items = []
    url = "http://a.cameraservice.goakamai.org/cameras?format=mapPage&{}"
    r = requests.get(url, headers=headers)
    print(r.status_code)
    data = r.json()
    for item in data:
        temp_cam = {
            "img": item["cameraImageURL"],
            "name": item["description"],
            "stream_url": item["streamingURL"]
        }
        if temp_cam["stream_url"]:
            all_items.append(temp_cam)
    return all_items

def main():
    data = [
        {
            "name": "Hawaii - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("goakamai-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "hi")



if __name__=="__main__": 
    main() 