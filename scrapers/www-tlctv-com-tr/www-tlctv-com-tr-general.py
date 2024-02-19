import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

ajax_url = "https://www.tlctv.com.tr/ajax/more"
stream_url_pattern = "https://dygvideo.dygdigital.com/api/redirect?PublisherId=27&ReferenceId={}&SecretKey=NtvApiSecret2014*"

headers = {
    'Referer': "https://www.tlctv.com.tr/",
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_single_program_page(page=0):
    all_programs = []
    data = {
        'type': 'discover',
        'slug': 'a-z',
        'page': page,
    }
    r = requests.post(ajax_url, headers=headers, data=data)
    soup = BeautifulSoup(r.content, "html.parser")
    programs = soup.find_all("div", {"class": "poster"})
    for program in programs:
        program_url = program.find("a").get("href")
        program_img = program.find("img").get("src")
        program_name = program.find("a").get("onclick").replace("GAEventTracker('DISCOVER_PAGE_EVENTS', 'POSTER_CLICKED', '", "").replace("');", "")
        temp_program = {
            "img": program_img,
            "url": program_url,
            "name": program_name
        }
        all_programs.append(temp_program)
    return all_programs

def get_all_programs():
    all_programs = []
    flag = True
    i = 0
    while flag:
        page_programs = get_single_program_page(i)
        if len(page_programs) == 0:
            flag = False
            print("Total number of pages: ", i)
        else:
            all_programs += page_programs
            i += 1
    return all_programs

def get_program_id(url):
    season_list = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        id = soup.find("a", {"class": "dyn-link"}).get("data-program-id")
        season_selector = soup.find("select", {"class": "custom-dropdown"})
        if season_selector:
            seasons = season_selector.find_all("option")
            for season in seasons:
                season_value = season.get("value")
                if season_value not in season_list:
                    season_list.append(season_value)
        return id, season_list
    except Exception as e:
        print(str(e))
        return 0, season_list
    
def parse_episodes_page(id, page, season, serie_name):
    all_episodes = []
    data = {
        "type": "episodes",
        "program_id": id,
        "page": page,
        "season": season
    }
    r = requests.post(ajax_url, headers=headers, data=data)
    soup = BeautifulSoup(r.content, "html.parser")
    episodes = soup.find_all("div", {"class": "item"})
    for episode in episodes:
        name = serie_name + " - " + episode.find("strong").get_text().strip()
        img = episode.find("img").get("src")
        url = episode.find("a").get("href")
        temp_episode = {
            "name": name,
            "img": img,
            "url": url
        }
        all_episodes.insert(0, temp_episode)
    return all_episodes

def get_episodes_by_program_id(id, season_list, serie_name):
    all_episodes = []
    for season in tqdm(season_list):
        flag = True
        page = 0
        while flag:
            #print("Season: ", season, " Page: ", page)
            page_episodes = parse_episodes_page(id, page, season, serie_name)
            if len(page_episodes) == 0:
                flag = False
            else:
                all_episodes = page_episodes + all_episodes
                page += 1
    return all_episodes

def get_stream_url(episode_url):
    try:
        r = requests.get(episode_url)
        soup = BeautifulSoup(r.content, "html.parser")
        reference_id = soup.find("div", {"class": "video-player"}).get("data-video-code")
        return "https://dygvideo.dygdigital.com/api/redirect?PublisherId=20&ReferenceId={}&SecretKey=NtvApiSecret2014*&.m3u8".format(reference_id)
    except:
        return ""


def main(start=0, end=0):
    data = []
    programs_list = get_all_programs()
    if end == 0:
        end_index = len(programs_list)
    else:
        end_index = end
    for i in tqdm(range(start, end_index)):
        program = programs_list[i]
        print(i, program["name"])
        program_id, season_list = get_program_id(program["url"])
        episodes = get_episodes_by_program_id(program_id, season_list, program["name"])
        if len(episodes) > 0:
            temp_program = program.copy()
            temp_program["episodes"] = []
            for episode in tqdm(episodes):
                temp_episode = episode.copy()
                stream_url = get_stream_url(episode["url"])
                if stream_url:
                    temp_episode["stream_url"] = stream_url
                    temp_program["episodes"].append(temp_episode)
            data.append(temp_program)
    print(json.dumps(data, indent=4, ensure_ascii=False))
    input()
    create_single_m3u("../../lists/video/sources/www-tlctv-com-tr", data, "all")
    f = open("www-tlctv-com-tr-programlar.json", "w+")
    json.dump(data, f, ensure_ascii=False, indent=4)
    create_m3us("../../lists/video/sources/www-tlctv-com-tr/programlar", data)


main()