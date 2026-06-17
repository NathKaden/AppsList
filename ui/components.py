import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy, QLineEdit, QMenuBar, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
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


def build_menu_bar(parent, on_exit, on_terminal, on_github):
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

    return menuBar
