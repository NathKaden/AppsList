from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsView


class CanvasView(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Déplacement au clic gauche
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        # Masquer les barres de défilement
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # --- CONFIGURATION DES LIMITES DE ZOOM ---
        self.zoom_minimum = 0.3  # Dézoomer jusqu'à 30% de la taille réelle
        self.zoom_maximum = 3.0  # Zoomer jusqu'à 300%

    def wheelEvent(self, event):
        """Gère le zoom avec une borne min et max."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        # 1. Calculer le facteur théorique selon le sens de la molette
        if event.angleDelta().y() > 0:
            facteur_potentiel = zoom_in_factor
        else:
            facteur_potentiel = zoom_out_factor

        # 2. Récupérer le niveau de zoom actuel sur l'axe X (m11 de la matrice de transformation)
        zoom_actuel = self.transform().m11()

        # 3. Calculer le niveau de zoom final si on appliquait le changement
        zoom_futur = zoom_actuel * facteur_potentiel

        # 4. Appliquer le zoom uniquement si on reste dans les limites
        if self.zoom_minimum <= zoom_futur <= self.zoom_maximum:
            self.scale(facteur_potentiel, facteur_potentiel)