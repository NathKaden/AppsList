import sys
import os
import json
import webbrowser

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMainWindow, QStatusBar, QLabel, QMenuBar
from PyQt6.QtCore import pyqtSignal, QEvent, Qt

# Import des fonctions nécessaires, des modèles et des composants UI
from functions.functions import getDisques, getNbApps, get_color
from models import Database
from ui.components import DiskWidget, TerminalWidget, build_menu_bar

class MainWindow(QMainWindow):
    changedToDark = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        # Get path relative to the script directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assetsdir = os.path.join(current_dir, "assets").replace("\\", "/") + "/"
        path_settings = self.assetsdir + "settings.json"
        with open(path_settings, "r", encoding='utf-8') as fichiersettings:
            self.settings = json.load(fichiersettings)
            
        # Resolve BDD path to be absolute if it is relative
        if not os.path.isabs(self.settings["path_bdd"]):
            self.settings["path_bdd"] = os.path.abspath(os.path.join(current_dir, self.settings["path_bdd"]))
            
        # Initialize Database model instance
        self.db = Database(self.settings["path_bdd"])
        self.db.load()
        
        self.__initUi()
        self.__applyBDD()
        self.__applyTheme()

    def __initUi(self):
        # Build menu bar using components.py
        menuBar = build_menu_bar(
            parent=self,
            on_exit=self.close,
            on_terminal=self.open_terminal,
            on_github=self.open_github
        )
        self.setMenuBar(menuBar)
        menuBar.installEventFilter(self)
        self.setWindowTitle("AppsList")
        self.setWindowIcon(QIcon(self.assetsdir + 'medias/icon.jpg'))
        self.setGeometry(400, 300, 750, 480)  # (x, y, width, height)

        central_layout = QVBoxLayout()
        centralWidget = QWidget()
        centralWidget.setObjectName("centralWidget")
        centralWidget.setLayout(central_layout)
        self.input_open = False
        self.setCentralWidget(centralWidget)

    def __applyBDD(self):
        # Barre de statut
        statusbar = QStatusBar()
        disques = getDisques(self.db)
        formatted_list = ""
        for index, disque in enumerate(disques):
            if index > 0:
                formatted_list += "   "
            formatted_list += f'<span style="font-weight:900; color: {get_color(index)};">| </span>{disque}'

        list_label = QLabel(f'<html>{formatted_list}</html>')
        list_label.setOpenExternalLinks(True)
        statusbar.addWidget(list_label)
        
        bddnamestr = os.path.splitext(os.path.basename(self.db.filepath))[0]
        r_label = bddnamestr + "  -  " + str(getNbApps(self.db)) + " App(s)"
        right_label = QLabel(r_label)
        statusbar.addPermanentWidget(list_label, 1)
        statusbar.addPermanentWidget(right_label)
        self.setStatusBar(statusbar)

        # Widget central (uses components.py for clean rendering)
        central_layout = QVBoxLayout()

        for index, disk in enumerate(self.db.disks.values()):
            disk_widget = DiskWidget(disk, index, self.assetsdir, get_color, self.settings.get("launchers", {}))
            central_layout.addWidget(disk_widget)

        centralWidget = QWidget()
        centralWidget.setLayout(central_layout)
        centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(centralWidget)

    def refresh(self):
        self.db.load()
        self.__applyBDD()

    def open_github(self):
        webbrowser.open('https://github.com/NathKaden/AppsList')
        print("Github")
        
    def open_terminal(self):
        if not self.input_open:
            self.input = TerminalWidget(
                db=self.db,
                on_success_callback=self.refresh,
                on_close_callback=self._on_terminal_close,
                parent=self
            )
            self.centralWidget().layout().addWidget(self.input)
            self.input.setFocus()
            self.input_open = True  # Marquer le champ de saisie comme ouvert

    def _on_terminal_close(self):
        self.input_open = False

    def eventFilter(self, source, event):
        if isinstance(source, QMenuBar):
            if event.type() in (QEvent.Type.HoverMove, QEvent.Type.HoverEnter, QEvent.Type.MouseMove):
                pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
                action = source.actionAt(pos)
                if action is not None:
                    source.setCursor(Qt.CursorShape.PointingHandCursor)
                    self.setCursor(Qt.CursorShape.PointingHandCursor)
                else:
                    source.setCursor(Qt.CursorShape.ArrowCursor)
                    self.setCursor(Qt.CursorShape.ArrowCursor)
            elif event.type() == QEvent.Type.HoverLeave:
                source.setCursor(Qt.CursorShape.ArrowCursor)
                self.setCursor(Qt.CursorShape.ArrowCursor)
        return super().eventFilter(source, event)

    def __applyTheme(self):
        with open(self.assetsdir+'style.qss', 'r') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

if __name__ == "__main__":
    print("App ouverte")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
