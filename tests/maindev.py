import sys
import webbrowser

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMenuBar, QVBoxLayout, QWidget, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AppsList")
        self.setWindowIcon(QIcon('../assets/icon.jpg'))
        self.setGeometry(400, 300, 750, 480)  # (x, y, width, height)

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

        githubAction.setStatusTip('Ouvrir le GitHub')
        githubAction.triggered.connect(self.open_github)
        commandAction.triggered.connect(self.open_input)

        central_layout = QVBoxLayout()
        centralWidget = QWidget()
        centralWidget.setObjectName("centralWidget")
        centralWidget.setLayout(central_layout)
        self.setCentralWidget(centralWidget)

    def open_github(self):
        webbrowser.open('https://github.com')

    def open_input(self):
        self.input = QLineEdit(self)
        self.input.returnPressed.connect(self.print_text)
        self.centralWidget().layout().addWidget(self.input)
        self.input.setFocus()

    def print_text(self):
        text = self.input.text()
        print(text)
        self.input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
