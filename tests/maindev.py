from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QIODevice, QFile
from functions.functions import *

from functions.functions import loadBDD

def load_stylesheet():
    style_file = QFile("../assets/styles.css")  # Nom du fichier CSS
    style_sheet = style_file.readAll()
    QApplication.instance().setStyleSheet(bytes(style_sheet).decode("utf-8"))
    style_file.close()
    print("Impossible de charger la feuille de style.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()
        self.__applyTheme()
        self.__applyBDD()

    def __initUi(self):
        self.setWindowTitle("GameList")
        self.setWindowIcon(QIcon('../assets/icon.jpg'))
        self.setGeometry(200, 200, 750, 480)

        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

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

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

    def __applyTheme(self):
        stylesheet = """
        QWidget {
            color: #ffffff;
            font-size: 15px;
        }
        QMenuBar {
            background: qlineargradient(x1:0, y1:0, x2:0.5, y2:0,
                    stop:0 #3b3b54, stop:1 #353336);
            color: #ffffff;
            font-size: 15px;
            border-bottom: 1px solid;
            border-top: 1px solid #2d2b2e;
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
        """
        self.setStyleSheet(stylesheet)

    def __applyBDD(self):
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # Exemple de chargement de données et affichage dans la barre de statut
        path_bdd = "chemin_vers_votre_base_de_donnees"
        BDD = loadBDD(path_bdd)

        disques = ["Disque 1", "Disque 2", "Disque 3"]  # Exemple de données

        formatted_list = ""
        for index, disque in enumerate(disques):
            if index > 0:
                formatted_list += "   "
            formatted_list += f'<span style="font-weight:900; color: red;">| </span>{disque}'

        list_label = QLabel(f'<html>{formatted_list}</html>')
        statusbar.addWidget(list_label)

        # Exemple d'utilisation d'un QLabel pour afficher des données dans la fenêtre principale
        listdisques_label = QLabel(f'<html><div class="disque">{"<br>".join(disques)}</div></html>')
        listdisques_label.setObjectName("centralWidget")
        self.setCentralWidget(listdisques_label)


def main():
    import sys
    app = QApplication(sys.argv)

    # Charger la feuille de style CSS
    load_stylesheet()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
