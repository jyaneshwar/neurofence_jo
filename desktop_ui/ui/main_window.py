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


class Sidebar(QFrame):
    """Professional navigation sidebar."""

    def __init__(self, navigation_callback, parent=None):
        super().__init__(parent)

        self.setObjectName("Sidebar")
        self.setFixedWidth(218)

        self.navigation_callback = navigation_callback
        self.navigation_buttons = []

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 22, 14, 18)
        layout.setSpacing(5)

        brand = QLabel("NEUROFENCE")
        brand.setObjectName("BrandTitle")

        subtitle = QLabel("LLM SECURITY PLATFORM")
        subtitle.setObjectName("BrandSubtitle")

        layout.addWidget(brand)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        overview = QLabel("OVERVIEW")
        overview.setObjectName("SectionLabel")
        layout.addWidget(overview)

        navigation_items = [
            ("Dashboard", 0),
            ("Model Loader", 1),
            ("Security Scan", 2),
            ("Activations", 3),
            ("Reports", 4),
        ]

        for text, index in navigation_items:
            button = QPushButton(text)
            button.setObjectName("NavigationButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(40)

            button.clicked.connect(
                lambda checked=False, i=index:
                self._navigate(i)
            )

            layout.addWidget(button)
            self.navigation_buttons.append(button)

        layout.addSpacing(24)

        system = QLabel("SYSTEM")
        system.setObjectName("SectionLabel")
        layout.addWidget(system)

        settings = QPushButton("Settings")
        settings.setObjectName("NavigationButton")
        settings.setCheckable(True)
        settings.setMinimumHeight(40)
        settings.setCursor(Qt.CursorShape.PointingHandCursor)

        settings.clicked.connect(
            lambda: self._navigate(5)
        )

        layout.addWidget(settings)
        self.navigation_buttons.append(settings)

        layout.addStretch()

        status = QLabel("●  SYSTEM SECURE")
        status.setObjectName("StatusGreen")

        version = QLabel("NeuroFence  •  v0.1.0")
        version.setObjectName("VersionLabel")

        layout.addWidget(status)
        layout.addWidget(version)

        self.navigation_buttons[0].setChecked(True)

    def _navigate(self, index):
        for i, button in enumerate(self.navigation_buttons):
            button.setChecked(i == index)

        self.navigation_callback(index)


class TopBar(QFrame):
    """Application top bar."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TopBar")
        self.setFixedHeight(62)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)

        title_box = QVBoxLayout()
        title_box.setSpacing(1)

        title = QLabel("Security Overview")
        title.setObjectName("TopTitle")

        subtitle = QLabel("Model security monitoring")
        subtitle.setObjectName("TopSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        layout.addLayout(title_box)
        layout.addStretch()

        badge = QLabel("●  SYSTEM SECURE")
        badge.setObjectName("SecureBadge")

        layout.addWidget(badge)


class InfoCard(QFrame):
    """Small security information card."""

    def __init__(self, label, value, description):
        super().__init__()

        self.setObjectName("InfoCard")
        self.setMinimumHeight(112)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(4)

        label_widget = QLabel(label)
        label_widget.setObjectName("CardLabel")

        value_widget = QLabel(value)
        value_widget.setObjectName("CardValue")

        description_widget = QLabel(description)
        description_widget.setObjectName("CardDescription")

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        layout.addWidget(description_widget)
        layout.addStretch()


class DashboardPage(QWidget):
    """Initial NeuroFence dashboard."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 28)
        layout.setSpacing(18)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "A clear view of your model's current security posture."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        cards_layout.addWidget(
            InfoCard(
                "MODEL",
                "Not Loaded",
                "Select an LLM to begin analysis",
            )
        )

        cards_layout.addWidget(
            InfoCard(
                "LAST SCAN",
                "—",
                "No security scans performed",
            )
        )

        cards_layout.addWidget(
            InfoCard(
                "THREAT SCORE",
                "0 / 100",
                "No threats detected",
            )
        )

        layout.addLayout(cards_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(14)

        activity_panel = QFrame()
        activity_panel.setObjectName("Panel")

        activity_layout = QVBoxLayout(activity_panel)
        activity_layout.setContentsMargins(20, 18, 20, 18)

        activity_title = QLabel("Recent Activity")
        activity_title.setObjectName("PanelTitle")

        activity_subtitle = QLabel(
            "Security events and scan activity will appear here."
        )
        activity_subtitle.setObjectName("PanelSubtitle")

        activity_empty = QLabel("No activity recorded yet.")
        activity_empty.setObjectName("EmptyState")
        activity_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)

        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(activity_subtitle)
        activity_layout.addWidget(activity_empty, 1)

        scan_panel = QFrame()
        scan_panel.setObjectName("Panel")

        scan_layout = QVBoxLayout(scan_panel)
        scan_layout.setContentsMargins(20, 18, 20, 18)

        scan_title = QLabel("Scan Center")
        scan_title.setObjectName("PanelTitle")

        scan_subtitle = QLabel(
            "Choose a model and start a security assessment."
        )
        scan_subtitle.setObjectName("PanelSubtitle")

        scan_empty = QLabel(
            "MODEL REQUIRED\n\n"
            "Load a model before starting a security scan."
        )
        scan_empty.setObjectName("EmptyState")
        scan_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scan_button = QPushButton("Start Security Scan")
        scan_button.setObjectName("PrimaryButton")
        scan_button.setCursor(Qt.CursorShape.PointingHandCursor)

        scan_layout.addWidget(scan_title)
        scan_layout.addWidget(scan_subtitle)
        scan_layout.addWidget(scan_empty, 1)
        scan_layout.addWidget(scan_button)

        bottom_layout.addWidget(activity_panel, 3)
        bottom_layout.addWidget(scan_panel, 2)

        layout.addLayout(bottom_layout, 1)


class PlaceholderPage(QWidget):
    """Placeholder for future modules."""

    def __init__(self, title, description):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 28)
        layout.setSpacing(18)

        title_label = QLabel(title)
        title_label.setObjectName("PageTitle")

        description_label = QLabel(description)
        description_label.setObjectName("PageSubtitle")

        panel = QFrame()
        panel.setObjectName("Panel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)

        heading = QLabel("Module ready for implementation")
        heading.setObjectName("PanelTitle")

        text = QLabel(
            "This area is reserved for the corresponding "
            "NeuroFence security workflow."
        )
        text.setObjectName("PanelSubtitle")

        panel_layout.addWidget(heading)
        panel_layout.addSpacing(6)
        panel_layout.addWidget(text)
        panel_layout.addStretch()

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(panel, 1)


class MainWindow(QMainWindow):
    """Main NeuroFence application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "NeuroFence — LLM Security Scanner"
        )

        self.resize(1240, 780)
        self.setMinimumSize(1000, 650)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("ContentArea")

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = Sidebar(self._change_page)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        topbar = TopBar()

        self.page_stack = QStackedWidget()

        self._create_pages()

        content_layout.addWidget(topbar)
        content_layout.addWidget(self.page_stack, 1)

        root.addWidget(sidebar)
        root.addWidget(content, 1)

        self.setCentralWidget(central)

    def _create_pages(self):
        pages = [
            DashboardPage(),
            PlaceholderPage(
                "Model Loader",
                "Load and validate an LLM for security analysis.",
            ),
            PlaceholderPage(
                "Security Scan",
                "Analyze the selected model for suspicious behavior.",
            ),
            PlaceholderPage(
                "Activation Tracker",
                "Inspect model activation behavior.",
            ),
            PlaceholderPage(
                "Reports",
                "Review and export security findings.",
            ),
            PlaceholderPage(
                "Settings",
                "Configure NeuroFence.",
            ),
        ]

        for page in pages:
            self.page_stack.addWidget(page)

    def _change_page(self, index):
        if 0 <= index < self.page_stack.count():
            self.page_stack.setCurrentIndex(index)


def create_main_window():
    """Create the main NeuroFence window."""
    return MainWindow()