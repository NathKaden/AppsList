import os
import json
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy, QLineEdit, QMenuBar, QMenu, QPushButton, QFileDialog, QColorDialog, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap, QColor
from functions.functions import terminal

class DiskWidget(QWidget):
    def __init__(self, disk, index, assetsdir, get_color, launchers_config=None, parent=None):
        super().__init__(parent)
        self.disk = disk
        self.index = index
        self.assetsdir = assetsdir
        self.get_color = get_color
        self.launchers_config = launchers_config if launchers_config is not None else {}
        self.init_ui()

    def init_ui(self):
        disk_layout = QHBoxLayout(self)
        disk_layout.setContentsMargins(0, 0, 0, 0)
        disk_layout.setSpacing(0)

        # Determine if it's SSD or HDD
        if 'ssd' in self.disk.name.lower():
            image_disque = self.assetsdir + "medias/ssd.png"
        else:
            image_disque = self.assetsdir + "medias/hdd.png"

        # Create a container widget for the disk header to support custom styling and High-DPI scaling
        disk_header = QWidget()
        disk_header.setObjectName("disque")
        disk_header.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        disk_header.setStyleSheet(f"""
            QWidget#disque {{
                border-right: 3px solid {self.get_color(self.index)} !important;
            }}
        """)
        
        disk_header_layout = QVBoxLayout(disk_header)
        disk_header_layout.setContentsMargins(10, 5, 10, 5)
        disk_header_layout.setSpacing(2)
        disk_header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Top row: Logo and Name (horizontal layout)
        disk_top_row = QWidget()
        disk_top_row_layout = QHBoxLayout(disk_top_row)
        disk_top_row_layout.setContentsMargins(0, 0, 0, 0)
        disk_top_row_layout.setSpacing(5)
        disk_top_row_layout.addStretch()
        
        if os.path.exists(image_disque):
            pixmap = QPixmap(image_disque)
            dpr = self.devicePixelRatioF()
            target_w = int(25 * dpr)
            target_h = int(25 * dpr)
            scaled_pixmap = pixmap.scaled(
                target_w, target_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            scaled_pixmap.setDevicePixelRatio(dpr)
            
            disk_logo_label = QLabel()
            disk_logo_label.setPixmap(scaled_pixmap)
            disk_logo_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            disk_top_row_layout.addWidget(disk_logo_label)

        disk_text_label = QLabel(f'<b>{self.disk.name}</b>')
        disk_text_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        disk_top_row_layout.addWidget(disk_text_label)
        
        disk_header_layout.addWidget(disk_top_row)
        
        # Bottom row: Total size in Go (in grey)
        total_disk_size = sum(float(app.size) for launcher in self.disk.launchers.values() for app in launcher.apps)
        disk_size_label = QLabel(f'<span style="font-size: 12px; color: grey;">{total_disk_size:.1f} Go</span>')
        disk_size_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        disk_size_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        disk_header_layout.addWidget(disk_size_label, 0, Qt.AlignmentFlag.AlignRight)
        
        disk_layout.addWidget(disk_header)

        launchers_layout = QVBoxLayout()
        launchers_layout.setContentsMargins(0, 0, 0, 0)
        launchers_layout.setSpacing(0)

        for launcher_name, launcher in self.disk.launchers.items():
            launcher_layout = QHBoxLayout()
            launcher_layout.setContentsMargins(0, 0, 0, 0)
            launcher_layout.setSpacing(15)

            launcher_data = self.launchers_config.get(launcher_name, {})
            launcher_color = launcher_data.get("color", "lightgrey")
            launcher_style = f"""
                QWidget#disque {{
                    border-right: 3px solid {launcher_color} !important;
                }}
                QLabel {{
                    color: {launcher_color};
                }}
            """
            
            launcher_image = launcher_data.get("image", "")
            image_path = self.assetsdir + "medias/launchers/" + launcher_image if launcher_image else ""
            
            header_widget = QWidget()
            header_widget.setObjectName("disque")
            header_widget.setStyleSheet(launcher_style)
            header_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
            
            header_layout = QVBoxLayout(header_widget)
            header_layout.setContentsMargins(10, 5, 10, 5)
            header_layout.setSpacing(2)
            header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            
            # Top row: Logo and Name (horizontal layout)
            launcher_top_row = QWidget()
            launcher_top_row_layout = QHBoxLayout(launcher_top_row)
            launcher_top_row_layout.setContentsMargins(0, 0, 0, 0)
            launcher_top_row_layout.setSpacing(5)
            
            if image_path and os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                dpr = self.devicePixelRatioF()
                target_w = int(20 * dpr)
                target_h = int(20 * dpr)
                scaled_pixmap = pixmap.scaled(
                    target_w, target_h, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
                scaled_pixmap.setDevicePixelRatio(dpr)
                logo_label = QLabel()
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                launcher_top_row_layout.addWidget(logo_label)
                
            text_label = QLabel(f'<b>{launcher_name}</b>')
            text_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            launcher_top_row_layout.addWidget(text_label)
            
            header_layout.addWidget(launcher_top_row)
            
            # Bottom row: Total size in Go (in grey)
            total_launcher_size = sum(float(app.size) for app in launcher.apps)
            launcher_size_label = QLabel(f'<span style="font-size: 12px; color: grey;">{total_launcher_size:.1f} Go</span>')
            launcher_size_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            launcher_size_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            header_layout.addWidget(launcher_size_label, 0, Qt.AlignmentFlag.AlignRight)
            
            launcher_layout.addWidget(header_widget)

            apps_layout = QVBoxLayout()
            for app in launcher.apps:
                app_label = QLabel(f'{app.name} ({app.year}) - {app.size} Go')
                apps_layout.addWidget(app_label)

            launcher_layout.addLayout(apps_layout)
            launchers_layout.addLayout(launcher_layout)

        disk_layout.addLayout(launchers_layout)


class TerminalWidget(QLineEdit):
    def __init__(self, db, on_success_callback, on_close_callback, parent=None):
        super().__init__(parent)
        self.db = db
        self.on_success = on_success_callback
        self.on_close = on_close_callback
        self.returnPressed.connect(self.execute_command)

    def execute_command(self):
        text = self.text()
        result = terminal(text, self.db, self.db.filepath)
        print(result)
        if "succès" in result.lower():
            self.on_success()
        self.on_close()
        self.deleteLater()


def build_menu_bar(parent, on_exit, on_terminal, on_github, settings_button=None):
    menuBar = QMenuBar(parent)
    menuBar.setObjectName("mainMenuBar")
    menuBar.setMouseTracking(True)
    menuBar.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

    fileMenu = QMenu('Fichier', parent)
    fileMenu.setCursor(Qt.CursorShape.PointingHandCursor)
    newAction = QAction('Nouveau', parent)
    openAction = QAction('Ouvrir', parent)
    saveAction = QAction('Enregistrer', parent)
    exitAction = QAction('Quitter', parent)
    exitAction.triggered.connect(on_exit)
    fileMenu.addAction(newAction)
    fileMenu.addAction(openAction)
    fileMenu.addAction(saveAction)
    fileMenu.addAction(exitAction)

    editMenu = QMenu('Editer', parent)
    editMenu.setCursor(Qt.CursorShape.PointingHandCursor)
    cutAction = QAction('Couper', parent)
    copyAction = QAction('Copier', parent)
    pasteAction = QAction('Coller', parent)
    editMenu.addAction(cutAction)
    editMenu.addAction(copyAction)
    editMenu.addAction(pasteAction)

    viewMenu = QMenu('Vue', parent)
    viewMenu.setCursor(Qt.CursorShape.PointingHandCursor)
    listAction = QAction('Liste', parent)
    sortAction = QAction('Trier', parent)
    themeAction = QAction('Thèmes', parent)
    languageAction = QAction('Langue', parent)
    viewMenu.addAction(listAction)
    viewMenu.addAction(sortAction)
    viewMenu.addAction(themeAction)
    viewMenu.addAction(languageAction)

    otherMenu = QMenu('Autres', parent)
    otherMenu.setCursor(Qt.CursorShape.PointingHandCursor)
    commandAction = QAction('Terminal', parent)
    commandAction.setStatusTip('  Ouvrir le Terminal')
    commandAction.triggered.connect(on_terminal)
    githubAction = QAction('GitHub', parent)
    githubAction.setStatusTip('  Ouvrir le GitHub')
    githubAction.triggered.connect(on_github)
    creditsAction = QAction('Crédits', parent)
    otherMenu.addAction(commandAction)
    otherMenu.addAction(githubAction)
    otherMenu.addAction(creditsAction)

    menuBar.addMenu(fileMenu)
    menuBar.addMenu(editMenu)
    menuBar.addMenu(viewMenu)
    menuBar.addMenu(otherMenu)

    if settings_button is not None:
        menuBar.setCornerWidget(settings_button, Qt.Corner.TopRightCorner)

    return menuBar


class SettingsWidget(QWidget):
    def __init__(self, settings_path, on_save, on_cancel, parent=None):
        super().__init__(parent)
        self.settings_path = settings_path
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.load_settings()
        self.init_ui()

    def load_settings(self):
        with open(self.settings_path, "r", encoding='utf-8') as f:
            self.settings_data = json.load(f)
        self.current_colors = list(self.settings_data.get("colors", []))
        self.current_path = self.settings_data.get("path_bdd", "")

    def init_ui(self):
        # Apply stylesheet to match the premium dark theme
        self.setStyleSheet("""
            QWidget#settingsWidget {
                background-color: #29272b;
            }
            QLabel {
                font-size: 14px;
                color: #e0e0e0;
            }
            QLabel#settingsTitle {
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
            }
            QLabel#sectionHeader {
                font-size: 15px;
                font-weight: bold;
                color: #b4b4ee;
            }
            QPushButton {
                background-color: #3b3b54;
                border: 1px solid #59596B;
                border-radius: 4px;
                padding: 6px 12px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4c4c6d;
                border-color: #727293;
            }
            QPushButton:pressed {
                background-color: #29272b;
            }
            QPushButton#saveBtn {
                background-color: #4a8a4a;
                border-color: #5fa85f;
            }
            QPushButton#saveBtn:hover {
                background-color: #58a258;
            }
            QPushButton#cancelBtn {
                background-color: #a33838;
                border-color: #c74848;
            }
            QPushButton#cancelBtn:hover {
                background-color: #bd4242;
            }
            QScrollArea {
                border: 1px solid #3b3b54;
                background-color: #211f22;
                border-radius: 4px;
            }
        """)

        self.setObjectName("settingsWidget")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        # Title
        title_label = QLabel("Paramètres de l'Application")
        title_label.setObjectName("settingsTitle")
        main_layout.addWidget(title_label)

        # Separator line
        sep = QWidget()
        sep.setFixedHeight(2)
        sep.setStyleSheet("background-color: #3b3b54;")
        main_layout.addWidget(sep)

        # 1. BDD Path Section
        path_label = QLabel("<b>Base de données</b> (fichier JSON) :")
        main_layout.addWidget(path_label)

        path_row = QHBoxLayout()
        self.path_input = QLineEdit(self.current_path)
        self.path_input.setPlaceholderText("Sélectionnez le fichier JSON de la BDD...")
        browse_btn = QPushButton("Parcourir...")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_db_path)
        path_row.addWidget(self.path_input)
        path_row.addWidget(browse_btn)
        main_layout.addLayout(path_row)

        # 2. Colors Section
        colors_label = QLabel("<b>Couleurs des bordures de disques :</b>")
        main_layout.addWidget(colors_label)

        # Colors Scroll Area with fixed height to prevent window growth
        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedHeight(120)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background-color: #211f22;")
        self.colors_layout = QVBoxLayout(self.scroll_widget)
        self.colors_layout.setContentsMargins(5, 5, 5, 5)
        self.colors_layout.setSpacing(4)
        
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)

        # Add Color Button
        add_color_btn = QPushButton("Ajouter une couleur")
        add_color_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_color_btn.clicked.connect(self.add_color)
        main_layout.addWidget(add_color_btn)

        # 3. Save / Cancel Buttons Row
        actions_row = QHBoxLayout()
        actions_row.addStretch()
        
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.on_cancel)
        
        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        
        actions_row.addWidget(self.cancel_btn)
        actions_row.addWidget(self.save_btn)
        main_layout.addLayout(actions_row)

        # Initial colors list render
        self.rebuild_colors_list()

    def rebuild_colors_list(self):
        # Clear existing items
        while self.colors_layout.count():
            item = self.colors_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Add current colors
        for index, color in enumerate(self.current_colors):
            color_item = QWidget()
            color_item.setObjectName("colorItem")
            color_item.setStyleSheet("""
                QWidget#colorItem {
                    background-color: #2e2b2f;
                    border-radius: 4px;
                }
            """)
            h_layout = QHBoxLayout(color_item)
            h_layout.setContentsMargins(8, 4, 8, 4)
            h_layout.setSpacing(10)
            
            # Color indicator preview
            circle = QLabel()
            circle.setFixedSize(20, 20)
            circle.setStyleSheet(f"""
                background-color: {color};
                border-radius: 10px;
                border: 1px solid #555555;
            """)
            
            # Color label name
            name_label = QLabel(color)
            name_label.setStyleSheet("font-family: Consolas; font-size: 13px; color: #ffffff;")
            
            # Delete button
            del_btn = QPushButton("Supprimer")
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.setFixedSize(90, 26)
            del_btn.setStyleSheet("""
                QPushButton {
                    background-color: #594343;
                    border: 1px solid #7a5c5c;
                    font-size: 12px;
                    padding: 2px;
                }
                QPushButton:hover {
                    background-color: #705252;
                }
            """)
            del_btn.clicked.connect(lambda checked, idx=index: self.delete_color(idx))
            
            h_layout.addWidget(circle)
            h_layout.addWidget(name_label)
            h_layout.addStretch()
            h_layout.addWidget(del_btn)
            
            self.colors_layout.addWidget(color_item)
            
        self.colors_layout.addStretch()

    def delete_color(self, idx):
        if 0 <= idx < len(self.current_colors):
            self.current_colors.pop(idx)
            self.rebuild_colors_list()

    def add_color(self):
        color = QColorDialog.getColor(parent=self)
        if color.isValid():
            self.current_colors.append(color.name())
            self.rebuild_colors_list()

    def browse_db_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir la base de données",
            os.path.dirname(self.path_input.text()) if self.path_input.text() else "",
            "Fichiers JSON (*.json)"
        )
        if file_path:
            self.path_input.setText(file_path)

    def save_settings(self):
        self.settings_data["path_bdd"] = self.path_input.text()
        self.settings_data["colors"] = self.current_colors
        with open(self.settings_path, "w", encoding='utf-8') as f:
            json.dump(self.settings_data, f, indent=2, ensure_ascii=False)
        self.on_save()
