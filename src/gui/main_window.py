import os
import re
import sys
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QListWidget, \
    QAbstractItemView, QFileDialog, QListWidgetItem, QApplication, QMessageBox, QStyle

from src.config import Config
from src.gui.npc_item import NpcItem
from src.gui.npc_list_item import NpcListItem
from src.util import copy_files, CopyFileResult, clear_files

MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600
BUTTON_WIDTH = 150

WINDOW_TITLE_TEXT = 'NPC Remover'
FOLDER_LABEL_TEXT = 'Mod Engine 2 Mod Folder'
BROWSE_BUTTON_TEXT = 'Browse'
COPY_BUTTON_TEXT = 'Replace NPCs'
DELETE_BUTTON_TEXT = 'Clear Folder'
CLEAR_BUTTON_TEXT = 'Clear Selection'
REPLACED_NPC_LABEL_TEXT = 'Replaced NPCs'
AVAILABLE_NPC_LABEL_TEXT = 'Available NPCs'

MOD_FOLDER_SELECT_START_DIRECTORY = '~'
MOD_FOLDER_SELECT_TITLE_TEXT = 'Select Mod Engine 2 Mod Folder'
MOD_FOLDER_REQUIRED_NAME = 'mod'
MOD_FOLDER_REQUIRED_NAME_TITLE = 'Must Select Mod Folder'
MOD_FOLDER_REQUIRED_NAME_BODY = 'The folder you chose is not called "mod". You must select the "mod" folder from Mod Engine 2.'
REPLACE_NPC_NO_SELECTION_TITLE = 'No NPCs Selected'
REPLACE_NPC_NO_SELECTION_BODY = 'Select some NPCs and then try again.'
REPLACE_NPC_CONFIRMATION_TITLE = 'Replace NPCs'
REPLACE_NPC_CONFIRMATION_BODY = 'Are you sure you wish to replace the selected NPCs?'
REPLACE_NPC_SUCCESS_TITLE = 'NPCs Replaced'
REPLACE_NPC_SUCCESS_BODY = 'The selected NPCs have been replaced.'
REPLACE_NPC_ERROR_TITLE = 'Replacement Files Incorrect'
REPLACE_NPC_ERROR_BODY = 'There should be one and only one of each file type in the res folder, and they should have matching names.\nPlease make sure you only have one of each of the following files with the same name in the res folder: anibnd.dcx, chrbnd.dcx, _h.texbnd.dcx, _l.texbnd.dcx.\nFor example, if you have a file called turtle.anibnd.dcx, the other files should be called turtle.chrbnd.dcx, turtle_h.texbnd.dcx, and turtle_l.texbnd.dcx. If you need help, try re-downloading the mod which comes with these files pre-set.'
CLEAR_FOLDER_CONFIRMATION_TITLE = 'Clear Folder'
CLEAR_FOLDER_CONFIRMATION_BODY = 'WARNING: This action will also remove mods which are not managed by this application. Are you sure you wish to clear the character mod folder?'
CLEAR_FOLDER_SUCCESS_TITLE = 'Folder Cleared'
CLEAR_FOLDER_SUCCESS_BODY = 'The character mod folder has been cleared.'

LIST_KEY = 'list'

DEFAULT_ROW = -1


class MainWindow(QMainWindow):
    def __init__(self, id_json: dict, config: Config):
        super().__init__()

        self.id_json = id_json
        self.config = config

        self.setWindowTitle(WINDOW_TITLE_TEXT)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        main_layout.addWidget(QLabel(FOLDER_LABEL_TEXT))

        folder_select_layout = QHBoxLayout()
        main_layout.addLayout(folder_select_layout)

        self.mod_engine_folder_text = QLineEdit(self.config.get_mod_folder())
        self.mod_engine_folder_text.setDisabled(True)
        folder_select_layout.addWidget(self.mod_engine_folder_text)

        self.mod_engine_button = QPushButton(BROWSE_BUTTON_TEXT)
        self.mod_engine_button.clicked.connect(self.mod_engine_button_clicked)
        folder_select_layout.addWidget(self.mod_engine_button)

        main_layout.addWidget(QLabel(REPLACED_NPC_LABEL_TEXT))

        self.replaced_list_box = QListWidget()
        self.replaced_list_box.itemSelectionChanged.connect(self.replaced_list_selected)
        main_layout.addWidget(self.replaced_list_box)

        clear_selection_layout = QHBoxLayout()
        main_layout.addLayout(clear_selection_layout)
        clear_selection_button = QPushButton(CLEAR_BUTTON_TEXT)
        clear_selection_button.clicked.connect(self.clear_button_clicked)
        clear_selection_button.setFixedWidth(BUTTON_WIDTH)
        clear_selection_layout.addWidget(clear_selection_button)

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

        bottom_action_button_layout = QHBoxLayout()
        main_layout.addLayout(bottom_action_button_layout)

        delete_button = QPushButton(DELETE_BUTTON_TEXT)
        delete_button.clicked.connect(self.delete_button_clicked)
        delete_button.setFixedWidth(BUTTON_WIDTH)
        bottom_action_button_layout.addWidget(delete_button)

        copy_button = QPushButton(COPY_BUTTON_TEXT)
        copy_button.clicked.connect(self.copy_button_clicked)
        copy_button.setFixedWidth(BUTTON_WIDTH)
        bottom_action_button_layout.addWidget(copy_button)

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

        if Path(folder).name != MOD_FOLDER_REQUIRED_NAME:
            self.show_message_box(MOD_FOLDER_REQUIRED_NAME_TITLE, MOD_FOLDER_REQUIRED_NAME_BODY)
            return

        self.config.set_mod_folder(folder)
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

    def show_message_box(self, title: str, body: str, buttons: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok, default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok) -> QMessageBox.StandardButton:
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(body)
        message_box.setStandardButtons(buttons)
        message_box.setDefaultButton(default_button)
        message_box.setWindowIcon(message_box.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        return message_box.exec()

    def copy_button_clicked(self):
        ids_to_replace = [self.replaced_list_box.item(x).npc_item.id for x in range(self.replaced_list_box.count())]
        if len(ids_to_replace) == 0:
            self.show_message_box(REPLACE_NPC_NO_SELECTION_TITLE, REPLACE_NPC_NO_SELECTION_BODY)
            return

        should_replace = self.show_message_box(REPLACE_NPC_CONFIRMATION_TITLE, REPLACE_NPC_CONFIRMATION_BODY, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.Yes)
        if should_replace != QMessageBox.StandardButton.Yes:
            return

        copy_result = copy_files(ids_to_replace, self.mod_engine_folder_text.text())
        if copy_result == CopyFileResult.SUCCESS:
            self.show_message_box(REPLACE_NPC_SUCCESS_TITLE, REPLACE_NPC_SUCCESS_BODY)
            return

        if copy_result == CopyFileResult.ERROR:
            self.show_message_box(REPLACE_NPC_ERROR_TITLE, REPLACE_NPC_ERROR_BODY)

    def delete_button_clicked(self):
        should_clear = self.show_message_box(CLEAR_FOLDER_CONFIRMATION_TITLE, CLEAR_FOLDER_CONFIRMATION_BODY, QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.Yes)
        if should_clear != QMessageBox.StandardButton.Yes:
            return

        clear_files(self.mod_engine_folder_text.text())
        self.show_message_box(CLEAR_FOLDER_SUCCESS_TITLE, CLEAR_FOLDER_SUCCESS_BODY)

    def clear_button_clicked(self):
        self.replaced_list_box.clear()

    @staticmethod
    def start(id_dict: dict, config: Config):
        app = QApplication(sys.argv)
        window = MainWindow(id_dict, config)
        window.show()
        app.exec()
