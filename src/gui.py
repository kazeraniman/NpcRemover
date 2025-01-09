import os.path
import re
import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QListWidget, QLineEdit, QWidget, \
    QHBoxLayout, QPushButton, QFileDialog, QAbstractItemView, QListWidgetItem


class Gui(QMainWindow):
    def __init__(self, id_dict: dict):
        super().__init__()

        self.id_dict = id_dict

        self.setWindowTitle("NPC Remover")
        self.setMinimumSize(600, 500)

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
        self.available_list_box.setSortingEnabled(True)
        self.available_list_box.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.available_list_box.itemSelectionChanged.connect(self.available_list_selected)
        main_layout.addWidget(self.available_list_box)

        for k, v in id_dict.items():
            self.available_list_box.addItem(f'{v} [{k}]')

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
        from_list.removeItemWidget(selected_item)
        to_list.addItem(selected_item)
        return selected_item

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

    def set_available_character_hidden(self, item: QListWidgetItem):
        item.setHidden(not re.search(self.search_box.text(), item.text(), re.IGNORECASE))

    @staticmethod
    def start_gui(id_dict: dict):
        app = QApplication(sys.argv)
        window = Gui(id_dict)
        window.show()
        app.exec()
