import requests
from tqdm import tqdm
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

json_data = {
    'query': 'query ($input: ListArgs!) { listCameraViewsQuery(input: $input) { cameraViews { category icon lastUpdated { timestamp timezone } title uri url sources { type src } parentCollection { title uri icon color location { routeDesignator } lastUpdated { timestamp timezone } } } totalRecords error { message type } } }',
    'variables': {
        'input': {
            'west': -180,
            'south': -85,
            'east': 180,
            'north': 85,
            'sortDirection': 'DESC',
            'sortType': 'ROADWAY',
            'freeSearchTerm': '',
            'classificationsOrSlugs': [],
            'recordLimit': 1000,
            'recordOffset': 0,
        },
    },
}

def get_all_cameras():
    all_items = []
    r = requests.post("https://511ia.org/api/graphql", json=json_data)
    data = r.json()["data"]["listCameraViewsQuery"]["cameraViews"]
    for cam in data:
        if cam["category"] == "VIDEO":
            temp_cam = {
                "name": cam["title"].replace("@", "at"),
                "img": cam["url"],
            }
            if cam["sources"]:
                if len(cam["sources"]) > 0:
                    for source in cam["sources"]:
                        if source["type"] == "application/x-mpegURL":
                            temp_cam["stream_url"] = source["src"]
                            all_items.append(temp_cam)
                            break
                            
    return all_items

def main():
    data = [
        {
            "name": "Iowa - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("511ia-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "ia")



if __name__=="__main__": 
    main() 