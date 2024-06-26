from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from functions.functions import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Styled List in StatusBar Example")
        self.setWindowIcon(QIcon('../assets/icon.jpg'))
        self.setGeometry(200, 200, 750, 480)  # (x, y, width, height)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout()
        centralWidget.setLayout(layout)

        status_bar = QStatusBar()
        layout.addWidget(status_bar)



        # Application du style personnalisé à la QStatusBar
        status_bar.setStyleSheet('''
            QStatusBar {
                background-color: #3e3c40;
                color: #ffffff;
                font-size: 15px;
                border-top: 1px solid #2d2b2e;
            }
            QStatusBar QLabel {
                padding: 5px;   /* Espacement intérieur */
            }
        ''')

        self.setStatusBar(status_bar)

    def get_color(self, index):
        # Fonction pour obtenir une couleur différente pour chaque élément
        colors = ["red", "blue", "green"]  # Ajoutez plus de couleurs au besoin
        return colors[index % len(colors)]  # Utilisation du modulo pour boucler sur les couleurs

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
