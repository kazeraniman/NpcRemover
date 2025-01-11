import json
import urllib.parse
import webbrowser
from pathlib import Path

RES_FOLDER_PATH = Path(f'{Path(__file__).parent.parent}/res/')
ID_JSON_FILE_PATH = Path.joinpath(RES_FOLDER_PATH, 'ids.json')

FILE_READ_MODE = 'r'

WIKI_URL = 'https://eldenring.wiki.gg/wiki/Special:Search?{0}&go=Go&ns0=1'
SEARCH_QUERY_PARAM = 'search'


def read_id_file():
    with open(ID_JSON_FILE_PATH, FILE_READ_MODE) as f:
        return json.load(f)

def open_wiki(npc_name: str):
    webbrowser.open(WIKI_URL.format(urllib.parse.urlencode({SEARCH_QUERY_PARAM: npc_name})))
