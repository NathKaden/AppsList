import sys
import os
import json
import webbrowser

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMainWindow, QStatusBar, QLabel, QMenuBar, QStackedWidget, QPushButton, QGraphicsScene, QFileDialog
from PyQt6.QtCore import pyqtSignal, QEvent, Qt, QSize

# Import des fonctions nécessaires, des modèles et des composants UI
from functions.functions import getDisques, getNbApps, get_color
from models import Database
from ui.components import DiskWidget, TerminalWidget, build_menu_bar, SettingsWidget, create_gear_icon, create_home_icon, CanvasView, NewBddInputWidget

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
        # Create settings button
        self.settings_button = QPushButton()
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 4px 8px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 40);
                border-radius: 4px;
            }
        """)
        self.settings_icon = create_gear_icon()
        self.home_icon = create_home_icon()
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.clicked.connect(self.toggle_settings)

        # Build menu bar using components.py
        menuBar = build_menu_bar(
            parent=self,
            on_exit=self.close,
            on_terminal=self.open_terminal,
            on_github=self.open_github,
            on_new=self.open_new_bdd_input,
            on_open=self.open_bdd_file,
            on_refresh=self.refresh,
            settings_button=self.settings_button
        )
        self.setMenuBar(menuBar)
        menuBar.installEventFilter(self)
        self.setWindowTitle("AppsList")
        self.setWindowIcon(QIcon(self.assetsdir + 'medias/icon.jpg'))
        self.setGeometry(400, 300, 750, 480)  # (x, y, width, height)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.stacked_widget)
        self.input_open = False

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

        # Create canvas container for DiskWidgets vertical layout
        self.canvas_container = QWidget()
        self.canvas_container.setObjectName("canvasContainer")
        self.canvas_container.setStyleSheet("background-color: transparent;")
        
        central_layout = QVBoxLayout(self.canvas_container)
        central_layout.setContentsMargins(10, 10, 10, 10)
        central_layout.setSpacing(15)

        for index, disk in enumerate(self.db.disks.values()):
            disk_widget = DiskWidget(
                disk, 
                index, 
                self.assetsdir, 
                get_color, 
                self.settings.get("launchers", {}),
                db=self.db,
                refresh_callback=self.refresh
            )
            central_layout.addWidget(disk_widget)

        # Initialize QGraphicsScene and add canvas_container to it
        self.scene = QGraphicsScene(self)
        self.proxy = self.scene.addWidget(self.canvas_container)

        # Initialize zoomable & pannable QGraphicsView (CanvasView)
        self.canvas_view = CanvasView(self.scene, self)
        
        # Enforce container sizing and bound displacement/panning
        self.canvas_container.setMinimumWidth(730)
        self.canvas_container.setMinimumHeight(410)
        self.canvas_container.adjustSize()
        bounds = self.scene.itemsBoundingRect()
        margin_w = bounds.width() * 0.5
        margin_h = bounds.height() * 0.5
        self.scene.setSceneRect(
            bounds.left() - margin_w,
            bounds.top() - margin_h,
            bounds.width() + 2 * margin_w,
            bounds.height() + 2 * margin_h
        )
        
        # Center initially on the content
        self.canvas_view.centerOn(bounds.center())

        # Main page layout wrapping the QGraphicsView
        main_page_layout = QVBoxLayout()
        main_page_layout.setContentsMargins(0, 0, 0, 0)
        main_page_layout.addWidget(self.canvas_view)

        self.main_page_widget = QWidget()
        self.main_page_widget.setLayout(main_page_layout)
        self.main_page_widget.setObjectName("mainPageWidget")

        if self.stacked_widget.count() > 0:
            old_widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()
            
        self.stacked_widget.insertWidget(0, self.main_page_widget)

        if self.stacked_widget.count() < 2:
            self.settings_widget = SettingsWidget(
                settings_path=self.assetsdir + "settings.json",
                on_save=self.on_settings_saved,
                on_cancel=self.on_settings_cancelled,
                parent=self
            )
            self.stacked_widget.addWidget(self.settings_widget)

        self.stacked_widget.setCurrentIndex(0)
        self.settings_button.setIcon(self.settings_icon)

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
            self.main_page_widget.layout().addWidget(self.input)
            self.input.setFocus()
            self.input_open = True  # Marquer le champ de saisie comme ouvert

    def open_new_bdd_input(self):
        if not self.input_open:
            self.input = NewBddInputWidget(
                assetsdir=self.assetsdir,
                on_created_callback=self.on_new_bdd_created,
                on_close_callback=self._on_terminal_close,
                parent=self
            )
            self.main_page_widget.layout().addWidget(self.input)
            self.input.setFocus()
            self.input_open = True

    def on_new_bdd_created(self, new_bdd_path):
        # Reload settings
        path_settings = self.assetsdir + "settings.json"
        with open(path_settings, "r", encoding='utf-8') as fichiersettings:
            self.settings = json.load(fichiersettings)
            
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isabs(self.settings["path_bdd"]):
            self.settings["path_bdd"] = os.path.abspath(os.path.join(current_dir, self.settings["path_bdd"]))
            
        self.db = Database(self.settings["path_bdd"])
        self.db.load()
        
        # Reset is_first_show flag in CanvasView so that it centers the new BDD list correctly
        self.canvas_view.is_first_show = True
        
        self.refresh()
        
        # Update SettingsWidget fields if initialized
        if hasattr(self, 'settings_widget'):
            self.settings_widget.load_settings()
            self.settings_widget.path_input.setText(self.settings_widget.current_path)

    def open_bdd_file(self):
        initial_dir = os.path.dirname(self.settings["path_bdd"]) if "path_bdd" in self.settings else ""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir la base de données",
            initial_dir,
            "Fichiers JSON (*.json)"
        )
        if file_path:
            # Update settings.json
            path_settings = self.assetsdir + "settings.json"
            with open(path_settings, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            bdd_dir = os.path.join(current_dir, "bdd").replace("\\", "/")
            normalized_file_path = file_path.replace("\\", "/")
            
            # Use relative path if the file is inside the project's bdd/ folder
            if normalized_file_path.startswith(bdd_dir):
                rel_path = "bdd/" + os.path.basename(normalized_file_path)
            else:
                rel_path = normalized_file_path
                
            settings_data["path_bdd"] = rel_path
            
            with open(path_settings, "w", encoding="utf-8") as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)
                
            self.settings = settings_data
            if not os.path.isabs(self.settings["path_bdd"]):
                self.settings["path_bdd"] = os.path.abspath(os.path.join(current_dir, self.settings["path_bdd"]))
                
            self.db = Database(self.settings["path_bdd"])
            self.db.load()
            
            # Update SettingsWidget fields if initialized
            if hasattr(self, 'settings_widget'):
                self.settings_widget.load_settings()
                self.settings_widget.path_input.setText(self.settings_widget.current_path)
                
            self.canvas_view.is_first_show = True
            self.refresh()

    def toggle_settings(self):
        if self.stacked_widget.currentIndex() == 0:
            self.settings_widget.load_settings()
            self.settings_widget.rebuild_colors_list()
            self.settings_widget.path_input.setText(self.settings_widget.current_path)
            self.stacked_widget.setCurrentIndex(1)
            self.settings_button.setIcon(self.home_icon)
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.settings_button.setIcon(self.settings_icon)

    def on_settings_saved(self):
        path_settings = self.assetsdir + "settings.json"
        with open(path_settings, "r", encoding='utf-8') as fichiersettings:
            self.settings = json.load(fichiersettings)
            
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isabs(self.settings["path_bdd"]):
            self.settings["path_bdd"] = os.path.abspath(os.path.join(current_dir, self.settings["path_bdd"]))
            
        self.db = Database(self.settings["path_bdd"])
        self.db.load()
        
        self.__applyBDD()
        self.stacked_widget.setCurrentIndex(0)
        self.settings_button.setIcon(self.settings_icon)

    def on_settings_cancelled(self):
        self.stacked_widget.setCurrentIndex(0)
        self.settings_button.setIcon(self.settings_icon)

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
