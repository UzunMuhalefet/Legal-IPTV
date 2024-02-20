import re, requests, json
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import parse_qs, urlparse
import sys
import json

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

domain = "https://www.mdottraffic.com/"

headers = {
    'referer': 'https://www.mdottraffic.com/default.aspx?showMain=true',
    'x-requested-with': 'XMLHttpRequest',
    'content-type': 'application/json; charset=UTF-8',
}

def get_stream_url(url):
    stream_url = ""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    source = soup.find("source", {"type": "application/x-mpegurl"})
    if source:
        stream_url = source.get("src")
    
    return stream_url

def get_cam_detail(url):
    temp_cam = {
        "name": "",
        "img": "",
        "stream_url": "",
        "url": ""
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    cam_img = soup.find("img", {"id": "camimg"}).get("src")
    temp_cam["img"] = cam_img
    parsed = urlparse(cam_img)
    qs = parse_qs(parsed.query)
    if 'streamname' in qs:
        cam_url = domain + "streamcam.aspx?cam=" + qs['streamname'][0].split('.')[0]
        temp_cam["url"] = cam_url
        stream_url = get_stream_url(cam_url)
        if stream_url:
            cam_name = soup.find("img", {"id": "camimg"}).get("alt")
            temp_cam["stream_url"] = stream_url
            temp_cam["name"] = cam_name
    return temp_cam


def get_all_cameras():
    all_items = []
    r = requests.post('https://www.mdottraffic.com/default.aspx/LoadCameraData', allow_redirects=False, headers=headers)
    data = r.json()['d']
    for cam in tqdm(data):
        soup = BeautifulSoup(cam["framehtml"], "html.parser")
        cam_url = domain + soup.find("iframe").get("src")
        cam_detail = get_cam_detail(cam_url)
        if cam_detail["stream_url"]:
            all_items.append(cam_detail)
    
    return all_items

def main():
    data = [
        {
            "name": "Mississippi - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("www-dot-ri-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ms")


if __name__=="__main__": 
    main() 