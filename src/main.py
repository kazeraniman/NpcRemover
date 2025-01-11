from gui.main_window import MainWindow
from src.util import read_id_file

if __name__ == '__main__':
    # Read in the IDs
    id_json = read_id_file()

    # Create the main window
    MainWindow.start(id_json)
