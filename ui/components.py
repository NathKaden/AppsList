import os
import json
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy, QLineEdit, QMenuBar, QMenu, QPushButton, QFileDialog, QColorDialog, QScrollArea, QGraphicsView, QGraphicsScene, QApplication, QMessageBox, QDialog, QFormLayout, QSpinBox, QDoubleSpinBox, QDialogButtonBox
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QAction, QPixmap, QColor, QPainter, QBrush, QPen, QIcon, QPolygonF
from functions.functions import terminal

class LogoLabel(QWidget):
    def __init__(self, image_path, target_w, target_h, parent=None):
        super().__init__(parent)
        self.pix = QPixmap(image_path)
        self.target_w = target_w
        self.target_h = target_h
        self.setFixedSize(target_w, target_h)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(self.rect(), self.pix)


class AppLabel(QLabel):
    def __init__(self, app, launcher, disk, db, refresh_callback, parent=None):
        super().__init__(f'{app.name} ({app.year}) - {app.size} Go', parent)
        self.app = app
        self.launcher = launcher
        self.disk = disk
        self.db = db
        self.refresh_callback = refresh_callback
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("appLabel")
        self.setStyleSheet("""
            QLabel#appLabel {
                padding: 2px 4px;
                border-radius: 3px;
                color: #ffffff;
            }
            QLabel#appLabel:hover {
                background-color: rgba(255, 255, 255, 15);
            }
        """)
        
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #29272b;
                color: #ffffff;
                border: 1px solid dimgrey;
                border-radius: 5px;
                padding: 4px;
            }
            QMenu::item {
                padding: 4px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #59596B;
            }
        """)
        
        modify_action = menu.addAction("Modifier...")
        delete_action = menu.addAction("Supprimer")
        
        action = menu.exec(self.mapToGlobal(pos))
        if action == modify_action:
            self.modify_app()
        elif action == delete_action:
            self.delete_app()

    def delete_app(self):
        reply = QMessageBox.question(
            self,
            "Supprimer l'application",
            f"Êtes-vous sûr de vouloir supprimer '{self.app.name}' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_app_from_launcher(self.app.name, self.launcher.name)
            self.refresh_callback()

    def modify_app(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Modifier {self.app.name}")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #29272b;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #302E33;
                color: white;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
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
            }
        """)
        
        layout = QFormLayout(dialog)
        
        name_input = QLineEdit(self.app.name)
        year_input = QSpinBox()
        year_input.setRange(1900, 2100)
        year_input.setValue(int(self.app.year))
        
        size_input = QDoubleSpinBox()
        size_input.setRange(0.0, 10000.0)
        size_input.setDecimals(1)
        size_input.setValue(float(self.app.size))
        size_input.setSuffix(" Go")
        
        layout.addRow("Nom :", name_input)
        layout.addRow("Année :", year_input)
        layout.addRow("Taille :", size_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name = name_input.text().strip()
            if new_name:
                self.app.name = new_name
                self.app.year = year_input.value()
                self.app.size = size_input.value()
                self.db.save()
                self.refresh_callback()


class DiskWidget(QWidget):
    def __init__(self, disk, index, assetsdir, get_color, launchers_config=None, db=None, refresh_callback=None, parent=None):
        super().__init__(parent)
        self.disk = disk
        self.index = index
        self.assetsdir = assetsdir
        self.get_color = get_color
        self.launchers_config = launchers_config if launchers_config is not None else {}
        self.db = db
        self.refresh_callback = refresh_callback
        self.init_ui()

    def init_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("DiskWidget")
        self.setStyleSheet("""
            QWidget#DiskWidget {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 6px;
            }
        """)
        disk_layout = QHBoxLayout(self)
        disk_layout.setContentsMargins(6, 6, 6, 6)
        disk_layout.setSpacing(10)

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
            disk_logo_label = LogoLabel(image_disque, 25, 25, self)
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
                logo_label = LogoLabel(image_path, 20, 20, self)
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
                app_label = AppLabel(app, launcher, self.disk, self.db, self.refresh_callback, self)
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


class NewBddInputWidget(QLineEdit):
    def __init__(self, assetsdir, on_created_callback, on_close_callback, parent=None):
        super().__init__(parent)
        self.assetsdir = assetsdir
        self.on_created = on_created_callback
        self.on_close = on_close_callback
        self.setPlaceholderText("Nom de la BDD")
        self.returnPressed.connect(self.create_new_bdd)

    def create_new_bdd(self):
        bdd_name = self.text().strip()
        if not bdd_name:
            self.on_close()
            self.deleteLater()
            return
            
        # Sanitize filename: replace non-alphanumeric chars (except _ and -) with underscore
        safe_filename = "".join(c if (c.isalnum() or c in ('_', '-')) else '_' for c in bdd_name).strip()
        while '__' in safe_filename:
            safe_filename = safe_filename.replace('__', '_')
        safe_filename = safe_filename.strip('_')
        
        if not safe_filename:
            safe_filename = "NewBDD"
            
        # Get project dir relative to assets directory
        project_dir = os.path.dirname(self.assetsdir.rstrip('/'))
        bdd_dir = os.path.join(project_dir, "bdd").replace("\\", "/")
        os.makedirs(bdd_dir, exist_ok=True)
        
        new_bdd_path = os.path.join(bdd_dir, f"{safe_filename}.json").replace("\\", "/")
        
        # If the BDD file does not exist, initialize it with empty object
        if not os.path.exists(new_bdd_path):
            initial_data = {}
            with open(new_bdd_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=4)
            
        settings_path = self.assetsdir + "settings.json"
        with open(settings_path, "r", encoding="utf-8") as f:
            settings_data = json.load(f)
            
        rel_path = "bdd/" + os.path.basename(new_bdd_path)
        settings_data["path_bdd"] = rel_path
        
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=2, ensure_ascii=False)
            
        self.on_created(new_bdd_path)
        self.on_close()
        self.deleteLater()


def build_menu_bar(parent, on_exit, on_terminal, on_github, on_new, on_open, on_refresh, settings_button=None):
    menuBar = QMenuBar(parent)
    menuBar.setObjectName("mainMenuBar")
    menuBar.setMouseTracking(True)
    menuBar.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

    fileMenu = QMenu('Fichier', parent)
    fileMenu.setCursor(Qt.CursorShape.PointingHandCursor)
    newAction = QAction('Nouveau', parent)
    newAction.triggered.connect(on_new)
    openAction = QAction('Ouvrir', parent)
    openAction.triggered.connect(on_open)
    refreshAction = QAction('Actualiser', parent)
    refreshAction.triggered.connect(on_refresh)
    exitAction = QAction('Quitter', parent)
    exitAction.triggered.connect(on_exit)
    fileMenu.addAction(newAction)
    fileMenu.addAction(openAction)
    fileMenu.addAction(refreshAction)
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


def create_gear_icon(color=Qt.GlobalColor.white):
    import math
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(color))
    
    center_x, center_y = 16.0, 16.0
    outer_r = 13.0
    inner_r = 9.0
    
    # Draw teeth
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        p1_x = center_x + (outer_r + 2.5) * math.cos(angle - 0.2)
        p1_y = center_y + (outer_r + 2.5) * math.sin(angle - 0.2)
        p2_x = center_x + (outer_r + 2.5) * math.cos(angle + 0.2)
        p2_y = center_y + (outer_r + 2.5) * math.sin(angle + 0.2)
        p3_x = center_x + inner_r * math.cos(angle + 0.4)
        p3_y = center_y + inner_r * math.sin(angle + 0.4)
        p4_x = center_x + inner_r * math.cos(angle - 0.4)
        p4_y = center_y + inner_r * math.sin(angle - 0.4)
        
        polygon = QPolygonF([QPointF(p1_x, p1_y), QPointF(p2_x, p2_y), QPointF(p3_x, p3_y), QPointF(p4_x, p4_y)])
        painter.drawPolygon(polygon)
        
    # Draw outer ring
    painter.drawEllipse(QPointF(center_x, center_y), 11.0, 11.0)
    
    # Draw inner hole cutout
    painter.setBrush(QBrush(Qt.GlobalColor.transparent))
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
    painter.drawEllipse(QPointF(center_x, center_y), 5.0, 5.0)
    
    painter.end()
    return QIcon(pixmap)


def create_home_icon(color=Qt.GlobalColor.white):
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(color))
    
    # Draw roof (triangle)
    roof = QPolygonF([
        QPointF(16.0, 5.0),
        QPointF(4.0, 16.0),
        QPointF(28.0, 16.0)
    ])
    painter.drawPolygon(roof)
    
    # Draw body (rectangle)
    painter.drawRect(7, 16, 18, 12)
    
    # Cutout the door
    painter.setBrush(QBrush(Qt.GlobalColor.transparent))
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
    painter.drawRect(13, 20, 6, 8)
    
    painter.end()
    return QIcon(pixmap)


class CanvasView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Déplacement au clic gauche
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # Masquer les barres de défilement
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Style pour correspondre au thème sombre
        self.setStyleSheet("QGraphicsView { border: none; background-color: transparent; }")

        # Configuration des limites de zoom
        self.zoom_minimum = 0.3  # Dézoomer jusqu'à 30%
        self.zoom_maximum = 3.0  # Zoomer jusqu'à 300%
        self.is_first_show = True

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.is_first_show:
            if self.scene():
                bounds = self.scene().itemsBoundingRect()
                if bounds.isValid() and not bounds.isEmpty():
                    # Align to the top of the canvas vertically, center horizontally
                    view_height = self.viewport().height()
                    top_center = QPointF(bounds.center().x(), bounds.top() + view_height / 2.0)
                    self.centerOn(top_center)
                    self.is_first_show = False

    def wheelEvent(self, event):
        """Gère le zoom avec une borne min et max."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        # 1. Calculer le facteur théorique selon le sens de la molette
        if event.angleDelta().y() > 0:
            facteur_potentiel = zoom_in_factor
        else:
            facteur_potentiel = zoom_out_factor

        # 2. Récupérer le niveau de zoom actuel sur l'axe X (m11 de la matrice de transformation)
        zoom_actuel = self.transform().m11()

        # 3. Calculer le niveau de zoom final si on appliquait le changement
        zoom_futur = zoom_actuel * facteur_potentiel

        # 4. Appliquer le zoom uniquement si on reste dans les limites
        if self.zoom_minimum <= zoom_futur <= self.zoom_maximum:
            self.scale(facteur_potentiel, facteur_potentiel)
