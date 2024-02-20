import requests
from tqdm import tqdm
import json
import sys
from math import ceil

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

img_base_url = "https://511ga.org/map/Cctv/"

query = {"columns":[{"data":None,"name":""},{"name":"sortId","s":True},{"name":"roadway","s":True},{"data":3,"name":""}],"order":[{"column":1,"dir":"asc"},{"column":2,"dir":"asc"}],"start":0,"length":100,"search":{"value":""}}
headers = {
    "Referer": "https://511ga.org/"
}

def get_page_cameras(start):
    print(start, "requested")
    all_items = []
    query["start"] = start*100
    params = {
        'query': json.dumps(query),
        'lang': 'en',
    }
    r = requests.get('https://511ga.org/List/GetData/Cameras', params=params, headers=headers)
    cameras = r.json()["data"]
    for cam in cameras:
        if cam["videoUrl"]:
            temp_cam = {
                "stream_url": cam["videoUrl"],
                "name": cam["displayName"],
                "img": img_base_url + cam["DT_RowId"]
            }
            all_items.append(temp_cam)
    return all_items

def get_all_cameras():
    all_items = []
    r = requests.get('https://511ga.org/List/GetData/Cameras')
    total_cam = r.json()["recordsTotal"]
    limit = ceil(total_cam/100)
    for page in range(0, limit):
        page_cameras = get_page_cameras(page)
        all_items += page_cameras
        #page += 100
    return all_items



def main():
    data = [
        {
            "name": "Georgia - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("511ga-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ga")


if __name__=="__main__": 
    main() 