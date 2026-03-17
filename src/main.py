from gui.main_window import MainWindow
from src.config import Config
from src.util import read_id_file

if __name__ == '__main__':
    # Read in the IDs
    id_json = read_id_file()

    # Prepare the config
    config = Config()

    # Create the main window
    MainWindow.start(id_json, config)
