from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QStatusBar
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ma Application')
        self.setGeometry(100, 100, 600, 400)  # Taille initiale de la fenêtre

        # Création d'un widget central avec un layout vertical
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout(central_widget)

        # Ajout d'un label au layout central
        label = QLabel('Contenu principal ici', self)
        vbox.addWidget(label)

        # Changer la couleur de fond du widget central
        central_widget.setStyleSheet('''
            QWidget {
                background-color: #ADD8E6;  /* Couleur de fond de la fenêtre principale */
            }
        ''')

        # Création d'une barre de statut personnalisée
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)

        # Style CSS pour la barre de statut
        statusbar.setStyleSheet('''
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #353336, stop:1 #3e3c40); /* Dégradé horizontal de gauche à droite */
                color: #ffffff;
                font-size: 15px;
                border-top: 1px solid grey;
            }
            QStatusBar::resize-handle {
                width: 0;  /* Masque la poignée de redimensionnement */
                height: 0;
            }
        ''')

        # Ajout d'un widget dans la barre de statut
        status_label = QLabel('Statut : Prêt', self)
        statusbar.addWidget(status_label)

        self.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())
