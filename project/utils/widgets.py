from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import pyqtSignal, QRectF, QObject
from PyQt5.QtGui import QBrush, QPen, QColor

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


