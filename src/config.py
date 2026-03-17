import configparser
from pathlib import Path

from src.util import RES_FOLDER_PATH, FILE_WRITE_MODE

INI_FILE_PATH = Path.joinpath(RES_FOLDER_PATH, 'config.ini')

CONFIG_BASIC_SECTION = 'Basic'
CONFIG_MOD_FOLDER_OPTION = 'ModFolder'


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(INI_FILE_PATH)

        if not self.config.has_section(CONFIG_BASIC_SECTION):
            self.config[CONFIG_BASIC_SECTION] = {}

        if not self.config.has_option(CONFIG_BASIC_SECTION, CONFIG_MOD_FOLDER_OPTION):
            self.config[CONFIG_BASIC_SECTION][CONFIG_MOD_FOLDER_OPTION] = ''

        self.write_config()

    def write_config(self):
        with open(INI_FILE_PATH, FILE_WRITE_MODE) as f:
            self.config.write(f)

    def get_mod_folder(self):
        return self.config[CONFIG_BASIC_SECTION][CONFIG_MOD_FOLDER_OPTION]

    def set_mod_folder(self, mod_folder):
        if self.config[CONFIG_BASIC_SECTION][CONFIG_MOD_FOLDER_OPTION] == mod_folder:
            return

        self.config[CONFIG_BASIC_SECTION][CONFIG_MOD_FOLDER_OPTION] = mod_folder
        self.write_config()

