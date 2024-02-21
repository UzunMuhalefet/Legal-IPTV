import re, requests, json
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import parse_qs, urlparse
import sys
import json

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

domain = "https://www.mdottraffic.com/"
pattern = r"javascript:switchImage\((.*?)\)"

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

def parse_img_cam_page(url):
    cams = []
    r = requests.get(url)
    results = re.findall(pattern, r.text)
    for result in results:
        temp_cam = {}
        params = result.split("', ")
        temp_cam["name"] = params[2].replace("'", "").strip()
        temp_cam["url"] = domain + "mapbubbles/streamcam.aspx?cam=" + params[1].replace("'", "").strip()
        temp_cam["img"] = params[0].replace("'", "").strip()
        stream_url = get_stream_url(temp_cam["url"])
        if stream_url:
            temp_cam["stream_url"] = stream_url
            cams.append(temp_cam)
    return cams
    

def get_all_cameras():
    all_items = []
    r = requests.post('https://www.mdottraffic.com/default.aspx/LoadCameraData', allow_redirects=False, headers=headers)
    data = r.json()['d']
    for cam in tqdm(data):
        soup = BeautifulSoup(cam["framehtml"], "html.parser")
        cam_url = domain + soup.find("iframe").get("src")
        cams = parse_img_cam_page(cam_url)
        all_items += cams
    
    return all_items

def main():
    data = [
        {
            "name": "Mississippi - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("www-mdottrafic-com.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ms")


if __name__=="__main__": 
    main() 