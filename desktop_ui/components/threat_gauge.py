"""
NeuroFence threat assessment gauge.

Displays a centered visual representation of the
current model threat score.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QFont
from PyQt6.QtWidgets import QWidget


class ThreatGauge(QWidget):
    """Centered threat score gauge."""

    def __init__(self, score=0, parent=None):
        super().__init__(parent)

        self.score = max(
            0,
            min(100, score)
        )

        self.setObjectName("ThreatGauge")

        # Give the gauge a sensible minimum size,
        # while allowing the parent panel to resize it.
        self.setMinimumHeight(190)

    def set_score(self, score: int):
        """Update the threat score."""

        self.score = max(
            0,
            min(100, score)
        )

        self.update()

    def paintEvent(self, event):
        """Draw the gauge."""

        del event

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()
        height = self.height()

        # ---------------------------------------------------------
        # Center the gauge inside the available widget
        # ---------------------------------------------------------

        center_x = width // 2

        # Keep the visual group together vertically.
        center_y = int(height * 0.53)

        radius = min(
            width // 2 - 35,
            height // 2 - 25
        )

        radius = max(
            55,
            radius
        )

        # ---------------------------------------------------------
        # Background arc
        # ---------------------------------------------------------

        background_pen = QPen(
            Qt.GlobalColor.darkGray
        )

        background_pen.setWidth(14)
        background_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            background_pen
        )

        painter.drawArc(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2,
            40 * 16,
            100 * 16,
        )

        # ---------------------------------------------------------
        # Active score arc
        # ---------------------------------------------------------

        if self.score > 0:

            active_pen = QPen(
                Qt.GlobalColor.cyan
            )

            active_pen.setWidth(14)

            active_pen.setCapStyle(
                Qt.PenCapStyle.RoundCap
            )

            painter.setPen(
                active_pen
            )

            score_span = int(
                (self.score / 100) * 100
            )

            painter.drawArc(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2,
                40 * 16,
                -score_span * 16,
            )

        # ---------------------------------------------------------
        # Score number
        # ---------------------------------------------------------

        painter.setPen(
            Qt.GlobalColor.white
        )

        font = QFont(
            "Segoe UI",
            27
        )

        font.setBold(True)

        painter.setFont(
            font
        )

        score_text = str(
            self.score
        )

        text_rect = painter.boundingRect(
            0,
            0,
            width,
            50,
            Qt.AlignmentFlag.AlignCenter,
            score_text,
        )

        # Put the number directly underneath
        # the center of the gauge.
        text_y = center_y + radius // 2

        painter.drawText(
            text_rect.x(),
            text_y,
            text_rect.width(),
            50,
            Qt.AlignmentFlag.AlignCenter,
            score_text,
        )

        painter.end()