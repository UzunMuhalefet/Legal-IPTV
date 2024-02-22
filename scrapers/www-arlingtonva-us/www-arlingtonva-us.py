import requests
from tqdm import tqdm
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

stream_domain = "https://itsvideo.arlingtonva.us"

img_url = "https://www.arlingtonva.us/files/sharedassets/public/v/1/countylogo_reverse_vertical.png"


def get_all_cameras():
    all_items = []
    url = "https://datahub-v2-s3.arlingtonva.us/Uploads/AutomatedJobs/Traffic+Cameras.json"
    r = requests.get(url)
    data = r.json()
    for cam in data:
        temp_cam = {
            "name": cam["Camera EncoderB2"],
            "img": img_url,
            "stream_url": stream_domain + ":" + cam["port"] + "/live/" + cam["Camera Site"] + ".stream/playlist.m3u8"
        }
        all_items.append(temp_cam)

    return all_items

def main():
    data = [
        {
            "name": "Virginia (Arlington) - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("www-arlingtonva-us.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "va", mode="add")
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "va-arp")



if __name__=="__main__": 
    main() 
