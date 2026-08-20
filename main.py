"""
NeuroFence
LLM Weight Poisoning & Backdoor Scanner

Application entry point.
"""

import sys

from PyQt6.QtWidgets import QApplication

from desktop_ui.themes.dark_theme import DarkTheme
from desktop_ui.ui.main_window import create_main_window


def main() -> int:
    """Start the NeuroFence desktop application."""

    application = QApplication(sys.argv)

    DarkTheme.apply(application)

    window = create_main_window()
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())