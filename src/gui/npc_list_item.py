from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from src.gui.npc_item import NpcItem


class NpcListItem(QListWidgetItem):
    def __init__(self, npc_item: NpcItem, parent: QListWidget = None):
        super().__init__(parent)
        self.npc_item = npc_item

    def __lt__(self, other: 'NpcListItem'):
        if self.npc_item.name != other.npc_item.name:
            return self.npc_item.name < other.npc_item.name

        if self.npc_item.is_dlc != other.npc_item.is_dlc:
            return not self.npc_item.is_dlc

        return self.npc_item.id < other.npc_item.id
