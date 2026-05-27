# =============================================================================
# main.py
# =============================================================================
#
# NexusView - Enterprise Edition
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

# -----------------------------------------------------------------------------
# LOCAL UI IMPORTS
# -----------------------------------------------------------------------------

from ui_sidebar import SidebarWidget
from ui_workspace import WorkspaceWidget
from ui_file_browser import FileBrowserWidget


# =============================================================================
# MAIN WINDOW
# =============================================================================

class ScrcpyEnterprise(QMainWindow):
    """
    Main application window.
    """

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(self):
        """
        Initialize main application window.
        """

        super().__init__()

        # ---------------------------------------------------------------------
        # WINDOW CONFIGURATION
        # ---------------------------------------------------------------------

        self.setWindowTitle(
            "NexusView - Enterprise Edition"
        )

        self.setMinimumSize(1100, 700)

        # ---------------------------------------------------------------------
        # BUILD UI
        # ---------------------------------------------------------------------

        self.build_ui()

        # ---------------------------------------------------------------------
        # SIGNAL CONNECTIONS
        # ---------------------------------------------------------------------

        self.connect_sidebar_signals()

        # ---------------------------------------------------------------------
        # APPLY THEME
        # ---------------------------------------------------------------------

        self.apply_global_theme()

    # =========================================================================
    # BUILD USER INTERFACE
    # =========================================================================

    def build_ui(self):
        """
        Assemble application layout.
        """

        # ---------------------------------------------------------------------
        # CENTRAL WIDGET
        # ---------------------------------------------------------------------

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        # ---------------------------------------------------------------------
        # MAIN LAYOUT
        # ---------------------------------------------------------------------

        self.main_layout = QHBoxLayout(central_widget)

        self.main_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        self.main_layout.setSpacing(12)

        # ---------------------------------------------------------------------
        # SIDEBAR
        # ---------------------------------------------------------------------

        self.sidebar_widget = SidebarWidget()

        self.sidebar_widget.setFixedWidth(320)

        # ---------------------------------------------------------------------
        # STACKED CONTENT AREA
        # ---------------------------------------------------------------------

        self.stacked_widget = QStackedWidget()

        self.stacked_widget.setObjectName(
            "workspaceWidget"
        )

        # ---------------------------------------------------------------------
        # WORKSPACE PAGE
        # ---------------------------------------------------------------------

        self.workspace_widget = WorkspaceWidget(
            sidebar_widget=self.sidebar_widget
        )

        # ---------------------------------------------------------------------
        # FILE BROWSER PAGE
        # ---------------------------------------------------------------------

        self.file_browser_widget = FileBrowserWidget()

        # ---------------------------------------------------------------------
        # ADD PAGES TO STACK
        # ---------------------------------------------------------------------

        self.stacked_widget.addWidget(
            self.workspace_widget
        )

        self.stacked_widget.addWidget(
            self.file_browser_widget
        )

        # ---------------------------------------------------------------------
        # ADD TO MAIN LAYOUT
        # ---------------------------------------------------------------------

        self.main_layout.addWidget(
            self.sidebar_widget
        )

        self.main_layout.addWidget(
            self.stacked_widget
        )

    # =========================================================================
    # CONNECT SIDEBAR SIGNALS
    # =========================================================================

    def connect_sidebar_signals(self):
        """
        Connect sidebar buttons/signals.
        """

        # ---------------------------------------------------------------------
        # FILE BROWSER BUTTON
        # ---------------------------------------------------------------------

        if hasattr(
            self.sidebar_widget,
            "button_file_browser"
        ):

            self.sidebar_widget.button_file_browser.clicked.connect(
                self.show_file_browser
            )

    # =========================================================================
    # PAGE SWITCHING
    # =========================================================================

    def show_workspace(self):
        """
        Show streaming workspace.
        """

        self.stacked_widget.setCurrentIndex(0)

    def show_file_browser(self):
        """
        Show file browser page.
        """

        self.stacked_widget.setCurrentIndex(1)

    # =========================================================================
    # GLOBAL DARK THEME
    # =========================================================================

    def apply_global_theme(self):
        """
        Apply enterprise dark theme.
        """

        self.setStyleSheet("""

        QWidget {
            background-color: #181825;
            color: #cdd6f4;
            font-family: 'Segoe UI';
            font-size: 13px;
        }

        QWidget#sidebarWidget {
            background-color: #1e1e2e;
            border-radius: 14px;
        }

        QWidget#workspaceWidget {
            background-color: #1e1e2e;
            border-radius: 14px;
        }

        QLabel#sidebarTitle {
            font-size: 18px;
            font-weight: bold;
            color: #89b4fa;
        }

        QGroupBox {
            background-color: #181825;
            border: 1px solid #313244;
            border-radius: 12px;
            margin-top: 12px;
            padding-top: 14px;
            font-weight: 600;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 14px;
            padding: 0 6px;
            color: #89b4fa;
        }

        QPushButton {
            background-color: #313244;
            border: none;
            border-radius: 10px;
            padding: 10px;
            color: white;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #45475a;
        }

        QPushButton:pressed {
            background-color: #585b70;
        }

        QPushButton#pairButton {
            background-color: #89b4fa;
            color: #11111b;
        }

        QPushButton#pairButton:hover {
            background-color: #a6c8ff;
        }

        QPushButton#startStreamButton {
            background-color: #00c853;
            color: white;
            font-weight: bold;
        }

        QPushButton#startStreamButton:hover {
            background-color: #00e676;
        }

        QPushButton#stopStreamButton {
            background-color: #d50000;
            color: white;
            font-weight: bold;
        }

        QPushButton#stopStreamButton:hover {
            background-color: #ff1744;
        }

        QLineEdit,
        QComboBox,
        QTreeView {
            background-color: #11111b;
            border: 1px solid #313244;
            border-radius: 10px;
            padding: 8px;
            color: #cdd6f4;
        }

        QLineEdit:focus,
        QComboBox:focus {
            border: 1px solid #89b4fa;
        }

        QTabWidget::pane {
            border: 1px solid #313244;
            border-radius: 12px;
            background-color: #1e1e2e;
            top: -1px;
        }

        QTabBar::tab {
            background-color: #181825;
            color: #cdd6f4;
            padding: 10px 18px;
            margin-right: 4px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            min-width: 120px;
            font-weight: 600;
        }

        QTabBar::tab:selected {
            background-color: #89b4fa;
            color: #11111b;
        }

        QTreeView {
            border-radius: 12px;
            padding: 6px;
        }

        QHeaderView::section {
            background-color: #313244;
            color: #cdd6f4;
            padding: 6px;
            border: none;
        }

        QLabel#streamingPlaceholder,
        QLabel#recordingPlaceholder,
        QLabel#advancedPlaceholder {
            color: #6c7086;
            font-size: 16px;
            font-weight: 600;
        }

        """)


# =============================================================================
# APPLICATION ENTRY
# =============================================================================

def main():
    """
    Start application.
    """

    app = QApplication(sys.argv)

    window = ScrcpyEnterprise()

    window.show()

    sys.exit(app.exec())


# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == "__main__":
    main()