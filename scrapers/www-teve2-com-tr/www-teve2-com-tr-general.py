import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

site_url = "https://www.teve2.com.tr"
action_media_url = "https://www.teve2.com.tr/action/media/"

episodes_path = "/bolumler"

episodes_params = {
    "page": "1",
    "orderby": "StartDate asc"
}

def get_stream_url(media_url):
    
    try:
        r = requests.get(media_url)
        data = r.json()
        if data["Status"] == "Success":
            path = data["Media"]["Link"]["SecurePath"].split("?")[0]
            if path[0] != "/":
                path = "/" + path
            url = data["Media"]["Link"]["ServiceUrl"] + path
            return url
        else:
            return ""
    except:
        return ""

def parse_bolum_page(episode_url):
    r = requests.get(episode_url)
    soup = BeautifulSoup(r.content, "html.parser")
    media_id = soup.find("body").get("data-content-id")
    if media_id:
        return action_media_url + media_id
    else:
        return ""

def parse_bolumler_page(page_url):
    episodes_list = []
    r = requests.get(page_url)
    soup = BeautifulSoup(r.content, "html.parser")
    episodes = soup.find("div", {"class": "thumbnail-slider-container"}).find_all("a", {"class": "thumbnail"})
    for episode in episodes:
        episode_url = site_url + episode.get("href")
        episode_img = episode.find("img").get("data-src")
        episode_name = episode.get_text().strip()
        temp_episode = {
            "name": episode_name,
            "img": episode_img,
            "url": episode_url
        }
        episodes_list.append(temp_episode)
    return episodes_list

def get_bolumler_page(serie_url):
    all_episodes = []
    episodes_url = serie_url + episodes_path
    r = requests.get(episodes_url, params=episodes_params)
    if r.status_code != 200:
        return all_episodes
    else:
        soup = BeautifulSoup(r.content, "html.parser")
        page_block = soup.find("ul", {"class": "pagination-numbers"})
        if page_block:
            pages = page_block.find_all("li")
            for page in tqdm(pages):
                page_url = r.url.split("?")[0] + page.find("a").get("href")
                page_url = page_url.replace(" ", "+")
                all_episodes = all_episodes + parse_bolumler_page(page_url)
            return all_episodes

def parse_arsiv_page(url):
    series_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    series = soup.find("div", {"class": "thumbnail-slider-container"}).find_all("div", {"class": "col-md-3"})
    for serie in series:
        serie_url = site_url + serie.find("a").get("href")
        serie_img = serie.find("img").get("data-src")
        serie_name = serie.get_text().strip()
        temp_serie = {
            "name": serie_name,
            "img": serie_img,
            "url": serie_url,
            "episodes": []
        }
        series_list.append(temp_serie)
    return series_list

def get_arsiv(url):
    all_series = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    pages = soup.find("ul", {"class": "pagination-numbers"}).find_all("li")
    for page in tqdm(pages):
        page_url = url + page.find("a").get("href")
        series_of_the_page = parse_arsiv_page(page_url)
        all_series = all_series + series_of_the_page
    return all_series

def main(url, name, start=0, end=0):
    data = []
    series_list = get_arsiv(url)
    if end == 0:
        end_index = len(series_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        serie = series_list[i]
        print(i, serie["name"])
        episodes = get_bolumler_page(serie["url"])
        if episodes:
            temp_serie = serie.copy()
            temp_serie["episodes"] = []
            for episode in tqdm(episodes):
                media_url = parse_bolum_page(episode["url"])
                stream_url = get_stream_url(media_url)
                episode["stream_url"] = stream_url
                if stream_url:
                    temp_serie["episodes"].append(episode)
            data.append(temp_serie)
    create_single_m3u("../../lists/video/sources/www-teve2-com-tr", data, name)
    f = open("www-teve2-com-tr-" + name + ".json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-teve2-com-tr/" + name, data)

dizi_page_url = "https://www.teve2.com.tr/diziler/arsiv"
program_page_url = "https://www.teve2.com.tr/programlar/arsiv"

main(dizi_page_url, "diziler")

main(program_page_url, "programlar")