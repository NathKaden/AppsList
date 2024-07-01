from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QMenuBar, QMenu, QMainWindow, QStatusBar, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
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
        centralWidget.setObjectName("centralWidget")  # Ajout du nom d'objet
        centralWidget.setLayout(lay)


    def __applyTheme(self):
        with open('../assets/style.qss', 'r') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def __applyBDD(self):

        path_settings = "../assets/settings.json"
        fichiersettings = open(path_settings, "r", encoding='utf-8')
        settings = json.load(fichiersettings)
        fichiersettings.close()
        path_bdd = settings["path_bdd"]
        BDD = loadBDD(path_bdd)

        statusbar = QStatusBar()

        disques = getDisques(BDD)
        formatted_list = "" # Création d'un QLabel pour afficher la liste avec "|" avant chaque élément, avec des couleurs différentes
        for index, disque in enumerate(disques):
            if index > 0:
                formatted_list += "   "
            formatted_list += f'<span style="font-weight:900; color: {get_color(index)};">| </span>{disque}'

        list_label = QLabel(f'<html>{formatted_list}</html>')
        list_label.setOpenExternalLinks(True)  # Permet l'interprétation du HTML

        # Ajout du QLabel à la barre de statut
        statusbar.addWidget(list_label)

        # Afficher le nom du fichier
        bddnamestr = os.path.splitext(os.path.basename(path_bdd))[0]


        r_label = bddnamestr +"  -  "+ str(getNbApps(BDD)) + " App(s)"
        right_label = QLabel(r_label)

        # Ajout des widgets labels à la barre de statut
        statusbar.addPermanentWidget(list_label, 1)
        statusbar.addPermanentWidget(right_label)
        self.setStatusBar(statusbar)

        # TO DO -------------------------------------------------
        # Central Widget

        html1 = f'<html><div style="display: flex; flex-direction:column; gap:10px;">'

        listdisques = ""
        for indexd, disque in enumerate(disques):
            if indexd > 0:
                listdisques += "<br>"
            listdisques += f'<div style="width:100%; background-color:#333;">{disque}</div>'

        listdisques_label = QLabel(f'{html1}{listdisques}</div></html>')

        print(getDisques(BDD))
        print(getLaunchers(BDD))
        print(getApps(BDD))
        print(getNbDisques(BDD))
        print(getNbLaunchers(BDD))
        print(getNbApps(BDD))

        # TO DO -------------------------------------------------
        # Mise en place
        listdisques_label.setOpenExternalLinks(True)
        listdisques_label.setObjectName("centralWidget")
        listdisques_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setCentralWidget(listdisques_label)


if __name__ == "__main__":
    import sys
    print("Lancement de l'application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

