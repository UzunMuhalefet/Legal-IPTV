import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

def get_all_shows():
    all_shows = []
    url = "https://www.cartoonnetwork.co.uk/api/shows?locale=tr-TR&device=DESKTOP"
    r = requests.get(url)
    print(r.status_code)
    shows = r.json()
    for show in shows:
        temp_show = {
            "name": shows[show]["name"].replace('"', "'"),
            "id": shows[show]["id"]
        }
        all_shows.append(temp_show)

    return all_shows

def get_all_episodes_by_show(showid, show_name=""):
    all_episodes = []
    params = {
        "device": "DESKTOP",
        "order": "PUBLICATION_DATE",
        "locale": "tr-TR",
        "contentType": "video",
        "offset": 0,
        "limit": 1000,
        "showId": showid
    }
    url = "https://www.cartoonnetwork.co.uk/api/filtered-contents"
    r = requests.get(url, params=params)
    episodes = r.json()
    for episode in episodes:
        temp_episode = {
            "name": show_name + " - " + episode["data"]["title"],
            "img": episode["data"]["video"]["thumb"],
            "url": episode["data"]["friendlyUrl"]
        }
        all_episodes.insert(0, temp_episode)
    
    return all_episodes

def get_stream_url_by_id(asset_id):
    params = {
        "id": asset_id,
        "channel": "CN_APAC_TR",
        "language": "TUR"
    }
    try:
        r = requests.get("https://avsvideoapi.dmti.cloud/api/publicvideo", params=params)
        return r.json()["source"]
    except:
        return ""
    

def get_asset_id(friendly_url):
    params = {
        "friendly_url": friendly_url,
        "locale": "tr-TR",
        "kind": "video",
        "device": "DESKTOP"
    }
    try:
        r = requests.get("https://www.cartoonnetwork.co.uk/api/content-by-friendly-url", params=params)
        return r.json()["video"]["asset_id"]
    except:
        return ""

def get_stream_url_by_friendly_url(friendly_url):
    asset_id = get_asset_id(friendly_url)
    if asset_id:
        return get_stream_url_by_id(asset_id)
    else:
        return ""


def main(start=0, end=0):
    data = []
    shows_list = get_all_shows()
    if end == 0:
        end_index = len(shows_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        show = shows_list[i]
        print(i, show["name"])
        episodes = get_all_episodes_by_show(show["id"], show["name"])
        if len(episodes) > 0:
            temp_show = {
                "name": show["name"],
                "episodes": []
            }
            for episode in tqdm(episodes):
                stream_url = get_stream_url_by_friendly_url(episode["url"])
                if stream_url:
                    temp_episode = {
                        "name": episode["name"],
                        "img": episode["img"],
                        "stream_url": stream_url
                    }
                    temp_show["episodes"].append(temp_episode)
            data.append(temp_show)
    create_single_m3u("../../lists/video/sources/www-cartoonnetwork-com-tr", data, "videolar")
    with open("www-cartoonnetwork-com-tr-videolar.json", "w+", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-cartoonnetwork-com-tr/videolar", data)


main()
    
'''result = get_all_shows()
result = get_all_episodes_by_show(326, "Adventure Time")
print(get_stream_url_by_friendly_url("sürekli-dizi-1-sezon-1-bölüm-güç"))
input()
print(json.dumps(result, indent=4, ensure_ascii=False))'''