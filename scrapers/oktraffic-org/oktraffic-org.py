import requests
from tqdm import tqdm
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

img_url = "https://upload.wikimedia.org/wikipedia/commons/9/99/TransportationLogoVDark.png"

headers = {
    "filter": '{"include":[{"relation":"mapCameras","scope":{"include":"streamDictionary","where":{"status":{"neq":"Out Of Service"},"type":"Web","blockAtis":{"neq":"1"}}}},{"relation":"cameraLocationLinks","scope":{"include":["linkedCameraPole","cameraPole"]}}]}'
}

def get_all_cameras():
    all_items = []
    r = requests.get("https://oktraffic.org/api/CameraPoles", headers=headers)
    data = r.json()
    for item in data:
        item_cams = item["mapCameras"]
        for cam in item_cams:
            if "streamDictionary" in cam:
                if "streamSrc" in cam["streamDictionary"]:
                    if "m3u8" in cam["streamDictionary"]["streamSrc"]:
                        temp_cam = {
                            "name": cam["streamDictionary"]["streamName"],
                            "img": img_url,
                            "stream_url": cam["streamDictionary"]["streamSrc"]
                        }
                        all_items.append(temp_cam)
    return all_items

def main():
    data = [
        {
            "name": "Oklahoma - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("oktraffic-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ok")



if __name__=="__main__": 
    main() 