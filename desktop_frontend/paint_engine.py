import math
import random
from PyQt6.QtGui import QPainter, QColor, QBrush, QRadialGradient, QPen, QPolygon
from PyQt6.QtCore import Qt, QPoint

class VectorPaintEngine:
    def __init__(self, size=200):
        self.size = size
        self.is_blinking = False

    def render_layer_frame(self, painter: QPainter, skin_name: str, phase: float, glow: int):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        c = self.size / 2

        if skin_name == "CYBER_HUD":
            grad = QRadialGradient(c, c, 80)
            grad.setColorAt(0.0, QColor(0, 255, 204, glow))
            grad.setColorAt(0.8, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(10, 10, self.size - 20, self.size - 20)
            
            painter.setPen(QPen(QColor(0, 255, 204, 180), 2))
            painter.drawEllipse(45, 45, 110, 110)

        elif skin_name == "KAWAII_PET":
            if random.random() < 0.02: self.is_blinking = not self.is_blinking
            painter.setPen(QPen(QColor(255, 105, 180), 3))
            painter.setBrush(QBrush(QColor(255, 218, 224)))
            painter.drawEllipse(40, 50, 120, 95)
            
            painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QBrush(QColor(40, 40, 40)))
            if self.is_blinking:
                painter.setPen(QPen(QColor(40, 40, 40), 3))
                painter.drawLine(65, 92, 85, 92); painter.drawLine(115, 92, 135, 92)
            else:
                painter.drawEllipse(65, 82, 18, 18); painter.drawEllipse(115, 82, 18, 18)

        elif skin_name == "ZEN_OASIS":
            painter.setBrush(Qt.BrushStyle.NoBrush)
            for i in range(1, 6):
                radius = i * 26
                painter.setPen(QPen(QColor(218, 165, 32, max(10, 200 - (i * 35))), 1))
                painter.drawEllipse(int(c - radius/2), int(c - radius/2), radius, radius)
