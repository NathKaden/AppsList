from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QMenuBar, QMenu, QAction
from PyQt5.QtCore import pyqtSignal

from pyqt_windows_os_light_dark_theme_window.main import Window

class MainWindow(Window):
    changedToDark = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__initUi()
        self.__applyDarkTheme()

    def __initUi(self):
        # Create a menu bar
        menuBar = QMenuBar(self)
        self.setWindowTitle("GameList")
        self.setWindowIcon(QIcon('../assets/icon.jpg'))
        self.setGeometry(200, 200, 750, 480)  # (x, y, width, height)

        # Fichier menu
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
        editMenu = QMenu('Editer', self)
        cutAction = QAction('Couper', self)
        copyAction = QAction('Copier', self)
        pasteAction = QAction('Coller', self)
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)

        # Vue menu
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
        otherMenu = QMenu('Autres', self)
        commandAction = QAction('Commande (terminal)', self)
        githubAction = QAction('GitHub', self)
        creditsAction = QAction('Crédits', self)
        otherMenu.addAction(commandAction)
        otherMenu.addAction(githubAction)
        otherMenu.addAction(creditsAction)

        # Add menus to menu bar
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(viewMenu)
        menuBar.addMenu(otherMenu)

        # Create a layout and central widget
        lay = QVBoxLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(lay)

        # Create a main layout that includes the menu bar
        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(menuBar)
        mainLayout.addWidget(centralWidget)

        # Set the main layout to the main widget
        self.setLayout(mainLayout)

        self.changedToDark.connect(self.__darkThemeOn)

    def __applyDarkTheme(self):
        dark_stylesheet = """
        QWidget {
            background-color: #353336;
            color: #ffffff;font-size: 15px;
        }
        QMenuBar {
            background-color: #3e3c40;
            color: #ffffff;
            font-size: 15px;
            border-bottom: 1px solid #2d2b2e;
        }
        QMenuBar::item {
            color: #ffffff;
        }
        QMenuBar::item::selected {
            background: #555555;
        }
        QMenu {
            background-color: #2e2e2e;
            color: #ffffff;
            padding: 4px;
            border: 1px solid dimgrey;
        }
        QMenu:item {
            padding: 0 30px 0 20px;
        }
        QMenu::item::selected {
            background-color: #555555;
            border-radius: 5px;
        }
        """
        self.setStyleSheet(dark_stylesheet)

    def __darkThemeOn(self, f):
        print(f'Is current theme dark?: {f}')

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())