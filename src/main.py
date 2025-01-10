import json
import sys

from pathlib import Path

from gui import Gui

RES_FOLDER_PATH = Path(f'{Path(__file__).parent.parent}/res/')
ID_JSON_FILE_PATH = Path.joinpath(RES_FOLDER_PATH, 'ids.json')

if __name__ == '__main__':
    # Read in the IDs
    RES_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
    if ID_JSON_FILE_PATH.exists():
        with open(ID_JSON_FILE_PATH, 'r') as f:
            id_json = json.load(f)
    else:
        print("Could not find the file containing the IDs. Re-download the mod if you have accidentally deleted it.", file=sys.stderr)
        exit(1)

    # Create the main window
    Gui.start_gui(id_json)
