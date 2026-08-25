"""
NeuroFence Main Window

Includes:
    - Dashboard
    - Model Loader
    - Security Scan placeholder
    - Activation Tracker placeholder
    - Reports placeholder
    - Settings placeholder
"""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from model_loader.validator import ModelValidator


# ============================================================
# INFO CARD
# ============================================================

class InfoCard(QFrame):

    def __init__(
        self,
        title,
        value,
        description,
        parent=None,
    ):
        super().__init__(parent)

        self.setObjectName("InfoCard")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(5)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("CardTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("CardValue")

        self.description_label = QLabel(description)
        self.description_label.setObjectName("CardDescription")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.description_label)

    def set_value(self, value):

        self.value_label.setText(str(value))


# ============================================================
# THREAT GAUGE
# ============================================================

class ThreatGauge(QFrame):

    def __init__(self, score=0, parent=None):
        super().__init__(parent)

        self.score = score

        self.setObjectName("ThreatGauge")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            20,
            10,
            20,
        )

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.score_label = QLabel(
            f"{score}"
        )

        self.score_label.setObjectName(
            "ThreatScore"
        )

        self.level_label = QLabel(
            "LOW RISK"
        )

        self.level_label.setObjectName(
            "ThreatLevel"
        )

        layout.addWidget(
            self.score_label,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addWidget(
            self.level_label,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

    def set_score(self, score):

        self.score = score

        self.score_label.setText(
            str(score)
        )

        if score < 30:
            level = "LOW RISK"

        elif score < 70:
            level = "MEDIUM RISK"

        else:
            level = "HIGH RISK"

        self.level_label.setText(level)


# ============================================================
# ACTIVITY PANEL
# ============================================================

class ActivityPanel(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName("Panel")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        layout.setSpacing(8)

        title = QLabel(
            "Recent Activity"
        )

        title.setObjectName(
            "PanelTitle"
        )

        subtitle = QLabel(
            "NeuroFence system activity"
        )

        subtitle.setObjectName(
            "PanelSubtitle"
        )

        self.activity_label = QLabel(
            "No activity yet."
        )

        self.activity_label.setObjectName(
            "PanelSubtitle"
        )

        self.activity_label.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        layout.addWidget(
            self.activity_label
        )

        layout.addStretch()

    def add_activity(self, message):

        self.activity_label.setText(
            message
        )


# ============================================================
# SCAN STATUS
# ============================================================

class ScanStatus(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "ScanStatus"
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            15,
            10,
            15,
            10,
        )

        self.label = QLabel(
            "● Scanner ready"
        )

        self.label.setObjectName(
            "StatusGreen"
        )

        layout.addWidget(
            self.label
        )

        layout.addStretch()

    def set_status(self, text):

        self.label.setText(text)


# ============================================================
# SIDEBAR
# ============================================================

class Sidebar(QFrame):

    def __init__(
        self,
        navigation_callback,
        parent=None,
    ):

        super().__init__(parent)

        self.navigation_callback = (
            navigation_callback
        )

        self.buttons = []

        self.setObjectName(
            "Sidebar"
        )

        self.setFixedWidth(
            220
        )

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            22,
            14,
            18,
        )

        layout.setSpacing(5)

        # ----------------------------------------------------
        # Brand
        # ----------------------------------------------------

        brand = QLabel(
            "NEUROFENCE"
        )

        brand.setObjectName(
            "BrandTitle"
        )

        subtitle = QLabel(
            "LLM SECURITY PLATFORM"
        )

        subtitle.setObjectName(
            "BrandSubtitle"
        )

        layout.addWidget(brand)
        layout.addWidget(subtitle)

        layout.addSpacing(28)

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------

        overview = QLabel(
            "OVERVIEW"
        )

        overview.setObjectName(
            "SectionLabel"
        )

        layout.addWidget(
            overview
        )

        items = [
            ("Dashboard", 0),
            ("Model Loader", 1),
            ("Security Scan", 2),
            ("Activations", 3),
            ("Reports", 4),
        ]

        for text, index in items:

            button = QPushButton(text)

            button.setObjectName(
                "NavigationButton"
            )

            button.setCheckable(True)

            button.setMinimumHeight(
                40
            )

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            button.clicked.connect(
                lambda checked=False, i=index:
                self.navigate(i)
            )

            layout.addWidget(
                button
            )

            self.buttons.append(
                button
            )

        # ----------------------------------------------------
        # System
        # ----------------------------------------------------

        layout.addSpacing(20)

        system = QLabel(
            "SYSTEM"
        )

        system.setObjectName(
            "SectionLabel"
        )

        layout.addWidget(
            system
        )

        settings = QPushButton(
            "Settings"
        )

        settings.setObjectName(
            "NavigationButton"
        )

        settings.setCheckable(True)

        settings.setMinimumHeight(
            40
        )

        settings.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        settings.clicked.connect(
            lambda: self.navigate(5)
        )

        layout.addWidget(
            settings
        )

        self.buttons.append(
            settings
        )

        layout.addStretch()

        # ----------------------------------------------------
        # Footer
        # ----------------------------------------------------

        status = QLabel(
            "●  SYSTEM SECURE"
        )

        status.setObjectName(
            "StatusGreen"
        )

        version = QLabel(
            "NeuroFence • v0.1.0"
        )

        version.setObjectName(
            "VersionLabel"
        )

        layout.addWidget(status)
        layout.addWidget(version)

        if self.buttons:
            self.buttons[0].setChecked(
                True
            )

    def navigate(self, index):

        for i, button in enumerate(
            self.buttons
        ):

            button.setChecked(
                i == index
            )

        self.navigation_callback(
            index
        )


# ============================================================
# TOP BAR
# ============================================================

class TopBar(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName(
            "TopBar"
        )

        self.setFixedHeight(
            64
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            24,
            0,
            24,
            0,
        )

        title_layout = QVBoxLayout()

        title_layout.setSpacing(1)

        self.title = QLabel(
            "Security Overview"
        )

        self.title.setObjectName(
            "TopTitle"
        )

        self.subtitle = QLabel(
            "Model security monitoring"
        )

        self.subtitle.setObjectName(
            "TopSubtitle"
        )

        title_layout.addWidget(
            self.title
        )

        title_layout.addWidget(
            self.subtitle
        )

        layout.addLayout(
            title_layout
        )

        layout.addStretch()

        badge = QLabel(
            "●  SYSTEM SECURE"
        )

        badge.setObjectName(
            "SecureBadge"
        )

        layout.addWidget(
            badge
        )

    def set_page_title(
        self,
        title,
        subtitle,
    ):

        self.title.setText(
            title
        )

        self.subtitle.setText(
            subtitle
        )


# ============================================================
# DASHBOARD PAGE
# ============================================================

class DashboardPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            28,
            26,
            28,
            28,
        )

        layout.setSpacing(16)

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        title = QLabel(
            "Dashboard"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Monitor the security posture of your language model."
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ----------------------------------------------------
        # Cards
        # ----------------------------------------------------

        cards = QHBoxLayout()

        cards.setSpacing(12)

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

        cards.addWidget(
            self.model_card
        )

        cards.addWidget(
            self.scan_card
        )

        cards.addWidget(
            self.threat_card
        )

        cards.addWidget(
            self.status_card
        )

        layout.addLayout(
            cards
        )

        # ----------------------------------------------------
        # Lower section
        # ----------------------------------------------------

        lower = QHBoxLayout()

        lower.setSpacing(14)

        self.activity_panel = (
            ActivityPanel()
        )

        threat_panel = QFrame()

        threat_panel.setObjectName(
            "Panel"
        )

        threat_layout = QVBoxLayout(
            threat_panel
        )

        threat_layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        threat_title = QLabel(
            "Threat Assessment"
        )

        threat_title.setObjectName(
            "PanelTitle"
        )

        threat_subtitle = QLabel(
            "Current model security score"
        )

        threat_subtitle.setObjectName(
            "PanelSubtitle"
        )

        self.threat_gauge = ThreatGauge(
            0
        )

        threat_layout.addWidget(
            threat_title
        )

        threat_layout.addWidget(
            threat_subtitle
        )

        threat_layout.addWidget(
            self.threat_gauge,
            1,
        )

        lower.addWidget(
            self.activity_panel,
            3,
        )

        lower.addWidget(
            threat_panel,
            2,
        )

        layout.addLayout(
            lower,
            1,
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        self.scan_status = (
            ScanStatus()
        )

        layout.addWidget(
            self.scan_status
        )

    # --------------------------------------------------------
    # Dashboard update
    # --------------------------------------------------------

    def update_model(
        self,
        model_name,
    ):

        self.model_card.set_value(
            model_name
        )

        self.model_card.description_label.setText(
            "Model successfully loaded"
        )

        self.activity_panel.add_activity(
            f"Model selected: {model_name}"
        )

        self.scan_status.set_status(
            "● Model ready for security scanning"
        )

    def update_scan_count(
        self,
        count,
    ):

        self.scan_card.set_value(
            count
        )

    def update_threat_score(
        self,
        score,
    ):

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


# ============================================================
# MODEL LOADER PAGE
# ============================================================

class ModelLoaderPage(QWidget):

    def __init__(
        self,
        dashboard_page=None,
        parent=None,
    ):

        super().__init__(parent)

        # Dashboard reference
        self.dashboard_page = (
            dashboard_page
        )

        # STEP 3
        # Create the validator
        self.validator = (
            ModelValidator()
        )

        self.selected_model_path = ""

        self.build_ui()

    # ========================================================
    # BUILD UI
    # ========================================================

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            28,
            26,
            28,
            28,
        )

        layout.setSpacing(16)

        # ----------------------------------------------------
        # Page header
        # ----------------------------------------------------

        title = QLabel(
            "Model Loader"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Select and validate an LLM before starting security analysis."
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        subtitle.setWordWrap(True)

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # ----------------------------------------------------
        # Model directory panel
        # ----------------------------------------------------

        directory_panel = QFrame()

        directory_panel.setObjectName(
            "Panel"
        )

        directory_layout = QVBoxLayout(
            directory_panel
        )

        directory_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        directory_layout.setSpacing(12)

        directory_title = QLabel(
            "MODEL DIRECTORY"
        )

        directory_title.setObjectName(
            "SectionLabel"
        )

        directory_layout.addWidget(
            directory_title
        )

        # ----------------------------------------------------
        # Path row
        # ----------------------------------------------------

        path_row = QHBoxLayout()

        path_row.setSpacing(10)

        self.path_input = QLineEdit()

        self.path_input.setPlaceholderText(
            "Select a local model directory..."
        )

        self.path_input.setReadOnly(
            True
        )

        self.path_input.setMinimumHeight(
            42
        )

        path_row.addWidget(
            self.path_input,
            1,
        )

        # STEP 4
        # Browse button
        self.browse_button = QPushButton(
            "Browse"
        )

        self.browse_button.setObjectName(
            "PrimaryButton"
        )

        self.browse_button.setMinimumHeight(
            42
        )

        self.browse_button.setMinimumWidth(
            110
        )

        self.browse_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.browse_button.clicked.connect(
            self.browse_model
        )

        path_row.addWidget(
            self.browse_button
        )

        directory_layout.addLayout(
            path_row
        )

        # ----------------------------------------------------
        # Validate button
        # ----------------------------------------------------

        self.validate_button = QPushButton(
            "Validate Model"
        )

        self.validate_button.setObjectName(
            "PrimaryButton"
        )

        self.validate_button.setMinimumHeight(
            44
        )

        self.validate_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.validate_button.setEnabled(
            False
        )

        self.validate_button.clicked.connect(
            self.validate_model
        )

        directory_layout.addWidget(
            self.validate_button
        )

        layout.addWidget(
            directory_panel
        )

        # ----------------------------------------------------
        # Validation result panel
        # ----------------------------------------------------

        result_panel = QFrame()

        result_panel.setObjectName(
            "Panel"
        )

        result_layout = QVBoxLayout(
            result_panel
        )

        result_layout.setContentsMargins(
            22,
            20,
            22,
            20,
        )

        result_layout.setSpacing(9)

        result_title = QLabel(
            "Model Validation"
        )

        result_title.setObjectName(
            "PanelTitle"
        )

        result_description = QLabel(
            "NeuroFence checks the selected model directory "
            "before security analysis."
        )

        result_description.setObjectName(
            "PanelSubtitle"
        )

        result_description.setWordWrap(
            True
        )

        result_layout.addWidget(
            result_title
        )

        result_layout.addWidget(
            result_description
        )

        result_layout.addSpacing(
            10
        )

        # ----------------------------------------------------
        # Status lines
        # ----------------------------------------------------

        self.directory_status = QLabel(
            "○ Directory not selected"
        )

        self.config_status = QLabel(
            "○ config.json not checked"
        )

        self.weights_status = QLabel(
            "○ Model weights not checked"
        )

        self.tokenizer_status = QLabel(
            "○ Tokenizer not checked"
        )

        for label in (
            self.directory_status,
            self.config_status,
            self.weights_status,
            self.tokenizer_status,
        ):

            label.setObjectName(
                "PanelSubtitle"
            )

            result_layout.addWidget(
                label
            )

        result_layout.addSpacing(
            10
        )

        self.final_result = QLabel(
            "Waiting for model selection."
        )

        self.final_result.setObjectName(
            "PanelSubtitle"
        )

        self.final_result.setWordWrap(
            True
        )

        result_layout.addWidget(
            self.final_result
        )

        result_layout.addStretch()

        layout.addWidget(
            result_panel,
            1,
        )

    # ========================================================
    # STEP 4 — BROWSE MODEL
    # ========================================================

    def browse_model(self):

        directory = (
            QFileDialog.getExistingDirectory(
                self,
                "Select Model Directory",
            )
        )

        if not directory:
            return

        # Save selected path
        self.selected_model_path = (
            directory
        )

        # Display path
        self.path_input.setText(
            directory
        )

        # Enable validation
        self.validate_button.setEnabled(
            True
        )

        # Reset validation state
        self.directory_status.setText(
            "✓ Directory selected"
        )

        self.directory_status.setObjectName(
            "SuccessLabel"
        )

        self.config_status.setText(
            "○ config.json not checked"
        )

        self.config_status.setObjectName(
            "PanelSubtitle"
        )

        self.weights_status.setText(
            "○ Model weights not checked"
        )

        self.weights_status.setObjectName(
            "PanelSubtitle"
        )

        self.tokenizer_status.setText(
            "○ Tokenizer not checked"
        )

        self.tokenizer_status.setObjectName(
            "PanelSubtitle"
        )

        self.final_result.setText(
            "Click 'Validate Model' to inspect this directory."
        )

        self.final_result.setObjectName(
            "PanelSubtitle"
        )

        self.refresh_styles()

    # ========================================================
    # STEP 5 — VALIDATE MODEL
    # ========================================================

    def validate_model(self):

        if not self.selected_model_path:

            QMessageBox.warning(
                self,
                "No Model Selected",
                "Please select a model directory first.",
            )

            return

        self.validate_button.setEnabled(
            False
        )

        self.browse_button.setEnabled(
            False
        )

        self.validate_button.setText(
            "Validating..."
        )

        try:

            # ------------------------------------------------
            # Call ModelValidator
            # ------------------------------------------------

            result = (
                self.validator.validate(
                    self.selected_model_path
                )
            )

            # ------------------------------------------------
            # Config
            # ------------------------------------------------

            if result.config_found:

                self.config_status.setText(
                    "✓ config.json found"
                )

                self.config_status.setObjectName(
                    "SuccessLabel"
                )

            else:

                self.config_status.setText(
                    "✕ config.json not found"
                )

                self.config_status.setObjectName(
                    "ErrorLabel"
                )

            # ------------------------------------------------
            # Weights
            # ------------------------------------------------

            if result.weights_found:

                self.weights_status.setText(
                    "✓ Model weights found"
                )

                self.weights_status.setObjectName(
                    "SuccessLabel"
                )

            else:

                self.weights_status.setText(
                    "✕ Model weights not found"
                )

                self.weights_status.setObjectName(
                    "ErrorLabel"
                )

            # ------------------------------------------------
            # Tokenizer
            # ------------------------------------------------

            if result.tokenizer_found:

                self.tokenizer_status.setText(
                    "✓ Tokenizer files found"
                )

                self.tokenizer_status.setObjectName(
                    "SuccessLabel"
                )

            else:

                self.tokenizer_status.setText(
                    "⚠ Tokenizer files not found"
                )

                self.tokenizer_status.setObjectName(
                    "WarningLabel"
                )

            # ------------------------------------------------
            # VALID
            # ------------------------------------------------

            if result.valid:

                self.final_result.setText(
                    "✓ MODEL VALIDATION PASSED\n\n"
                    "The selected model contains the "
                    "required configuration and weight files."
                )

                self.final_result.setObjectName(
                    "SuccessLabel"
                )

                # =================================================
                # STEP 6 — UPDATE DASHBOARD
                # =================================================

                model_name = Path(
                    self.selected_model_path
                ).name

                if self.dashboard_page:

                    self.dashboard_page.update_model(
                        model_name
                    )

            # ------------------------------------------------
            # INVALID
            # ------------------------------------------------

            else:

                if result.errors:

                    errors = "\n".join(
                        f"• {error}"
                        for error in result.errors
                    )

                else:

                    errors = (
                        "• Model validation failed."
                    )

                self.final_result.setText(
                    "✕ MODEL VALIDATION FAILED\n\n"
                    + errors
                )

                self.final_result.setObjectName(
                    "ErrorLabel"
                )

            self.refresh_styles()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Validation Error",
                (
                    "An error occurred while "
                    "validating the model.\n\n"
                    f"{error}"
                ),
            )

        finally:

            self.validate_button.setEnabled(
                True
            )

            self.browse_button.setEnabled(
                True
            )

            self.validate_button.setText(
                "Validate Model"
            )

    # ========================================================
    # Refresh styles
    # ========================================================

    def refresh_styles(self):

        widgets = [
            self.directory_status,
            self.config_status,
            self.weights_status,
            self.tokenizer_status,
            self.final_result,
        ]

        for widget in widgets:

            widget.style().unpolish(
                widget
            )

            widget.style().polish(
                widget
            )

            widget.update()


# ============================================================
# PLACEHOLDER PAGE
# ============================================================

class PlaceholderPage(QWidget):

    def __init__(
        self,
        title,
        description,
        parent=None,
    ):

        super().__init__(parent)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            28,
            26,
            28,
            28,
        )

        layout.setSpacing(16)

        title_label = QLabel(
            title
        )

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

        panel = QFrame()

        panel.setObjectName(
            "Panel"
        )

        panel_layout = QVBoxLayout(
            panel
        )

        panel_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        message = QLabel(
            "This module will be connected "
            "to the NeuroFence security pipeline "
            "in a later stage."
        )

        message.setObjectName(
            "PanelSubtitle"
        )

        message.setWordWrap(
            True
        )

        panel_layout.addWidget(
            message
        )

        panel_layout.addStretch()

        layout.addWidget(
            panel,
            1,
        )


# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "NeuroFence — LLM Security Scanner"
        )

        self.resize(
            1240,
            780
        )

        self.setMinimumSize(
            1000,
            650
        )

        self.build_ui()

    # ========================================================
    # BUILD MAIN UI
    # ========================================================

    def build_ui(self):

        central = QWidget()

        central.setObjectName(
            "ContentArea"
        )

        root = QHBoxLayout(
            central
        )

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root.setSpacing(0)

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = Sidebar(
            self.change_page
        )

        root.addWidget(
            self.sidebar
        )

        # ----------------------------------------------------
        # Content
        # ----------------------------------------------------

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(0)

        # Top bar
        self.top_bar = TopBar()

        content_layout.addWidget(
            self.top_bar
        )

        # Pages
        self.page_stack = (
            QStackedWidget()
        )

        self.create_pages()

        content_layout.addWidget(
            self.page_stack,
            1,
        )

        root.addWidget(
            content,
            1,
        )

        self.setCentralWidget(
            central
        )

    # ========================================================
    # CREATE PAGES
    # ========================================================

    def create_pages(self):

        # ----------------------------------------------------
        # Dashboard
        # ----------------------------------------------------

        self.dashboard_page = (
            DashboardPage()
        )

        self.page_stack.addWidget(
            self.dashboard_page
        )

        # ----------------------------------------------------
        # Model Loader
        # ----------------------------------------------------

        self.model_loader_page = (
            ModelLoaderPage(
                dashboard_page=
                self.dashboard_page
            )
        )

        self.page_stack.addWidget(
            self.model_loader_page
        )

        # ----------------------------------------------------
        # Security Scan
        # ----------------------------------------------------

        self.page_stack.addWidget(
            PlaceholderPage(
                "Security Scan",
                "Analyze the selected model "
                "for poisoning, backdoors and "
                "suspicious behavior.",
            )
        )

        # ----------------------------------------------------
        # Activation Tracker
        # ----------------------------------------------------

        self.page_stack.addWidget(
            PlaceholderPage(
                "Activation Tracker",
                "Monitor model activations and "
                "identify suspicious activation patterns.",
            )
        )

        # ----------------------------------------------------
        # Reports
        # ----------------------------------------------------

        self.page_stack.addWidget(
            PlaceholderPage(
                "Reports",
                "Review and export NeuroFence "
                "security findings.",
            )
        )

        # ----------------------------------------------------
        # Settings
        # ----------------------------------------------------

        self.page_stack.addWidget(
            PlaceholderPage(
                "Settings",
                "Configure NeuroFence application "
                "preferences.",
            )
        )

    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    def change_page(
        self,
        page_index,
    ):

        if page_index < 0:
            return

        if page_index >= self.page_stack.count():
            return

        self.page_stack.setCurrentIndex(
            page_index
        )

        page_titles = {

            0: (
                "Security Overview",
                "Model security monitoring",
            ),

            1: (
                "Model Loader",
                "Select and validate a local LLM",
            ),

            2: (
                "Security Scan",
                "Analyze the selected model",
            ),

            3: (
                "Activation Tracker",
                "Monitor suspicious activations",
            ),

            4: (
                "Security Reports",
                "Review model security findings",
            ),

            5: (
                "Settings",
                "Configure NeuroFence",
            ),
        }

        if page_index in page_titles:

            title, subtitle = (
                page_titles[page_index]
            )

            self.top_bar.set_page_title(
                title,
                subtitle,
            )


# ============================================================
# CREATE MAIN WINDOW
# ============================================================

def create_main_window():

    """
    Function imported by main.py.
    """

    return MainWindow()