import requests
from tqdm import tqdm
import json
import sys
from math import ceil

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

def get_page_cameras(page):
    print()
    all_items = []
    json_data['variables']["input"]["recordOffset"] = page*1000
    json_data['variables']["input"]["recordLimit"] = 1000
    r = requests.post("https://www.cotrip.org/api/graphql", json=json_data)
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

def get_all_cameras():
    all_items = []
    json_data['variables']["input"]["recordLimit"] = 25
    r = requests.post("https://www.cotrip.org/api/graphql", json=json_data)
    total_cams = r.json()["data"]["listCameraViewsQuery"]["totalRecords"]
    page = ceil(total_cams/1000)
    for i in range(0, page):
        page_items = get_page_cameras(i)
        all_items += page_items
    
    return all_items

def main():
    data = [
        {
            "name": "Colorado - Traffic Cameras",
            "episodes": get_all_cameras()
        }
    ]
    f = open("www-cotrip-org.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_single_m3u("../../lists/cameras/countries/us/traffic", data, "co")


if __name__=="__main__": 
    main() 