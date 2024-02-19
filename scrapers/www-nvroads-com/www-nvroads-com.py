import requests
from tqdm import tqdm
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

img_path = "https://www.nvroads.com/map/Cctv/"


query = {"columns":[{"data":None,"name":""},{"name":"sortId","s":True},{"name":"cityName","s":True},{"name":"roadway","s":True},{"data":4,"name":""}],"order":[{"column":1,"dir":"asc"},{"column":2,"dir":"asc"},{"column":3,"dir":"asc"}],"start":600,"length":100,"search":{"value":""}}


def parse_cameras_page(start, total_number=0):
    print(start, " requested")
    page_cameras = []
    query["start"] = start
    params = {
        'query': json.dumps(query),
        'lang': 'en',
    }
    r = requests.get("https://www.nvroads.com/List/GetData/Cameras", params=params)
    data = r.json()["data"]
    recordsTotal = r.json()["recordsTotal"]
    if total_number == recordsTotal:
        return []
    else:
        for cam in data:
            temp_cam = {
                "name": cam["displayName"],
                "img": img_path + cam["id"],
                "stream_url": cam["videoUrl"]
            }
            page_cameras.append(temp_cam)
        
        return page_cameras

def get_all_cameras():
    all_cameras = []
    flag = True
    start = 0
    while flag:
        page_cameras = parse_cameras_page(start, len(all_cameras))
        if len(page_cameras) == 0:
            flag = False
        else:
            all_cameras += page_cameras
            start += 100
    return all_cameras

data = [
    {
        "name": "Nevada - Traffic Cameras",
        "episodes": []
    }
]

data[0]["episodes"] = get_all_cameras()

create_single_m3u("../../lists/cameras/countries/us/traffic", data, "nv")
f = open("www-nvroads-com.json", "w+")
json.dump(data, f, ensure_ascii=False, indent=4)