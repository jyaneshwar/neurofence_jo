"""
NeuroFence main application window.

Day 3:
Professional security dashboard and application navigation.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from desktop_ui.components.info_card import InfoCard
from desktop_ui.components.threat_gauge import ThreatGauge
from desktop_ui.components.activity_panel import ActivityPanel
from desktop_ui.components.scan_status import ScanStatus


class Sidebar(QFrame):
    """Professional NeuroFence navigation sidebar."""

    def __init__(self, navigation_callback, parent=None):
        super().__init__(parent)

        self.setObjectName("Sidebar")
        self.setFixedWidth(218)

        self.navigation_callback = navigation_callback
        self.navigation_buttons = []

        self._build_ui()

    def _build_ui(self):
        """Build the sidebar."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 22, 14, 18)
        layout.setSpacing(5)

        # ---------------------------------------------------------
        # Branding
        # ---------------------------------------------------------

        brand = QLabel("NEUROFENCE")
        brand.setObjectName("BrandTitle")

        subtitle = QLabel("LLM SECURITY PLATFORM")
        subtitle.setObjectName("BrandSubtitle")

        layout.addWidget(brand)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        # ---------------------------------------------------------
        # Overview section
        # ---------------------------------------------------------

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
            button.setMinimumHeight(40)
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            button.clicked.connect(
                lambda checked=False, i=index:
                self._navigate(i)
            )

            layout.addWidget(button)

            self.navigation_buttons.append(button)

        # ---------------------------------------------------------
        # System section
        # ---------------------------------------------------------

        layout.addSpacing(24)

        system = QLabel("SYSTEM")
        system.setObjectName("SectionLabel")

        layout.addWidget(system)

        settings = QPushButton("Settings")

        settings.setObjectName("NavigationButton")
        settings.setCheckable(True)
        settings.setMinimumHeight(40)
        settings.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        settings.clicked.connect(
            lambda: self._navigate(5)
        )

        layout.addWidget(settings)

        self.navigation_buttons.append(settings)

        # ---------------------------------------------------------
        # Bottom section
        # ---------------------------------------------------------

        layout.addStretch()

        status = QLabel("●  SYSTEM SECURE")
        status.setObjectName("StatusGreen")

        version = QLabel("NeuroFence  •  v0.1.0")
        version.setObjectName("VersionLabel")

        layout.addWidget(status)
        layout.addWidget(version)

        # Dashboard selected by default
        self.navigation_buttons[0].setChecked(True)

    def _navigate(self, index):
        """Navigate to a page."""

        for button_index, button in enumerate(
            self.navigation_buttons
        ):
            button.setChecked(
                button_index == index
            )

        self.navigation_callback(index)


class TopBar(QFrame):
    """Application top navigation bar."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TopBar")
        self.setFixedHeight(62)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            24,
            0,
            24,
            0,
        )

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        title_box = QVBoxLayout()
        title_box.setSpacing(1)

        title = QLabel("Security Overview")
        title.setObjectName("TopTitle")

        subtitle = QLabel(
            "Model security monitoring"
        )
        subtitle.setObjectName("TopSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        layout.addLayout(title_box)

        layout.addStretch()

        # ---------------------------------------------------------
        # System status
        # ---------------------------------------------------------

        badge = QLabel("●  SYSTEM SECURE")
        badge.setObjectName("SecureBadge")

        layout.addWidget(badge)


class DashboardPage(QWidget):
    """
    Main NeuroFence security dashboard.

    This page currently displays UI state and placeholder
    security information. Real model/scanner data will be
    connected in later development days.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        """Build dashboard layout."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            28,
            26,
            28,
            28,
        )

        layout.setSpacing(16)

        # =========================================================
        # PAGE HEADER
        # =========================================================

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Monitor the security posture of your loaded "
            "language model."
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # =========================================================
        # INFORMATION CARDS
        # =========================================================

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.model_card = InfoCard(
            "MODEL",
            "NOT LOADED",
            "No model selected",
        )

        self.scan_card = InfoCard(
            "SCANS",
            "0",
            "Security scans completed",
        )

        self.threat_card = InfoCard(
            "THREAT SCORE",
            "0 / 100",
            "Current security risk",
        )

        self.status_card = InfoCard(
            "STATUS",
            "SECURE",
            "No suspicious activity",
        )

        cards_layout.addWidget(
            self.model_card
        )

        cards_layout.addWidget(
            self.scan_card
        )

        cards_layout.addWidget(
            self.threat_card
        )

        cards_layout.addWidget(
            self.status_card
        )

        layout.addLayout(cards_layout)

        # =========================================================
        # MIDDLE SECTION
        # =========================================================

        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(14)

        # ---------------------------------------------------------
        # Activity panel
        # ---------------------------------------------------------

        self.activity_panel = ActivityPanel()

        # ---------------------------------------------------------
        # Threat assessment panel
        # ---------------------------------------------------------

        gauge_panel = QFrame()
        gauge_panel.setObjectName("Panel")

        gauge_layout = QVBoxLayout(
            gauge_panel
        )

        gauge_layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        gauge_layout.setSpacing(6)

        gauge_title = QLabel(
            "Threat Assessment"
        )

        gauge_title.setObjectName(
            "PanelTitle"
        )

        gauge_subtitle = QLabel(
            "Current model security score"
        )

        gauge_subtitle.setObjectName(
            "PanelSubtitle"
        )

        self.threat_gauge = ThreatGauge(
            0
        )

        gauge_layout.addWidget(
            gauge_title
        )

        gauge_layout.addWidget(
            gauge_subtitle
        )

        gauge_layout.addWidget(
            self.threat_gauge,
            1,
        )

        middle_layout.addWidget(
            self.activity_panel,
            3,
        )

        middle_layout.addWidget(
            gauge_panel,
            2,
        )

        layout.addLayout(
            middle_layout,
            1,
        )

        # =========================================================
        # SCAN STATUS
        # =========================================================

        self.scan_status = ScanStatus()

        layout.addWidget(
            self.scan_status
        )

    # =============================================================
    # DASHBOARD UPDATE METHODS
    # =============================================================

    def update_model(self, model_name: str):
        """Update the loaded model displayed on the dashboard."""

        self.model_card.set_value(
            model_name
        )

        self.activity_panel.add_activity(
            f"Model loaded: {model_name}"
        )

    def update_scan_count(self, count: int):
        """Update number of completed scans."""

        self.scan_card.set_value(
            str(count)
        )

    def update_threat_score(self, score: int):
        """Update the dashboard threat score."""

        score = max(
            0,
            min(
                100,
                score,
            ),
        )

        self.threat_gauge.set_score(
            score
        )

        self.threat_card.set_value(
            f"{score} / 100"
        )

        # ---------------------------------------------------------
        # Security status
        # ---------------------------------------------------------

        if score < 30:

            self.status_card.set_value(
                "SECURE"
            )

        elif score < 70:

            self.status_card.set_value(
                "WARNING"
            )

        else:

            self.status_card.set_value(
                "CRITICAL"
            )

    def update_scan_status(
        self,
        message: str,
        progress: int,
    ):
        """Update scan status and progress."""

        self.scan_status.set_status(
            message
        )

        self.scan_status.set_progress(
            progress
        )


class PlaceholderPage(QWidget):
    """
    Temporary page for modules that will be implemented later.
    """

    def __init__(
        self,
        title: str,
        description: str,
        parent=None,
    ):
        super().__init__(parent)

        self._build_ui(
            title,
            description,
        )

    def _build_ui(
        self,
        title: str,
        description: str,
    ):
        """Build placeholder page."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            28,
            26,
            28,
            28,
        )

        layout.setSpacing(18)

        # ---------------------------------------------------------
        # Page heading
        # ---------------------------------------------------------

        title_label = QLabel(title)
        title_label.setObjectName(
            "PageTitle"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "PageSubtitle"
        )

        description_label.setWordWrap(
            True
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            description_label
        )

        # ---------------------------------------------------------
        # Placeholder panel
        # ---------------------------------------------------------

        panel = QFrame()
        panel.setObjectName("Panel")

        panel_layout = QVBoxLayout(
            panel
        )

        panel_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        panel_layout.setSpacing(8)

        heading = QLabel(
            "Module ready for implementation"
        )

        heading.setObjectName(
            "PanelTitle"
        )

        text = QLabel(
            "This area is reserved for the "
            "corresponding NeuroFence security workflow."
        )

        text.setObjectName(
            "PanelSubtitle"
        )

        text.setWordWrap(
            True
        )

        panel_layout.addWidget(
            heading
        )

        panel_layout.addWidget(
            text
        )

        panel_layout.addStretch()

        layout.addWidget(
            panel,
            1,
        )


class MainWindow(QMainWindow):
    """Main NeuroFence application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "NeuroFence — LLM Security Scanner"
        )

        self.resize(
            1240,
            780,
        )

        self.setMinimumSize(
            1000,
            650,
        )

        self._build_ui()

    def _build_ui(self):
        """Build the main application layout."""

        # =========================================================
        # CENTRAL WIDGET
        # =========================================================

        central_widget = QWidget()

        central_widget.setObjectName(
            "ContentArea"
        )

        root_layout = QHBoxLayout(
            central_widget
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root_layout.setSpacing(0)

        # =========================================================
        # SIDEBAR
        # =========================================================

        sidebar = Sidebar(
            navigation_callback=self._change_page
        )

        # =========================================================
        # MAIN CONTENT
        # =========================================================

        content_widget = QWidget()

        content_layout = QVBoxLayout(
            content_widget
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(0)

        # =========================================================
        # TOP BAR
        # =========================================================

        top_bar = TopBar()

        # =========================================================
        # PAGE STACK
        # =========================================================

        self.page_stack = QStackedWidget()

        self.page_stack.setObjectName(
            "ContentArea"
        )

        self._create_pages()

        # =========================================================
        # ASSEMBLE CONTENT
        # =========================================================

        content_layout.addWidget(
            top_bar
        )

        content_layout.addWidget(
            self.page_stack,
            1,
        )

        # =========================================================
        # ASSEMBLE MAIN WINDOW
        # =========================================================

        root_layout.addWidget(
            sidebar
        )

        root_layout.addWidget(
            content_widget,
            1,
        )

        self.setCentralWidget(
            central_widget
        )

    def _create_pages(self):
        """Create application pages."""

        # ---------------------------------------------------------
        # Dashboard
        # ---------------------------------------------------------

        self.dashboard_page = DashboardPage()

        self.page_stack.addWidget(
            self.dashboard_page
        )

        # ---------------------------------------------------------
        # Model Loader
        # ---------------------------------------------------------

        model_loader_page = PlaceholderPage(
            "Model Loader",
            "Load and validate an LLM for security analysis.",
        )

        self.page_stack.addWidget(
            model_loader_page
        )

        # ---------------------------------------------------------
        # Security Scan
        # ---------------------------------------------------------

        security_scan_page = PlaceholderPage(
            "Security Scan",
            "Analyze the selected model for suspicious behavior.",
        )

        self.page_stack.addWidget(
            security_scan_page
        )

        # ---------------------------------------------------------
        # Activation Tracker
        # ---------------------------------------------------------

        activation_page = PlaceholderPage(
            "Activation Tracker",
            "Inspect model activation behavior and suspicious patterns.",
        )

        self.page_stack.addWidget(
            activation_page
        )

        # ---------------------------------------------------------
        # Reports
        # ---------------------------------------------------------

        reports_page = PlaceholderPage(
            "Reports",
            "Review and export NeuroFence security findings.",
        )

        self.page_stack.addWidget(
            reports_page
        )

        # ---------------------------------------------------------
        # Settings
        # ---------------------------------------------------------

        settings_page = PlaceholderPage(
            "Settings",
            "Configure NeuroFence application preferences.",
        )

        self.page_stack.addWidget(
            settings_page
        )

    def _change_page(self, page_index: int):
        """Switch the active application page."""

        if (
            0 <= page_index
            < self.page_stack.count()
        ):
            self.page_stack.setCurrentIndex(
                page_index
            )


def create_main_window() -> MainWindow:
    """Create and return the NeuroFence main window."""

    return MainWindow()