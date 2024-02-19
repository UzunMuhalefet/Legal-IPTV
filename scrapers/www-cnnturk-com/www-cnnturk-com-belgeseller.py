import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

base_url = "https://www.cnnturk.com"
loadmore_url = "https://www.cnnturk.com/api/lazy/loadmore"
api_url = "https://www.cnnturk.com/api/cnnvideo/media"

def get_stream_url(data_id):
    params = {
        "id": data_id
    }
    url =  ""
    try:
        r = requests.get(api_url, params=params)
        data = r.json()
        path = data["Media"]["Link"]["SecurePath"]
        if "m3u8" in path:
            if path[0] != "/":
                path = "/" + path
            url = data["Media"]["Link"]["ServiceUrl"] + path
            return url
        return ""
    except:
        return ""


def parse_episode_page(url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, "html.parser")
        data_id = soup.find("div", {"class": "player-container"}).get("data-id")
        return data_id
    except:
        return ""

def get_episodes(path, url, skip=0, top=99):
    all_items = []
    params = {
        "orderBy": 'StartDate+asc',
        "skip": skip, 
        "top": top,
        "contentTypes": "NewsVideo,Clip,TVShow",
        "viewName": "load-vertical",
        "controlIxName": "program-videolari",
        "subPath": True,
        "url": url,
        "paths": path
    }
    try:
        r = requests.get(loadmore_url, params=params)
        soup = BeautifulSoup(r.content, "html.parser")
        episodes = soup.find_all("div", {"class": "col-xs-6"})
        #episodes = soup.find_all("a")
        for episode in episodes:
            episode_name = episode.find("div", {"class": "caption-title"}).get_text().strip().replace('\"', "'")
            episode_url = base_url + episode.find("a").get("href")
            episode_img = episode.find_all("img")[1].get("src")
            temp_episode = {
                "name": episode_name,
                "url": episode_url,
                "img": episode_img
            }
            all_items.append(temp_episode)
    except Exception as e:
        print(str(1))
    return all_items

def parse_content_page(url):
    data_path = ""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    load_more_button = soup.find("div", {"id": "load-more-container-program-videolari"})
    if load_more_button:
        data_path = soup.find("button", {"class": "btn-load-more"}).get("data-paths")
    return data_path

def get_category_page(path):
    all_items = []
    params = {
        "orderBy": 'IxName+asc',
        "skip": 0,
        "top": 99,
        "contentTypes": "TVShowContainer",
        "viewName": "load-vertical-circle",
        "controlIxName": "tum-programlar",
        "paths": path
    }
    r = requests.get(loadmore_url, params=params)
    soup = BeautifulSoup(r.content, "html.parser")
    contents = soup.find_all("div", {"class": "col-xs-6"})
    for content in contents:
        content_name = content.get_text().strip()
        content_img = content.find("img").get("src")
        content_url = base_url + content.find("a").get("href")
        temp_content = {
            "name": content_name,
            "img": content_img,
            "url": content_url
        }
        all_items.append(temp_content)

    return all_items


def main_all_category(path):
    data = []
    programs = get_category_page(path)
    for program in tqdm(programs):
        print(program["name"])
        program_path = parse_content_page(program["url"])
        if program_path:
            episodes = get_episodes(program_path, program["url"].replace(base_url, ""))
            temp_program = program.copy()
            temp_program["episodes"] = []
            for episode in tqdm(episodes):
                media_id = parse_episode_page(episode["url"])
                stream_url = get_stream_url(media_id)
                if stream_url:
                    episode["stream_url"] = stream_url
                    temp_program["episodes"].append(episode)
            #print(json.dumps(temp_program, indent=4, ensure_ascii=False))
            data.append(temp_program)
    create_single_m3u("../../lists/video/sources/www-cnnturk-com", data, "belgeseller")
    f = open("www-cnnturk-com-belgeseller.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-cnnturk-com/belgeseller", data)

belgesel_category_path = "/tv-cnn-turk/belgeseller/"

main_all_category(belgesel_category_path)