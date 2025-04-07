import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import sys

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us, create_json

main_url = "https://puhutv.com/"
diziler_url = "https://puhutv.com/dizi"

def get_series_details(series_id):
    url = f"https://appservice.puhutv.com/service/serie/getSerieInformations?id={series_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()[0]
    return {"title": "", "seasons": []}

def get_stream_urls(season_slug):
    url = urljoin(main_url, season_slug)
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Error: {r.status_code}, URL: {url}")
        return []

    soup = BeautifulSoup(r.content, "html.parser")
    content = json.loads(soup.find("script", {"id": "__NEXT_DATA__"}).string)["props"]["pageProps"]["episodes"]["data"]
    episodes = []
    for episode in content["episodes"]:
        episodes.append({
            "id": episode["id"],
            "name": episode["name"],
            "img": episode["image"],
            "url": urljoin(main_url, episode["slug"]),
            "stream_url": f"https://dygvideo.dygdigital.com/api/redirect?PublisherId=29&ReferenceId={episode['video_id']}&SecretKey=NtvApiSecret2014*&.m3u8"
        })
    return episodes

def get_all_content(url):
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Error: {r.status_code}, URL: {url}")
        return []

    soup = BeautifulSoup(r.content, "html.parser")
    contents = json.loads(soup.find("script", {"id": "__NEXT_DATA__"}).string)["props"]["pageProps"]["data"]["data"]["container_items"]
    series_list = []
    for item in contents:
        for content in item["items"]:
            series_list.append(content)

    all_series = []

    if not series_list:
        print("No series found.")
        return []
    for series in tqdm(series_list, desc="Processing Series"):
        print(f"Processing {series['name']}")
        series_id = series["id"]
        series_name = series["name"]
        series_slug = series["meta"]["slug"]
        series_img = series["image"]

        series_details = get_series_details(series_id)
        if not series_details["seasons"]:
            continue

        temp_series = {
            "name": series_name,
            "img": series_img,
            "url": urljoin(main_url, series_slug),
            "episodes": []
        }

        for season in tqdm(series_details["seasons"], desc=f"Processing {series_name} Seasons"):
            season_slug = season["slug"]
            season_name = season["name"]
            episodes = get_stream_urls(season_slug)
            for episode in episodes:
                episode["name"] = f"{season_name} - {episode['name']}"
                temp_series["episodes"].append(episode)

        all_series.append(temp_series)

    return all_series

def main():
    data = get_all_content(diziler_url)
    create_json("puhutv-com-diziler.json", data)
    create_single_m3u("../../lists/video/sources/puhutv-com", data, "diziler")
    create_m3us("../../lists/video/sources/puhutv-com/diziler", data)

if __name__ == "__main__":
    main()
