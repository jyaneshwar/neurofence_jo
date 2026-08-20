"""
NeuroFence visual theme.
"""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication


class DarkTheme:
    """Professional dark theme for NeuroFence."""

    @staticmethod
    def stylesheet() -> str:
        return """
        /* =========================================================
           GLOBAL
           ========================================================= */

        QWidget {
            background-color: #0A0D12;
            color: #E6EAF0;
            font-family: "Segoe UI";
            font-size: 13px;
        }

        QMainWindow {
            background-color: #0A0D12;
        }

        /* =========================================================
           SIDEBAR
           ========================================================= */

        #Sidebar {
            background-color: #0D1117;
            border-right: 1px solid #20262F;
        }

        #BrandTitle {
            color: #F3F5F7;
            font-size: 21px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        #BrandSubtitle {
            color: #697380;
            font-size: 9px;
            font-weight: 600;
            letter-spacing: 1.5px;
        }

        #SectionLabel {
            color: #59636F;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1.4px;
            padding-left: 8px;
        }

        #NavigationButton {
            background-color: transparent;
            color: #8D97A4;
            border: none;
            border-radius: 7px;
            padding: 11px 13px;
            text-align: left;
            font-size: 13px;
        }

        #NavigationButton:hover {
            background-color: #161C24;
            color: #E8ECF1;
        }

        #NavigationButton:checked {
            background-color: #172231;
            color: #6DB3FF;
            border-left: 2px solid #4A9EFF;
        }

        #VersionLabel {
            color: #4E5864;
            font-size: 10px;
        }

        /* =========================================================
           TOP BAR
           ========================================================= */

        #TopBar {
            background-color: #0D1117;
            border-bottom: 1px solid #20262F;
        }

        #TopTitle {
            color: #F0F3F6;
            font-size: 15px;
            font-weight: 600;
        }

        #TopSubtitle {
            color: #697380;
            font-size: 11px;
        }

        #SecureBadge {
            background-color: #10251A;
            color: #65D391;
            border: 1px solid #214C31;
            border-radius: 12px;
            padding: 5px 11px;
            font-size: 10px;
            font-weight: 600;
        }

        /* =========================================================
           CONTENT
           ========================================================= */

        #ContentArea {
            background-color: #0A0D12;
        }

        #PageTitle {
            color: #F1F4F7;
            font-size: 25px;
            font-weight: 650;
        }

        #PageSubtitle {
            color: #727C88;
            font-size: 12px;
        }

        /* =========================================================
           CARDS
           ========================================================= */

        #InfoCard {
            background-color: #10151C;
            border: 1px solid #202731;
            border-radius: 10px;
        }

        #InfoCard:hover {
            border: 1px solid #2C3540;
        }

        #CardLabel {
            color: #68727E;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.8px;
        }

        #CardValue {
            color: #F0F3F6;
            font-size: 22px;
            font-weight: 650;
        }

        #CardDescription {
            color: #59636F;
            font-size: 10px;
        }

        /* =========================================================
           PANELS
           ========================================================= */

        #Panel {
            background-color: #10151C;
            border: 1px solid #202731;
            border-radius: 10px;
        }

        #PanelTitle {
            color: #E7EBEF;
            font-size: 14px;
            font-weight: 600;
        }

        #PanelSubtitle {
            color: #66717D;
            font-size: 10px;
        }

        #EmptyState {
            color: #535D69;
            font-size: 12px;
        }

        /* =========================================================
           PRIMARY BUTTON
           ========================================================= */

        #PrimaryButton {
            background-color: #2F81D8;
            color: white;
            border: none;
            border-radius: 7px;
            padding: 10px 18px;
            font-size: 12px;
            font-weight: 600;
        }

        #PrimaryButton:hover {
            background-color: #3C91E8;
        }

        #PrimaryButton:pressed {
            background-color: #246DB8;
        }

        /* =========================================================
           SECONDARY BUTTON
           ========================================================= */

        #SecondaryButton {
            background-color: #151B23;
            color: #AEB7C2;
            border: 1px solid #29313B;
            border-radius: 7px;
            padding: 9px 15px;
        }

        #SecondaryButton:hover {
            background-color: #1B222C;
            color: #E6EAF0;
        }

        /* =========================================================
           STATUS
           ========================================================= */

        #StatusGreen {
            color: #65D391;
        }

        #StatusAmber {
            color: #E6B85C;
        }

        #StatusRed {
            color: #E36A6A;
        }

        /* =========================================================
           SCROLLBAR
           ========================================================= */

        QScrollBar:vertical {
            background: #0A0D12;
            width: 7px;
            border: none;
        }

        QScrollBar::handle:vertical {
            background: #29313B;
            border-radius: 3px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background: #37414D;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """

    @classmethod
    def apply(cls, application: QApplication) -> None:
        """Apply the NeuroFence theme."""

        application.setStyle("Fusion")
        application.setStyleSheet(cls.stylesheet())

        application.setFont(QFont("Segoe UI", 10))