import sys
import os
import json
import webbrowser

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QLabel, \
    QHBoxLayout, QSizePolicy, QLineEdit
from PyQt6.QtCore import pyqtSignal, Qt

# Import des fonctions nécessaires
from functions.functions import *

class MainWindow(QMainWindow):
    changedToDark = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__initUi()
        self.__applyBDD()
        self.__applyTheme()

    def __initUi(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        self.setWindowTitle("AppsList")
        self.setWindowIcon(QIcon('../assets/icon.jpg'))
        self.setGeometry(400, 300, 750, 480)  # (x, y, width, height)

        fileMenu = QMenu('Fichier', self)
        newAction = QAction('Nouveau', self)
        openAction = QAction('Ouvrir', self)
        saveAction = QAction('Enregistrer', self)
        exitAction = QAction('Quitter', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        editMenu = QMenu('Editer', self)
        cutAction = QAction('Couper', self)
        copyAction = QAction('Copier', self)
        pasteAction = QAction('Coller', self)
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)

        viewMenu = QMenu('Vue', self)
        listAction = QAction('Liste', self)
        sortAction = QAction('Trier', self)
        themeAction = QAction('Thèmes', self)
        languageAction = QAction('Langue', self)
        viewMenu.addAction(listAction)
        viewMenu.addAction(sortAction)
        viewMenu.addAction(themeAction)
        viewMenu.addAction(languageAction)

        otherMenu = QMenu('Autres', self)
        commandAction = QAction('Terminal', self)
        commandAction.setStatusTip('  Ouvrir le Terminal')
        commandAction.triggered.connect(self.open_terminal)
        githubAction = QAction('GitHub', self)
        githubAction.setStatusTip('  Ouvrir le GitHub')
        githubAction.triggered.connect(self.open_github)
        creditsAction = QAction('Crédits', self)
        otherMenu.addAction(commandAction)
        otherMenu.addAction(githubAction)
        otherMenu.addAction(creditsAction)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(viewMenu)
        menuBar.addMenu(otherMenu)

        central_layout = QVBoxLayout()
        centralWidget = QWidget()
        centralWidget.setObjectName("centralWidget")
        centralWidget.setLayout(central_layout)
        self.input_open = False
        self.setCentralWidget(centralWidget)

    def __applyBDD(self):
        path_settings = "../assets/settings.json"
        with open(path_settings, "r", encoding='utf-8') as fichiersettings:
            self.settings = json.load(fichiersettings)
        path_bdd = self.settings["path_bdd"]
        self.BDD = loadBDD(path_bdd)

        # Barre de statut
        statusbar = QStatusBar()
        disques = getDisques(self.BDD)
        formatted_list = ""
        for index, disque in enumerate(disques):
            if index > 0:
                formatted_list += "   "
            formatted_list += f'<span style="font-weight:900; color: {get_color(index)};">| </span>{disque}'

        list_label = QLabel(f'<html>{formatted_list}</html>')
        list_label.setOpenExternalLinks(True)
        statusbar.addWidget(list_label)
        bddnamestr = os.path.splitext(os.path.basename(path_bdd))[0]
        r_label = bddnamestr + "  -  " + str(getNbApps(self.BDD)) + " App(s)"
        right_label = QLabel(r_label)
        statusbar.addPermanentWidget(list_label, 1)
        statusbar.addPermanentWidget(right_label)
        self.setStatusBar(statusbar)

        # Widget central
        central_layout = QVBoxLayout()

        for index, (disk_name, launchers) in enumerate(self.BDD.items()):
            disk_layout = QHBoxLayout()
            disk_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges intérieures du disque
            disk_layout.setSpacing(0)  # Aucun espacement entre le nom du disque et les launchers

            # Charger le CSS depuis le fichier
            with open("../assets/style.css", "r") as file:
                css = file.read()

            # Obtenir la couleur pour la bordure


            # Créer le style dynamique avec la couleur de bordure droite
            style = f"<style>{css}</style>"
            disk_label = QLabel(f'{style}<b>💽 {disk_name}</b>')
            disk_label.setObjectName("disque")
            disk_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
            disk_label.adjustSize()
            disk_label.setStyleSheet(f"""
        QLabel#disque {{
            border-right: 3px solid {get_color(index)} !important;
        }}
    """)
            disk_layout.addWidget(disk_label)

            launcher_styles = {
                "Epic Games": "color: white;",
                "Steam": "color: #8aa5bf;",
                "Battle.net": "color: #8ac7ff;",
                "EA": "color: #ffa3a3;",
                # Ajoutez d'autres styles pour d'autres launchers si nécessaire
            }

            default_style = "color: lightgrey;"

            launchers_layout = QVBoxLayout()
            launchers_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges pour les launchers
            launchers_layout.setSpacing(0)  # Aucun espacement entre les launchers

            for launcher_name, apps_list in launchers.items():
                launcher_layout = QHBoxLayout()
                launcher_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges pour chaque launcher

                launcher_style = launcher_styles.get(launcher_name, default_style)
                launcher_label = QLabel(f'<b>{launcher_name}</b>')
                launcher_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
                launcher_label.setObjectName("disque")
                launcher_label.setStyleSheet(launcher_style)
                launcher_layout.addWidget(launcher_label)

                # Layout pour les jeux à droite de chaque launcher
                apps_layout = QVBoxLayout()
                for app in apps_list:
                    app_label = QLabel(f'{app["nom"]} ({app["année"]}) - {app["taille"]} Go')
                    apps_layout.addWidget(app_label)

                launcher_layout.addLayout(apps_layout)
                launchers_layout.addLayout(launcher_layout)

            disk_layout.addLayout(launchers_layout)
            central_layout.addLayout(disk_layout)

        centralWidget = QWidget()
        centralWidget.setLayout(central_layout)
        centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(centralWidget)

    def open_github(self):
        webbrowser.open('https://github.com/NathKaden/AppsList')
        print("Github")
    def open_terminal(self):
        if not self.input_open:
            self.input = QLineEdit(self)
            self.input.returnPressed.connect(self.print_text)
            self.centralWidget().layout().addWidget(self.input)
            self.input.setFocus()
            self.input_open = True  # Marquer le champ de saisie comme ouvert

    def print_text(self):
        text = self.input.text()
        print(terminal(text, self.BDD))
        print("terminal exit")
        self.input.deleteLater()  # Supprimer le champ de saisie
        self.input_open = False  # Marquer le champ de saisie comme fermé

    def __applyTheme(self):
        with open('../assets/style.qss', 'r') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

if __name__ == "__main__":
    print("App ouverte")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
