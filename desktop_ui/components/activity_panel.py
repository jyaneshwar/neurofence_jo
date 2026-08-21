from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class ActivityPanel(QFrame):
    """Recent security activity panel."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        title = QLabel("Recent Activity")
        title.setObjectName("PanelTitle")

        subtitle = QLabel(
            "Security events and scan activity."
        )
        subtitle.setObjectName("PanelSubtitle")

        self.activity_label = QLabel(
            "No security activity recorded yet."
        )

        self.activity_label.setObjectName("EmptyState")
        self.activity_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.activity_label, 1)

    def add_activity(self, message: str):
        """Display the latest activity message."""

        self.activity_label.setText(message)
        