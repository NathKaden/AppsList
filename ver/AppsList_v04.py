import sys
import os
import json
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QLabel, \
    QHBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt

# Import des fonctions nécessaires
from functions.functions import loadBDD, getDisques, getNbApps, get_color


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
        commandAction = QAction('Commande (terminal)', self)
        githubAction = QAction('GitHub', self)
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
        self.setCentralWidget(centralWidget)

    def __applyTheme(self):
        with open('../assets/style.qss', 'r') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def __applyBDD(self):
        path_settings = "../assets/settings.json"
        with open(path_settings, "r", encoding='utf-8') as fichiersettings:
            settings = json.load(fichiersettings)
        path_bdd = settings["path_bdd"]
        BDD = loadBDD(path_bdd)

        # Barre de statut
        statusbar = QStatusBar()
        disques = getDisques(BDD)
        formatted_list = ""
        for index, disque in enumerate(disques):
            if index > 0:
                formatted_list += "   "
            formatted_list += f'<span style="font-weight:900; color: {get_color(index)};">| </span>{disque}'

        list_label = QLabel(f'<html>{formatted_list}</html>')
        list_label.setOpenExternalLinks(True)
        statusbar.addWidget(list_label)
        bddnamestr = os.path.splitext(os.path.basename(path_bdd))[0]
        r_label = bddnamestr + "  -  " + str(getNbApps(BDD)) + " App(s)"
        right_label = QLabel(r_label)
        statusbar.addPermanentWidget(list_label, 1)
        statusbar.addPermanentWidget(right_label)
        self.setStatusBar(statusbar)

        # Widget central
        central_layout = QVBoxLayout()

        for disk_name, launchers in BDD.items():
            disk_layout = QHBoxLayout()
            disk_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges intérieures du disque
            disk_layout.setSpacing(0)  # Aucun espacement entre le nom du disque et les launchers

            # Label pour le nom du disque
            with open("../assets/style.css", "r") as file:
                css = file.read()

            style = f"<style>{css}</style>"
            disk_label = QLabel(f'{style}<b class="disque">{disk_name}</b>')
            disk_label.setObjectName("disque")
            disk_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
            disk_label.adjustSize()
            disk_layout.addWidget(disk_label)


            # Layout pour les launchers à droite
            launchers_layout = QVBoxLayout()
            launchers_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges pour les launchers
            launchers_layout.setSpacing(0)  # Aucun espacement entre les launchers

            for launcher_name, apps_list in launchers.items():
                launcher_layout = QHBoxLayout()
                launcher_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges pour chaque launcher

                launcher_label = QLabel(f'<u>{launcher_name}</u>')
                launcher_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
                launcher_label.setObjectName("disque")
                launcher_layout.addWidget(launcher_label)

                # Layout pour les jeux à droite de chaque launcher
                apps_layout = QVBoxLayout()
                for app in apps_list:
                    game_label = QLabel(f'{app["nom"]} ({app["année"]}) - {app["taille"]} Go')
                    apps_layout.addWidget(game_label)

                launcher_layout.addLayout(apps_layout)
                launchers_layout.addLayout(launcher_layout)

            disk_layout.addLayout(launchers_layout)
            central_layout.addLayout(disk_layout)

        centralWidget = QWidget()
        centralWidget.setLayout(central_layout)
        centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(centralWidget)

if __name__ == "__main__":
    print("Lancement de l'application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
