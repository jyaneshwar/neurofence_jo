"""
NeuroFence dark security theme.

This module contains the application's central Qt stylesheet.
Keeping the theme separate from the main window makes it reusable
throughout the application.
"""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication


class DarkTheme:
    """Provides the NeuroFence dark security theme."""

    @staticmethod
    def stylesheet() -> str:
        """Return the application's global Qt stylesheet."""

        return """
        QWidget {
            background-color: #0B1120;
            color: #E5E7EB;
            font-family: "Segoe UI";
            font-size: 14px;
        }

        QMainWindow {
            background-color: #0B1120;
        }

        #Sidebar {
            background-color: #111827;
            border-right: 1px solid #1F2937;
        }

        #BrandTitle {
            color: #F9FAFB;
            font-size: 20px;
            font-weight: 700;
        }

        #BrandSubtitle {
            color: #6B7280;
            font-size: 11px;
        }

        #NavigationButton {
            background-color: transparent;
            color: #9CA3AF;
            border: none;
            border-radius: 8px;
            padding: 12px 16px;
            text-align: left;
        }

        #NavigationButton:hover {
            background-color: #1F2937;
            color: #F9FAFB;
        }

        #NavigationButton:checked {
            background-color: #172554;
            color: #60A5FA;
        }

        #ContentArea {
            background-color: #0B1120;
        }

        #PageTitle {
            color: #F9FAFB;
            font-size: 26px;
            font-weight: 700;
        }

        #PageSubtitle {
            color: #6B7280;
            font-size: 13px;
        }

        #StatusBadge {
            background-color: #052E16;
            color: #4ADE80;
            border: 1px solid #166534;
            border-radius: 14px;
            padding: 6px 12px;
        }

        #PlaceholderCard {
            background-color: #111827;
            border: 1px solid #1F2937;
            border-radius: 12px;
        }

        #PlaceholderTitle {
            color: #E5E7EB;
            font-size: 18px;
            font-weight: 600;
        }

        #PlaceholderText {
            color: #6B7280;
            font-size: 13px;
        }

        QScrollArea {
            border: none;
            background-color: transparent;
        }

        QScrollBar:vertical {
            background-color: #111827;
            width: 8px;
            margin: 0;
        }

        QScrollBar::handle:vertical {
            background-color: #374151;
            border-radius: 4px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #4B5563;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }
        """

    @classmethod
    def apply(cls, application: QApplication) -> None:
        """Apply the NeuroFence theme to the application."""

        application.setStyle("Fusion")
        application.setStyleSheet(cls.stylesheet())

        font = QFont("Segoe UI", 10)
        application.setFont(font)