import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtCore import QRect
from main_gui import *
from search_ui import * 
from config import *
from utils import resource_path


MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 600

SEARCH_WINDOW_WIDTH = 1200
SEARCH_WINDOW_HEIGHT = 860

def on_found(path, start_index):
    if not search_window.isVisible():
        return False
    else:
        with open(path, "r", encoding="UTF-8") as f:
            search_window.ui.addCodeEditor(f.read(), start_index, path)
    
        return True
    

def search():
    global search_window, search_thread

    if ui.textEdit.toPlainText() != "":
        #MainWindow.showMinimized()
        
        screen = QDesktopWidget().screenGeometry()
        search_window = SearchWindow(MainWindow, "CodeSleuth", "images/icon.png", QRect(screen.width()//2-SEARCH_WINDOW_WIDTH//2, screen.height()//2-SEARCH_WINDOW_HEIGHT//2+20, SEARCH_WINDOW_WIDTH, SEARCH_WINDOW_HEIGHT))
        search_window.show()
    
        extension = ui.comboBox.currentText()
        if extension == "any":
            extension = None
        elif extension == ".cpp":
            extension = [extension, ".h", ".hpp"]
        elif extension == ".c":
            extension = [extension, ".h"]
        else:
            extension = [extension]

        search_thread = SearchThread(Ui_MainWindow.search_paths, Ui_MainWindow.search_exeption_paths, ui.textEdit.toPlainText(), extension, get_search_limits())
        search_thread.found_signal.connect(on_found)
        search_thread.start()

def main():
    global app, MainWindow, ui
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    ui = Ui_MainWindow()

    screen = QDesktopWidget().screenGeometry()
    ui.setupUi(MainWindow, "CodeSleuth", resource_path("icon.png"), QRect(screen.width()//2-MAIN_WINDOW_WIDTH//2, screen.height()//2-MAIN_WINDOW_HEIGHT//2, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT))

    ui.pushButton.clicked.connect(search)

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
