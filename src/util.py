import json
import shutil
import urllib.parse
import webbrowser
from enum import Enum
from pathlib import Path
from typing import List

BASE_FOLDER_PATH = Path(__file__).parent.parent
RES_FOLDER_PATH = Path.joinpath(BASE_FOLDER_PATH, 'res/')
ID_JSON_FILE_PATH = Path.joinpath(RES_FOLDER_PATH, 'ids.json')
CHR_FOLDER_NAME = 'chr'

FILE_READ_MODE = 'r'
FILE_WRITE_MODE = 'w'

WIKI_URL = 'https://eldenring.wiki.gg/wiki/Special:Search?{0}&go=Go&ns0=1'
SEARCH_QUERY_PARAM = 'search'

ANIBND_FILE_SUFFIX = '.anibnd.dcx'
CHRBND_FILE_SUFFIX = '.chrbnd.dcx'
HTEXBND_FILE_SUFFIX = '_h.texbnd.dcx'
LTEXBND_FILE_SUFFIX = '_l.texbnd.dcx'

class CopyFileResult(Enum):
    SUCCESS = 0
    ERROR = 1

def read_id_file() -> dict:
    with open(ID_JSON_FILE_PATH, FILE_READ_MODE) as f:
        return json.load(f)

def open_wiki(npc_name: str):
    webbrowser.open(WIKI_URL.format(urllib.parse.urlencode({SEARCH_QUERY_PARAM: npc_name})))

def copy_files(id_list: List[str], mod_folder: str):
    anibnd_files = list(RES_FOLDER_PATH.glob(f'*{ANIBND_FILE_SUFFIX}'))
    if len(anibnd_files) != 1:
        return CopyFileResult.ERROR

    replaced_part = anibnd_files[0].name[:-sum(len(s) for s in anibnd_files[0].suffixes)]
    chrbnd_files = list(RES_FOLDER_PATH.glob(f'{replaced_part}{CHRBND_FILE_SUFFIX}'))
    htexbnd_files = list(RES_FOLDER_PATH.glob(f'{replaced_part}{HTEXBND_FILE_SUFFIX}'))
    ltexbnd_files = list(RES_FOLDER_PATH.glob(f'{replaced_part}{LTEXBND_FILE_SUFFIX}'))

    if not (len(chrbnd_files) == 1 and len(htexbnd_files) == 1 and len(ltexbnd_files) == 1):
        return CopyFileResult.ERROR

    mod_folder_path = Path(mod_folder)
    chr_folder = mod_folder_path.joinpath(CHR_FOLDER_NAME)
    chr_folder.mkdir(exist_ok=True)

    for npc_id in id_list:
        copy_file(anibnd_files[0], chr_folder, npc_id, replaced_part)
        copy_file(chrbnd_files[0], chr_folder, npc_id, replaced_part)
        copy_file(htexbnd_files[0], chr_folder, npc_id, replaced_part)
        copy_file(ltexbnd_files[0], chr_folder, npc_id, replaced_part)

    return CopyFileResult.SUCCESS

def clear_files(mod_folder: str):
    mod_folder_path = Path(mod_folder)
    chr_folder = mod_folder_path.joinpath(CHR_FOLDER_NAME)
    if not chr_folder.exists():
        return

    for file in chr_folder.glob("*"):
        file.unlink()

def copy_file(original_path: Path, chr_folder: Path, npc_id: str, existing_id: str):
    shutil.copy(original_path, chr_folder.joinpath(original_path.name.replace(existing_id, npc_id)))
