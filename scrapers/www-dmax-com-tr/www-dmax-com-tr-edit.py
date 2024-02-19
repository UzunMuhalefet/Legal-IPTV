import sys
import json

sys.path.insert(0, '../../utilities')
from jsontom3u import create_single_m3u, create_m3us

f = open("www-dmax-com-tr-programlar.json", "r", encoding="utf-8")
data = json.load(f)

create_single_m3u("../../lists/video/sources/www-dmax-com-tr", data, "all")
create_m3us("../../lists/video/sources/www-dmax-com-tr/programlar", data)