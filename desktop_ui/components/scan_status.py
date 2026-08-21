"""
NeuroFence scan status component.

Displays the current scanner state and progress.
"""

from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)


class ScanStatus(QFrame):
    """Displays the current scan state and progress."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Panel")

        self._build_ui()

    def _build_ui(self):
        """Build the scan status interface."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            16,
            20,
            16,
        )

        layout.setSpacing(8)

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        title = QLabel("Scan Status")

        title.setObjectName(
            "PanelTitle"
        )

        # ---------------------------------------------------------
        # Status message
        # ---------------------------------------------------------

        self.status_label = QLabel(
            "Ready to analyze model."
        )

        self.status_label.setObjectName(
            "PanelSubtitle"
        )

        # ---------------------------------------------------------
        # Progress bar
        # ---------------------------------------------------------

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100,
        )

        self.progress.setValue(
            0
        )

        self.progress.setTextVisible(
            False
        )

        self.progress.setMinimumHeight(
            7
        )

        self.progress.setMaximumHeight(
            7
        )

        # ---------------------------------------------------------
        # Layout
        # ---------------------------------------------------------

        layout.addWidget(
            title
        )

        layout.addWidget(
            self.status_label
        )

        layout.addWidget(
            self.progress
        )

    # =============================================================
    # PUBLIC METHODS
    # =============================================================

    def set_status(self, text: str):
        """Update the scan status message."""

        self.status_label.setText(
            text
        )

    def set_progress(self, value: int):
        """Update the scan progress."""

        value = max(
            0,
            min(
                100,
                value,
            ),
        )

        self.progress.setValue(
            value
        )