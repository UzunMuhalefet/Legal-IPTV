import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

base_url = "https://www.tv4.com.tr"

def parse_episode_page(episode_url):
    try:
        r = requests.get(episode_url)
        soup = BeautifulSoup(r.content, "html.parser")
        stream_url = soup.find("source").get("src")
        return stream_url.strip()
    except:
        return ''
    
def get_episodes_page(content_url):
    all_episodes = []
    if "ekonomi" in content_url:
        episodes_url = content_url.replace("ekonomi/", "").replace("--", "-") + "-tum-bolumleri"
    else:
        episodes_url = content_url.replace("yasam/", "").replace("--", "-") + "-tum-bolumleri"
    r = requests.get(episodes_url, allow_redirects=False)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        episodes = soup.find("div", {"class": "pragram-list-wrapper"}).find_all("div", {"class": "item"})
        for episode in episodes:
            episode_name = episode.find("div", {"class": "name"}).get_text().strip()
            episode_img = episode.find("img").get("src")
            episode_url = base_url + episode.find("a").get("href")
            temp_episode = {
                "name": episode_name,
                "img": episode_img,
                "url": episode_url
            }
            all_episodes.insert(0,temp_episode)            
    return all_episodes

def get_programs_page():
    all_items = []
    url = "https://www.tv4.com.tr/yasam-programlar"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    contents = soup.find("div", {"class": "pragram-list-wrapper"}).find_all("div", {"class": "item"})
    for content in contents:
        content_img = content.find("img").get("src")
        content_name = content.find("div", {"class": "name"}).get_text().strip()
        content_url = base_url + content.find("a").get("href")
        #print(content_name, content_url)
        temp_content = {
            "name": content_name,
            "img": content_img,
            "url": content_url
        }
        all_items.append(temp_content)

    return all_items

def main(start=0, end=0):
    data = []
    programs_list = get_programs_page()
    if end == 0:
        end_index = len(programs_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        program = programs_list[i]
        print(i, program["name"])
        episodes = get_episodes_page(program["url"])
        if episodes:
            temp_program = program.copy()
            temp_program["episodes"] = []
            for episode in tqdm(episodes):
                stream_url = parse_episode_page(episode["url"])
                episode["stream_url"] = stream_url
                if stream_url:
                    temp_program["episodes"].append(episode)
            data.append(temp_program)
    create_single_m3u("../../lists/video/sources/www-tv4-com-tr", data, "all")
    f = open("www-tv4-com-tr-programlar.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-tv4-com-tr/programlar", data)

main()
