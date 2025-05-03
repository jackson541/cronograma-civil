from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsView
from PyQt5.QtCore import pyqtSignal, QRectF, QObject
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter

class CustomRectItem(QGraphicsRectItem):
    def __init__(self, item, rect, color, position, callback_function, parent=None):
        rect = QRectF(*rect)
        super().__init__(rect,)
        self.item = item
        self.setBrush(QBrush(color))
        self.setPos(*position)
        self.setPen(QPen(QColor("black")))
        self.setAcceptHoverEvents(True)
        self.callback_function = callback_function

    def mousePressEvent(self, event):
        self.callback_function(self.item.id)
        super().mousePressEvent(event)


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        
    def wheelEvent(self, event):
        # Zoom factor
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        # Set anchor point
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        # Zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            
        self.scale(zoom_factor, zoom_factor)


