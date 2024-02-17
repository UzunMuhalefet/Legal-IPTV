import csv
import json
import sys

## CSV must have the following columns: name and url
## CSV may have the following columns: tvg-logo and group-title
## Other columns will be ignored.

def build_m3u(channels):
    text = "#EXTM3U\n"
    for channel in channels:
        c_text = "#EXTINF:1"
        if "tvg-logo" in channel:
            c_text += ' tvg-logo="' + channel["tvg-logo"] + '"'
        if "group-title" in channel:
            c_text += ' group-title="' + channel["group-title"] + '"'
        c_text += ',' + channel["name"] + "\n"
        c_text += channel["url"] + "\n"
        text += c_text
    return text


f = open(sys.argv[1], "r", encoding="utf-8")
csv_reader = csv.DictReader(f)
channels = list(csv_reader)
output = open(sys.argv[1].replace(".csv", ".m3u"), "w+", encoding="utf-8")
text = build_m3u(channels)
output.write(text)
output.close()