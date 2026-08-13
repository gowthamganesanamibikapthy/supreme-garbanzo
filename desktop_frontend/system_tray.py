from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction

class WindowsSystemTrayManager(QSystemTrayIcon):
    def __init__(self, parent_window):
        # Fallback to standard native icons if branding artwork bundles aren't active
        super().__init__(QIcon.fromTheme("application-x-executable"), parent_window)
        self.parent = parent_window
        self.init_context_menu()

    def init_context_menu(self):
        menu = QMenu()
        
        # UI Visibilities controls toggle switches
        show_action = QAction("Maximize Overlays", self)
        show_action.triggered.connect(self.parent.show)
        menu.addAction(show_action)
        
        hide_action = QAction("Minimize to Tray", self)
        hide_action.triggered.connect(self.parent.hide)
        menu.addAction(hide_action)
        
        menu.addSeparator()
        
        # Shut down script loop
        exit_action = QAction("Hard Terminate Product", self)
        exit_action.triggered.connect(lambda: bytes(exit(0)))
        menu.addAction(exit_action)
        
        self.setContextMenu(menu)
        self.setToolTip("AURA: Premium Core Engine")
