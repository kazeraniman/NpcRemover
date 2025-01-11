import os
import re
import sys

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QListWidget, \
    QAbstractItemView, QFileDialog, QListWidgetItem, QApplication

from src.gui.npc_list_item import NpcListItem
from src.gui.npc_item import NpcItem

MIN_WINDOW_WIDTH = 750
MIN_WINDOW_HEIGHT = 500

WINDOW_TITLE_TEXT = 'NPC Remover'
FOLDER_LABEL_TEXT = 'Mod Engine 2 Mod Folder'
BROWSE_BUTTON_TEXT = 'Browse'
REPLACED_NPC_LABEL_TEXT = 'Replaced NPCs'
AVAILABLE_NPC_LABEL_TEXT = 'Available NPCs'

MOD_FOLDER_SELECT_START_DIRECTORY = '~'
MOD_FOLDER_SELECT_TITLE_TEXT = 'Select Mod Engine 2 Mod Folder'

LIST_KEY = 'list'

DEFAULT_ROW = -1


class MainWindow(QMainWindow):
    def __init__(self, id_json: dict):
        super().__init__()

        self.id_json = id_json

        self.setWindowTitle(WINDOW_TITLE_TEXT)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        main_layout.addWidget(QLabel(FOLDER_LABEL_TEXT))

        folder_select_layout = QHBoxLayout()
        main_layout.addLayout(folder_select_layout)

        self.mod_engine_folder_text = QLineEdit()
        self.mod_engine_folder_text.setReadOnly(True)
        folder_select_layout.addWidget(self.mod_engine_folder_text)

        self.mod_engine_button = QPushButton(BROWSE_BUTTON_TEXT)
        self.mod_engine_button.clicked.connect(self.mod_engine_button_clicked)
        folder_select_layout.addWidget(self.mod_engine_button)

        main_layout.addWidget(QLabel(REPLACED_NPC_LABEL_TEXT))

        self.replaced_list_box = QListWidget()
        self.replaced_list_box.itemSelectionChanged.connect(self.replaced_list_selected)
        main_layout.addWidget(self.replaced_list_box)

        main_layout.addWidget(QLabel(AVAILABLE_NPC_LABEL_TEXT))

        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.search_box_changed)
        main_layout.addWidget(self.search_box)

        self.available_list_box = QListWidget()
        self.available_list_box.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.available_list_box.itemSelectionChanged.connect(self.available_list_selected)
        main_layout.addWidget(self.available_list_box)

        for npc in id_json[LIST_KEY]:
            self.add_row_item(self.available_list_box, npc)

        self.available_list_box.sortItems()

    @staticmethod
    def add_row_item(list_widget: QListWidget, npc: dict) -> NpcListItem:
        npc_item = NpcItem(npc)
        list_item = NpcListItem(npc_item, list_widget)
        list_item.setSizeHint(npc_item.sizeHint())
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, npc_item)
        return list_item

    def mod_engine_button_clicked(self):
        starting_folder = self.mod_engine_folder_text.text() if self.mod_engine_folder_text.text() else os.path.expanduser(
            MOD_FOLDER_SELECT_START_DIRECTORY)
        folder = QFileDialog.getExistingDirectory(self, MOD_FOLDER_SELECT_TITLE_TEXT, directory=starting_folder)
        if not folder:
            return

        self.mod_engine_folder_text.setText(folder)

    @staticmethod
    def swap_list(from_list: QListWidget, to_list: QListWidget):
        current_row = from_list.currentRow()
        from_list.setCurrentRow(-1)
        selected_item = from_list.takeItem(current_row)
        new_item = MainWindow.add_row_item(to_list, selected_item.npc_item.npc_dict)

        to_list.sortItems()
        from_list.sortItems()

        return new_item

    def available_list_selected(self):
        if self.available_list_box.currentRow() == DEFAULT_ROW:
            return

        swapped_item = self.swap_list(self.available_list_box, self.replaced_list_box)
        swapped_item.setHidden(False)

    def replaced_list_selected(self):
        if self.replaced_list_box.currentRow() == DEFAULT_ROW:
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
    def start(id_dict: dict):
        app = QApplication(sys.argv)
        window = MainWindow(id_dict)
        window.show()
        app.exec()
