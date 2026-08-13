import sys
import random
import time
import urllib.request
import json
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QMessageBox
from PyQt6.QtGui import QPainter

# Import specialized visual frontend sub-components
from paint_engine import VectorPaintEngine
from system_tray import WindowsSystemTrayManager
from dashboard_hud import AuraDashboardHud
from app import AsyncVoiceEngine, APIWorker # Uses background thread components from main framework module

class AuraCloudPremiumWidget(QWidget):
    def __init__(self, validated_user):
        super().__init__()
        self.username = validated_user
        self.todos = []
        self.voice_pool = []
        self.network_workers = []
        
        # Initialize rendering engine component
        self.paint_shader = VectorPaintEngine()
        self.active_skin = "CYBER_HUD"
        self.rotation_phase = 0.0
        self.glow_intensity = 40
        self.glow_direction = 1
        self.last_water_check = time.time()

        self.init_ui()
        self.sync_with_cloud_backend()
        
        # Deploy native operational components hooks configuration layout properties
        self.tray_icon = WindowsSystemTrayManager(self)
        self.tray_icon.show()
        
        # Unified Master execution clock loops
        self.master_loop = QTimer(self)
        self.master_loop.timeout.connect(self.system_process_tick)
        self.master_loop.start(33)

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(200, 245)
        
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 212, int(screen.height() / 3))
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addSpacing(185)
        
        self.action_btn = QPushButton("CORE LINK", self)
        self.apply_button_aesthetics()
        self.action_btn.clicked.connect(self.trigger_boredom_interlocking)
        self.main_layout.addWidget(self.action_btn)
        self.drag_position = QPoint()

    def apply_button_aesthetics(self):
        if self.active_skin == "CYBER_HUD":
            self.action_btn.setText("BOREDOM PURGE")
            self.action_btn.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #001122, stop:1 #00ffcc); color: white; border: 2px solid #00ffcc; border-radius: 6px; font-weight: bold; font-family: 'Consolas'; font-size: 11px;")
        elif self.active_skin == "KAWAII_PET":
            self.action_btn.setText("PET COMPANION")
            self.action_btn.setStyleSheet("background-color: #FFB6C1; color: white; border: 2px solid #FF69B4; border-radius: 8px; font-weight: bold; font-family: 'Segoe UI'; font-size: 11px;")
        elif self.active_skin == "ZEN_OASIS":
            self.action_btn.setText("ALIGN MIND")
            self.action_btn.setStyleSheet("background-color: #2E4040; color: #E0EEE0; border: 1px solid #708090; border-radius: 4px; font-family: 'Georgia'; font-size: 11px;")

    def dispatch_api_call(self, endpoint, method="GET", data=None, action_id=""):
        worker = APIWorker(endpoint, method, data, action_id)
        worker.response_received.connect(self.handle_api_response)
        self.network_workers.append(worker)
        worker.start()

    def sync_with_cloud_backend(self):
        self.dispatch_api_call("/api/tasks/fetch", "POST", {"username": self.username, "skin_name": ""}, action_id="FETCH_TASKS")
        self.dispatch_api_call("/api/config/get-skin", "POST", {"username": self.username, "skin_name": ""}, action_id="FETCH_SKIN")

    def handle_api_response(self, action_id, response):
        if not response["success"]: 
            return
        payload = response["payload"]
        if action_id == "FETCH_TASKS":
            self.todos = [item["task_text"] for item in payload]
        elif action_id == "FETCH_SKIN":
            self.active_skin = payload["skin_name"]
            self.apply_button_aesthetics()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.rotation_phase += 0.04
        self.glow_intensity += self.glow_direction * 2
        if self.glow_intensity > 80 or self.glow_intensity < 25: 
            self.glow_direction *= -1
        self.paint_shader.render(painter, self.active_skin, self.rotation_phase, self.glow_intensity)

    def say(self, text):
        worker = AsyncVoiceEngine(text, rate=145 if self.active_skin == "ZEN_OASIS" else 175)
        self.voice_pool.append(worker)
        worker.start()

    def system_process_tick(self):
        now_ts = time.time()
        if now_ts - self.last_water_check >= 1200:
            self.last_water_check = now_ts
            txt = "Time for a water break!"
            self.say(txt)
        self.update()

    def trigger_boredom_interlocking(self):
        self.open_global_dashboard_hud()

    def open_global_dashboard_hud(self):
        self.dashboard = AuraDashboardHud(self)
        self.dashboard.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.open_global_dashboard_hud()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 212, self.y())

if __name__ == "__main__":
    # Fallback launching loop pipeline profile hook interface
    app = QApplication(sys.argv)
    user_name, ok1 = QInputDialog.getText(None, "Authentication Portal", "Username:")
    if ok1 and user_name.strip():
        toy = AuraCloudPremiumWidget(user_name.strip())
        toy.show()
        sys.exit(app.exec())
