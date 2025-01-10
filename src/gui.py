import os.path
import re
import sys
import typing

from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QListWidget, QLineEdit, QWidget, \
    QHBoxLayout, QPushButton, QFileDialog, QAbstractItemView, QListWidgetItem


class Gui(QMainWindow):
    def __init__(self, id_json: dict):
        super().__init__()

        self.id_json = id_json

        self.setWindowTitle("NPC Remover")
        self.setMinimumSize(700, 500)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        main_layout.addWidget(QLabel("Mod Engine 2 Mod Folder"))

        folder_select_layout = QHBoxLayout()
        main_layout.addLayout(folder_select_layout)

        self.mod_engine_folder_text = QLineEdit()
        self.mod_engine_folder_text.setReadOnly(True)
        folder_select_layout.addWidget(self.mod_engine_folder_text)

        self.mod_engine_button = QPushButton("Browse")
        self.mod_engine_button.clicked.connect(self.mod_engine_button_clicked)
        folder_select_layout.addWidget(self.mod_engine_button)

        main_layout.addWidget(QLabel("Replaced NPCs"))

        self.replaced_list_box = QListWidget()
        self.replaced_list_box.itemSelectionChanged.connect(self.replaced_list_selected)
        main_layout.addWidget(self.replaced_list_box)

        main_layout.addWidget(QLabel("Available NPCs"))

        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.search_box_changed)
        main_layout.addWidget(self.search_box)

        self.available_list_box = QListWidget()
        self.available_list_box.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.available_list_box.itemSelectionChanged.connect(self.available_list_selected)
        main_layout.addWidget(self.available_list_box)

        for npc in id_json['list']:
            self.add_row_item(self.available_list_box, npc)

        self.available_list_box.sortItems()

    @staticmethod
    def add_row_item(list_widget: QListWidget, npc: dict) -> 'NpcListItem':
        npc_item = NpcItem(npc)
        list_item = NpcListItem(npc_item, list_widget)
        list_item.setSizeHint(npc_item.sizeHint())
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, npc_item)
        return list_item

    def mod_engine_button_clicked(self):
        starting_folder = self.mod_engine_folder_text.text() if self.mod_engine_folder_text.text() else os.path.expanduser(
            '~')
        folder = QFileDialog.getExistingDirectory(self, "Select Mod Engine 2 Mod Folder", directory=starting_folder)
        if not folder:
            return

        self.mod_engine_folder_text.setText(folder)

    @staticmethod
    def swap_list(from_list: QListWidget, to_list: QListWidget):
        current_row = from_list.currentRow()
        from_list.setCurrentRow(-1)
        selected_item = from_list.takeItem(current_row)
        new_item = Gui.add_row_item(to_list, selected_item.npc_item.npc_dict)

        to_list.sortItems()
        from_list.sortItems()

        return new_item

    def available_list_selected(self):
        if self.available_list_box.currentRow() == -1:
            return

        swapped_item = self.swap_list(self.available_list_box, self.replaced_list_box)
        swapped_item.setHidden(False)

    def replaced_list_selected(self):
        if self.replaced_list_box.currentRow() == -1:
            return

        swapped_item = self.swap_list(self.replaced_list_box, self.available_list_box)
        self.set_available_character_hidden(swapped_item)

    def search_box_changed(self):
        for i in range(self.available_list_box.count()):
            current_item = self.available_list_box.item(i)
            self.set_available_character_hidden(current_item)

        self.available_list_box.scrollToTop()

    def set_available_character_hidden(self, item: QListWidgetItem):
        item.setHidden(not re.search(self.search_box.text(), self.available_list_box.itemWidget(item).name, re.IGNORECASE))

    @staticmethod
    def start_gui(id_dict: dict):
        app = QApplication(sys.argv)
        window = Gui(id_dict)
        window.show()
        app.exec()

class NpcItem(QWidget):
    def __init__(self, npc_dict: dict):
        super().__init__()

        self.npc_dict = npc_dict
        self.name = npc_dict['name']
        self.id = npc_dict['id']
        self.tags = npc_dict['tags']

        self.display_name = npc_dict['name']
        if 'sote' in self.tags:
            self.display_name += ' (DLC)'

        layout = QHBoxLayout()
        self.setLayout(layout)

        name_text = QLabel(self.display_name)
        layout.addWidget(name_text, stretch=4)

        id_text = QLabel(self.id)
        layout.addWidget(id_text, stretch=1)

        tag_text = QLabel(', '.join(self.tags))
        layout.addWidget(tag_text, stretch=4)

class NpcListItem(QListWidgetItem):
    def __init__(self, npc_item: NpcItem, parent: QListWidget = None):
        super().__init__(parent)
        self.npc_item = npc_item

    def __lt__(self, other: 'NpcListItem'):
        if self.npc_item.name != other.npc_item.name:
            return self.npc_item.name < other.npc_item.name

        self_is_dlc = 'sote' in self.npc_item.tags
        other_is_dlc = 'sote' in other.npc_item.tags

        if self_is_dlc != other_is_dlc:
            return not self_is_dlc

        return self.npc_item.id < other.npc_item.id
