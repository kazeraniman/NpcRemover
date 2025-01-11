import json
import urllib.parse
import webbrowser
from pathlib import Path

BASE_FOLDER_PATH = Path(__file__).parent.parent
RES_FOLDER_PATH = Path.joinpath(BASE_FOLDER_PATH, 'res/')
ID_JSON_FILE_PATH = Path.joinpath(RES_FOLDER_PATH, 'ids.json')

FILE_READ_MODE = 'r'
FILE_WRITE_MODE = 'w'

WIKI_URL = 'https://eldenring.wiki.gg/wiki/Special:Search?{0}&go=Go&ns0=1'
SEARCH_QUERY_PARAM = 'search'


def read_id_file() -> dict:
    with open(ID_JSON_FILE_PATH, FILE_READ_MODE) as f:
        return json.load(f)

def open_wiki(npc_name: str):
    webbrowser.open(WIKI_URL.format(urllib.parse.urlencode({SEARCH_QUERY_PARAM: npc_name})))
