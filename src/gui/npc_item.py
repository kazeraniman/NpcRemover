from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from src.util import open_wiki

NAME_KEY = 'name'
ID_KEY = 'id'
TAGS_KEY = 'tags'
DLC_TAG = 'sote'

WIKI_URL = 'https://eldenring.wiki.gg/wiki/Special:Search?{0}&go=Go&ns0=1'
SEARCH_QUERY_PARAM = 'search'

DLC_NAME_SUFFIX = ' (DLC)'
INFO_BUTTON_TEXT = 'Info'
TAG_SEPARATOR = ', '

SMALL_COLUMN_STRETCH = 1
LARGE_COLUMN_STRETCH = 4


class NpcItem(QWidget):
    def __init__(self, npc_dict: dict):
        super().__init__()

        self.npc_dict = npc_dict
        self.name = npc_dict[NAME_KEY]
        self.id = npc_dict[ID_KEY]
        self.tags = npc_dict[TAGS_KEY]
        self.is_dlc = DLC_TAG in self.tags

        self.display_name = npc_dict[NAME_KEY]
        if self.is_dlc:
            self.display_name += DLC_NAME_SUFFIX

        layout = QHBoxLayout()
        self.setLayout(layout)

        name_text = QLabel(self.display_name)
        layout.addWidget(name_text, stretch=LARGE_COLUMN_STRETCH)

        id_text = QLabel(self.id)
        layout.addWidget(id_text, stretch=SMALL_COLUMN_STRETCH)

        tag_text = QLabel(TAG_SEPARATOR.join(self.tags))
        layout.addWidget(tag_text, stretch=LARGE_COLUMN_STRETCH)

        info_button = QPushButton(INFO_BUTTON_TEXT)
        info_button.clicked.connect(self.info_button_clicked)
        layout.addWidget(info_button, stretch=SMALL_COLUMN_STRETCH)

    def info_button_clicked(self):
        open_wiki(self.name)
