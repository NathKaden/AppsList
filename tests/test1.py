# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QLabel
from PyQt5.QtCore import Qt, QSize
from pyqtdarkmode import PyQtDarkMode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Activer le mode sombre pour l'application
        PyQtDarkMode.enable()

        # Créer la barre de menu
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Créer le menu "Fichier"
        file_menu = QMenu("Fichier", self)
        menu_bar.addMenu(file_menu)

        # Créer les options du menu "Fichier"
        new_action = QAction("Nouveau", self)
        file_menu.addAction(new_action)

        open_action = QAction("Ouvrir", self)
        file_menu.addAction(open_action)

        save_action = QAction("Enregistrer", self)
        file_menu.addAction(save_action)

        quit_action = QAction("Quitter", self)
        file_menu.addAction(quit_action)

        # Connecter l'option "Quitter" à la fonction de fermeture de l'application
        quit_action.triggered.connect(self.close)

        # Créer le titre de la fenêtre personnalisé
        title_label = QLabel("GameList", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 16pt;")
        self.setWindowTitle("")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.resize(800, 600)
        title_label.resize(self.width(), 30)
        title_label.move(0, 0)

        # Ajouter un widget de contenu à la fenêtre principale
        content_widget = QLabel("Contenu de la fenêtre", self)
        content_widget.setAlignment(Qt.AlignCenter)
        content_widget.resize(self.width(), self.height() - 30)
        content_widget.move(0, 30)

    def resizeEvent(self, event):
        # Redimensionner le titre de la fenêtre personnalisé lorsque la fenêtre est redimensionnée
        title_label = self.findChild(QLabel, "GameList")
        if title_label:
            title_label.resize(self.width(), 30)

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
