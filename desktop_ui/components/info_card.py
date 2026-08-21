from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout


class InfoCard(QFrame):
    """Reusable dashboard information card."""

    def __init__(
        self,
        label: str,
        value: str,
        description: str,
        parent=None,
    ):
        super().__init__(parent)

        self.setObjectName("InfoCard")
        self.setMinimumHeight(110)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(4)

        label_widget = QLabel(label)
        label_widget.setObjectName("CardLabel")

        self.value_widget = QLabel(value)
        self.value_widget.setObjectName("CardValue")

        description_widget = QLabel(description)
        description_widget.setObjectName("CardDescription")

        layout.addWidget(label_widget)
        layout.addWidget(self.value_widget)
        layout.addWidget(description_widget)
        layout.addStretch()

    def set_value(self, value: str):
        """Update the displayed value."""

        self.value_widget.setText(value)