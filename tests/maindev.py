import sys
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

# Exemple de données
disques = {
    "SSD main": {
        "Epic Games": [
            {
                "nom": "RL",
                "taille": 26.2,
                "année": 2015
            }
        ],
        "Steam": [
            {
                "nom": "Ratchet",
                "taille": 39.3,
                "année": 2023
            },
            {
                "nom": "Portal Source_Unpack",
                "taille": 9.5,
                "année": 2007
            }
        ]
    },
    "SSD Sam": {
        "Battle.net": [
            {
                "nom": "Modern Warfare",
                "année": 2019,
                "taille": 150
            }
        ],
        "EA": [
            {
                "nom": "NFS : The Run",
                "année": 2011,
                "taille": 15.4
            },
            {
                "nom": "NFS : Payback",
                "année": 2017,
                "taille": 27.9
            }
        ]
    }
}

class MainWindow(QMainWindow):
    changedToDark = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__initUi()
        self.__applyTheme()
        self.__populateDisks()

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

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)  # Marges extérieures

    def __applyTheme(self):
        with open('../assets/style.qss', 'r') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def __populateDisks(self):
        for disk_name, launchers in disques.items():
            disk_layout = QHBoxLayout()
            disk_layout.setContentsMargins(10, 5, 10, 5)  # Marges intérieures du disque
            disk_layout.setSpacing(10)  # Espacement entre le nom du disque et les launchers

            # Layout pour le nom du disque à gauche
            disk_label = QLabel(f'<b>{disk_name}</b>')
            disk_layout.addWidget(disk_label)

            # Layout pour les launchers à droite
            launchers_layout = QVBoxLayout()
            for launcher_name, games_list in launchers.items():
                launcher_layout = QHBoxLayout()
                launcher_layout.setContentsMargins(0, 0, 0, 0)  # Aucune marge pour les launchers
                launcher_label = QLabel(f'<u>{launcher_name}</u>')
                launcher_layout.addWidget(launcher_label)

                # Layout pour les jeux à droite de chaque launcher
                games_layout = QVBoxLayout()
                for game in games_list:
                    game_label = QLabel(f'{game["nom"]} ({game["année"]}) - {game["taille"]} GB')
                    games_layout.addWidget(game_label)

                # Ajouter le layout des jeux à la mise en page du launcher
                launcher_layout.addLayout(games_layout)
                launchers_layout.addLayout(launcher_layout)

            disk_layout.addLayout(launchers_layout)
            self.mainLayout.addLayout(disk_layout)

if __name__ == "__main__":
    print("Lancement de l'application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
