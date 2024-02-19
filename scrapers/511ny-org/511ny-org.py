import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

camera_base_url = "https://511ny.org/tooltip/Cameras/"
img_base_url = "https://511ny.org"

def get_all_cameras():
    all_items = []
    r = requests.get("https://511ny.org/map/mapIcons/Cameras")
    data = r.json()["item2"]
    for cam in data:
        temp_cam = {
            "id": cam["itemId"]
        }
        all_items.append(temp_cam)
    return all_items


def get_camera_details(id):
    cam_detail = {}
    url = camera_base_url + str(id)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    checkhls = soup.find("div", {"data-streamtype": "application/x-mpegURL"})
    if checkhls:
        cam_detail["stream_url"] = checkhls.get("data-videourl")
        cam_detail["img"] = img_base_url + soup.find("img", {"class": "cctvImage"}).get("src")
        cam_detail["name"] = soup.find("td", {"id": "CameraTooltipDescriptionColumn"}).get_text().strip()
    return cam_detail

def main():
    data = [
        {
            "name": "New York - Traffic Cams",
            "episodes": []
        }
    ]
    all_items = get_all_cameras()
    for item in tqdm(all_items):
        temp_cam = get_camera_details(item["id"])
        if "stream_url" in temp_cam:
            data[0]["episodes"].append(temp_cam)
    
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ny")
    f = open("511ny-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)

main()

