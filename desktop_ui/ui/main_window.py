"""
NeuroFence main application window.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from desktop_ui.themes.dark_theme import DarkTheme


class Sidebar(QFrame):
    """Navigation sidebar for the NeuroFence application."""

    def __init__(self, navigation_callback, parent=None):
        super().__init__(parent)

        self.setObjectName("Sidebar")
        self.setMinimumWidth(220)
        self.setMaximumWidth(280)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )

        self.navigation_callback = navigation_callback
        self.navigation_buttons = []

        self._build_ui()

    def _build_ui(self):
        """Build the sidebar UI."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 20)
        layout.setSpacing(8)

        brand_title = QLabel("NeuroFence")
        brand_title.setObjectName("BrandTitle")

        brand_subtitle = QLabel("AI SECURITY PLATFORM")
        brand_subtitle.setObjectName("BrandSubtitle")

        layout.addWidget(brand_title)
        layout.addWidget(brand_subtitle)

        layout.addSpacing(28)

        navigation_items = [
            ("Dashboard", 0),
            ("Model Loader", 1),
            ("Security Scan", 2),
            ("Reports", 3),
            ("Settings", 4),
        ]

        for text, index in navigation_items:
            button = QPushButton(text)
            button.setObjectName("NavigationButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(44)

            button.clicked.connect(
                lambda checked=False, page_index=index:
                self._navigate(page_index)
            )

            layout.addWidget(button)
            self.navigation_buttons.append(button)

        layout.addStretch()

        version_label = QLabel("NeuroFence v0.1.0")
        version_label.setObjectName("BrandSubtitle")

        layout.addWidget(version_label)

        self.navigation_buttons[0].setChecked(True)

    def _navigate(self, page_index: int):
        """Handle navigation button selection."""

        for index, button in enumerate(self.navigation_buttons):
            button.setChecked(index == page_index)

        self.navigation_callback(page_index)


class PlaceholderPage(QWidget):
    """Temporary page used until the full UI is implemented."""

    def __init__(self, title: str, description: str, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        title_label = QLabel(title)
        title_label.setObjectName("PageTitle")

        description_label = QLabel(description)
        description_label.setObjectName("PageSubtitle")
        description_label.setWordWrap(True)

        card = QFrame()
        card.setObjectName("PlaceholderCard")
        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)

        card_title = QLabel("Module foundation ready")
        card_title.setObjectName("PlaceholderTitle")

        card_text = QLabel(
            "This page will be implemented during the "
            "corresponding NeuroFence development day."
        )
        card_text.setObjectName("PlaceholderText")
        card_text.setWordWrap(True)

        card_layout.addWidget(card_title)
        card_layout.addSpacing(8)
        card_layout.addWidget(card_text)
        card_layout.addStretch()

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(card)

    def set_page_content(self, title: str, description: str):
        """Update page content."""

        # Reserved for future page implementations.
        del title
        del description


class MainWindow(QMainWindow):
    """Main NeuroFence application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "NeuroFence — LLM Weight Poisoning & Backdoor Scanner"
        )

        self.resize(1200, 760)
        self.setMinimumSize(900, 600)

        self._build_ui()

    def _build_ui(self):
        """Build the main application layout."""

        central_widget = QWidget()
        central_widget.setObjectName("ContentArea")

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("ContentArea")

        self._create_pages()

        sidebar = Sidebar(
            navigation_callback=self._change_page
        )

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.page_stack, 1)

        self.setCentralWidget(central_widget)

    def _create_pages(self):
        """Create the initial application pages."""

        pages = [
            (
                "Dashboard",
                "NeuroFence security monitoring dashboard."
            ),
            (
                "Model Loader",
                "Load and validate an LLM for security analysis."
            ),
            (
                "Security Scan",
                "Analyze the selected model for security threats."
            ),
            (
                "Reports",
                "View and export NeuroFence security reports."
            ),
            (
                "Settings",
                "Configure NeuroFence application settings."
            ),
        ]

        for title, description in pages:
            page = PlaceholderPage(title, description)
            self.page_stack.addWidget(page)

    def _change_page(self, page_index: int):
        """Change the active application page."""

        if 0 <= page_index < self.page_stack.count():
            self.page_stack.setCurrentIndex(page_index)


def create_main_window() -> MainWindow:
    """Create and return the NeuroFence main window."""

    return MainWindow()