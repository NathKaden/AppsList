from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMenuBar, QMenu, QMainWindow
from PyQt6.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    changedToDark = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        print("Initialisation de l'interface utilisateur")
        self.__initUi()
        print("Application du thème")
        self.__applyTheme()

    def __initUi(self):
        # Create a menu bar
        print("Création de la barre de menu")
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        self.setWindowTitle("GameList")
        self.setWindowIcon(QIcon('../assets/icon.jpg'))
        self.setGeometry(200, 200, 750, 480)  # (x, y, width, height)

        # Fichier menu
        print("Création du menu Fichier")
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

        # Edit menu
        print("Création du menu Editer")
        editMenu = QMenu('Editer', self)
        cutAction = QAction('Couper', self)
        copyAction = QAction('Copier', self)
        pasteAction = QAction('Coller', self)
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)

        # Vue menu
        print("Création du menu Vue")
        viewMenu = QMenu('Vue', self)
        listAction = QAction('Liste', self)
        sortAction = QAction('Trier', self)
        themeAction = QAction('Thèmes', self)
        languageAction = QAction('Langue', self)
        viewMenu.addAction(listAction)
        viewMenu.addAction(sortAction)
        viewMenu.addAction(themeAction)
        viewMenu.addAction(languageAction)

        # Autres menu
        print("Création du menu Autres")
        otherMenu = QMenu('Autres', self)
        commandAction = QAction('Commande (terminal)', self)
        githubAction = QAction('GitHub', self)
        creditsAction = QAction('Crédits', self)
        otherMenu.addAction(commandAction)
        otherMenu.addAction(githubAction)
        otherMenu.addAction(creditsAction)

        # Add menus to menu bar
        print("Ajout des menus à la barre de menu")
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(viewMenu)
        menuBar.addMenu(otherMenu)

        # Create a layout and central widget
        print("Création du layout et du widget central")
        lay = QVBoxLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(lay)

        # Set the central widget
        self.setCentralWidget(centralWidget)

    def __applyTheme(self):
        print("Application du thème")
        stylesheet = """
        QWidget {
            background-color: #353336;
            color: #ffffff;
            font-size: 15px;
        }
        
        QMenuBar {
            background-color: #3e3c40;
            color: #ffffff;
            font-size: 15px;
            border-bottom: 1px solid #2d2b2e;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: #555555;
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

if __name__ == "__main__":
    import sys
    print("Lancement de l'application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("Affichage de la fenêtre principale")
    sys.exit(app.exec())
