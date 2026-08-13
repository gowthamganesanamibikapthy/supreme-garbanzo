import urllib.request
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QListWidget, QPushButton, QInputDialog

class AuraDashboardHud(QWidget):
    def __init__(self, main_window_instance):
        super().__init__()
        self.main_app = main_window_instance
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(f"AURA Command Console [{self.main_app.username}]")
        self.resize(340, 420)
        
        layout = QVBoxLayout(self)
        
        # Skin hot-swapping configuration engine dropdown toggler
        skin_box = QHBoxLayout()
        skin_box.addWidget(QLabel("ACTIVE ENGINE SKIN:", self))
        self.skin_dropdown = QComboBox(self)
        self.skin_dropdown.addItems(["CYBER_HUD", "KAWAII_PET", "ZEN_OASIS"])
        self.skin_dropdown.setCurrentText(self.main_app.active_skin)
        self.skin_dropdown.currentTextChanged.connect(self.request_skin_change)
        skin_box.addWidget(self.skin_dropdown)
        layout.addLayout(skin_box)
        
        layout.addWidget(QLabel("Active Master Logs (Double-Click item to COMPLETE):", self))
        
        self.list_view = QListWidget(self)
        self.refresh_task_list_view()
        self.list_view.itemDoubleClicked.connect(self.complete_task_item)
        layout.addWidget(self.list_view)
        
        add_btn = QPushButton("+ Register New Milestone Target", self)
        add_btn.clicked.connect(self.add_task_item)
        layout.addWidget(add_btn)

    def refresh_task_list_view(self):
        self.list_view.clear()
        for task in self.main_app.todos:
            self.list_view.addItem(task)

    def request_skin_change(self, val):
        self.main_app.dispatch_api_call("/api/config/skin", "POST", {"username": self.main_app.username, "skin_name": val}, "UPDATE_SKIN")
        self.main_app.active_skin = val
        self.main_app.apply_button_aesthetics()

    def add_task_item(self):
        text, ok = QInputDialog.getText(self, 'Log Milestone', 'Enter task criteria payload:')
        if ok and text.strip():
            new_task = text.strip()
            self.main_app.dispatch_api_call("/api/tasks", "POST", {"username": self.main_app.username, "task_text": new_task}, "ADD_TASK")
            self.main_app.todos.append(new_task)
            self.refresh_task_list_view()

    def complete_task_item(self, item):
        text = item.text()
        self.main_app.dispatch_api_call("/api/tasks/complete", "POST", {"username": self.main_app.username, "task_text": text}, "COMPLETE_TASK")
        self.main_app.todos.remove(text)
        self.main_app.play_chime(high_pitch=True)
        self.refresh_task_list_view()
