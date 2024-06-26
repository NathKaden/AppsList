from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QLabel
from PyQt6.QtCore import pyqtSignal
from functions.functions import *

class MainWindow(QMainWindow):
    changedToDark = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__initUi()
        self.__applyTheme()
        self.__applyBDD()

    def __initUi(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        self.setWindowTitle("GameList")
        self.setWindowIcon(QIcon('../assets/icon.jpg'))
        self.setGeometry(200, 200, 750, 480)  # (x, y, width, height)

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

        lay = QVBoxLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(lay)

        # Set the central widget
        self.setCentralWidget(centralWidget)


    def __applyTheme(self):
        print("Application du thème")
        stylesheet = """
        QWidget {
            color: #ffffff;
            font-size: 15px;
        }
        
        QMenuBar {
            background: qlineargradient(x1:0, y1:0, x2:0.5, y2:0,
                    stop:0 #2E3F00, stop:1 #353336);
            color: #ffffff;
            font-size: 15px;
            border-bottom: 1px solid;
            border-top: 1px solid #2d2b2e;
            border-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #9fc040, stop: 1 #575657) red #2d2b2e;
            padding-top: 1px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: rgba(255,255,255,40);
        }
        
        QMenuBar::item:hover {
            background-color: transparent;
        }
        
        QMenu {
            background-color: #2e2e2e;
            color: #ffffff;
            padding: 4px;
            border: 1px solid dimgrey;
        }
        
        QMenu::item {
            padding: 0 30px 0 20px;
        }
        
        QMenu::item:selected {
            background-color: #555555;
            border-radius: 5px;
        }
        
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #353336, stop:1 #3e3c40);
            color: #ffffff;
            font-size: 15px;
            border-top: 1px solid grey;
        }
        QStatusBar::item {
            border: none;
        }
        QStatusBar QLabel {
            background-color: transparent;
            padding: 0px 10 px;
        }
        """
        self.setStyleSheet(stylesheet)

    def __applyBDD(self):
        # Add a status bar
        statusbar = QStatusBar()


        # Liste de chaînes de caractères à afficher dans la barre de statut
        items = getDisques(BDD)

        # Création d'un QLabel pour afficher la liste avec "|" avant chaque élément, avec des couleurs différentes
        formatted_list = ""
        for index, item in enumerate(items):
            if index > 0:
                formatted_list += "   "
            formatted_list += f'<span style="font-weight:900; color: {get_color(index)};">| </span>{item}'

        list_label = QLabel(f'<html>{formatted_list}</html>')
        list_label.setOpenExternalLinks(True)  # Permet l'interprétation du HTML

        # Ajout du QLabel à la barre de statut
        statusbar.addWidget(list_label)


        r_label = str(getNbJeux(BDD)) + " App(s)"
        right_label = QLabel(r_label)

        # Ajout des widgets labels à la barre de statut
        statusbar.addPermanentWidget(list_label, 1)
        statusbar.addPermanentWidget(right_label)

        self.setStatusBar(statusbar)


if __name__ == "__main__":
    import sys
    print("Lancement de l'application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
