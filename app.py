import sys
import random
import time
import math
import urllib.request
import json
import pyttsx3
import winsound
from PyQt6.QtCore import Qt, QTimer, QPoint, QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QWidget, QInputDialog, QMessageBox, 
                             QPushButton, QVBoxLayout, QListWidget, QLabel, QComboBox, QHBoxLayout)
from PyQt6.QtGui import QPainter, QColor, QBrush, QRadialGradient, QPen, QPolygon

class AsyncVoiceEngine(QThread):
    def __init__(self, text, rate=165):
        super().__init__()
        self.text = text
        self.rate = rate

    def run(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.say(self.text)
            engine.runAndWait()
        except Exception: pass

class APIWorker(QThread):
    response_received = pyqtSignal(str, dict)

    def __init__(self, endpoint, method="GET", data=None, action_id=""):
        super().__init__()
        self.url = f"http://127.0.0.1:8000{endpoint}"
        self.method = method
        self.data = data
        self.action_id = action_id

    def run(self):
        try:
            req = urllib.request.Request(self.url, method=self.method)
            req.add_header('Content-Type', 'application/json')
            payload = json.dumps(self.data).encode('utf-8') if self.data else None
            
            with urllib.request.urlopen(req, data=payload, timeout=2) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                self.response_received.emit(self.action_id, {"success": True, "payload": res_data})
        except Exception as e:
            self.response_received.emit(self.action_id, {"success": False, "error": str(e)})

class AuraCloudPremiumWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.todos = []
        self.voice_pool = []
        self.network_workers = []
        
        self.active_skin = "CYBER_HUD"
        self.rotation_phase = 0.0
        self.is_blinking = False
        self.glow_direction = 1
        self.glow_intensity = 40
        
        self.last_water_check = time.time()
        self.last_todo_audit = time.time()
        
        self.copy_vault = {
            "CYBER_HUD": {
                "welcome": "Aura synchronized with cloud node. Perimeter secure.",
                "water": ["Telemetry notes main system requires fluid optimization. Drink H2O, Operator."],
                "block": ["Core objectives are stacking up. Complete a parameter block before launching distractions."]
            },
            "KAWAII_PET": {
                "welcome": "Yay, Aura is connected to the network! Let's work!",
                "water": ["Gulp gulp! Time for a magical water break, bestie!"],
                "break": ["No games yet! Prune down your messy chore list first!"]
            },
            "ZEN_OASIS": {
                "welcome": "Tranquility alignment initiated. Cloud network balanced.",
                "water": ["A focused spirit rests in a clean body. Consume fresh water."],
                "break": ["Fulfill your daily intentions before seeking outward distraction."]
            }
        }

        self.init_ui()
        self.sync_with_cloud_backend()
        self.play_chime(high_pitch=True)
        self.say(self.copy_vault[self.active_skin]["welcome"])

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

    def say(self, text):
        worker = AsyncVoiceEngine(text, rate=145 if self.active_skin == "ZEN_OASIS" else 175)
        self.voice_pool.append(worker)
        worker.start()

    def play_chime(self, high_pitch=False):
        try:
            if self.active_skin == "CYBER_HUD": 
                winsound.Beep(1000, 60) if high_pitch else winsound.Beep(500, 90)
            elif self.active_skin == "KAWAII_PET": 
                winsound.Beep(700, 80) if high_pitch else winsound.Beep(900, 50)
            elif self.active_skin == "ZEN_OASIS": 
                winsound.Beep(440, 180)
        except Exception: 
            pass

    def dispatch_api_call(self, endpoint, method="GET", data=None, action_id=""):
        worker = APIWorker(endpoint, method, data, action_id)
        worker.response_received.connect(self.handle_api_response)
        self.network_workers.append(worker)
        worker.start()

    def sync_with_cloud_backend(self):
        self.dispatch_api_call("/api/tasks", "GET", action_id="FETCH_TASKS")
        self.dispatch_api_call("/api/config/skin", "GET", action_id="FETCH_SKIN")

    def handle_api_response(self, action_id, response):
        if not response["success"]: 
            return
        payload = response["payload"]
        if action_id == "FETCH_TASKS":
            self.todos = [item["task_text"] for item in payload]
        elif action_id == "FETCH_SKIN":
            skin_name = payload["skin_name"]
            if skin_name != self.active_skin:
                self.active_skin = skin_name
                self.apply_button_aesthetics()
                self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        c = 100
        self.rotation_phase += 0.04
        self.glow_intensity += self.glow_direction * 2
        if self.glow_intensity > 80 or self.glow_intensity < 25: 
            self.glow_direction *= -1

        if self.active_skin == "CYBER_HUD":
            gradient = QRadialGradient(c, c, 80)
            gradient.setColorAt(0.0, QColor(0, 255, 204, self.glow_intensity))
            gradient.setColorAt(0.8, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(10, 10, 180, 180)
            painter.setPen(QPen(QColor(0, 255, 204, 180), 2))
            painter.drawEllipse(45, 45, 110, 110)

        elif self.active_skin == "KAWAII_PET":
            if random.random() < 0.02: 
                self.is_blinking = not self.is_blinking
            painter.setPen(QPen(QColor(255, 105, 180), 3))
            painter.setBrush(QBrush(QColor(255, 218, 224)))
            painter.drawEllipse(40, 50, 120, 95)
            if self.is_blinking:
                painter.setPen(QPen(QColor(40, 40, 40), 3))
                painter.drawLine(65, 92, 85, 92)
                painter.drawLine(115, 92, 135, 92)
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor(40, 40, 40)))
                painter.drawEllipse(65, 82, 18, 18)
                painter.drawEllipse(115, 82, 18, 18)

        elif self.active_skin == "ZEN_OASIS":
            painter.setBrush(Qt.BrushStyle.NoBrush)
            for i in range(1, 6):
                radius = i * 26
                painter.setPen(QPen(QColor(218, 165, 32, max(10, 200 - (i * 35))), 1))
                painter.drawEllipse(int(c - radius/2), int(c - radius/2), radius, radius)

    def system_process_tick(self):
        now_ts = time.time()
        if int(now_ts) % 5 == 0 and int(now_ts * 30) % 30 == 0:
            self.sync_with_cloud_backend()
        if now_ts - self.last_water_check >= 1200:
            self.last_water_check = now_ts
            txt = random.choice(self.copy_vault[self.active_skin]["water"])
            self.say(txt)
            QMessageBox.question(self, 'AURA Cloud Diagnostic', txt, QMessageBox.StandardButton.Ok)
        self.update()

    def trigger_boredom_interlocking(self):
        self.play_chime(high_pitch=True)
        if len(self.todos) >= 3:
            txt = self.copy_vault[self.active_skin]["break"][0]
            self.say(txt)
            QMessageBox.warning(self, "AURA Security Lockout", "Prune your pending task load to clear breaks.")
        else:
            breaks = ["Focus matrix locked. Stay concentrated for 10 minutes.", "Stand up and face away from the glare for 20 seconds."]
            chosen = random.choice(breaks)
            self.say(chosen)
            QMessageBox.information(self, "AURA Break Challenge", chosen)

    def open_global_dashboard_hud(self):
        self.hud = QWidget()
        self.hud.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.hud.setWindowTitle("AURA Command Hub")
        self.hud.resize(350, 420)
        
        layout = QVBoxLayout(self.hud)
        
        skin_box = QHBoxLayout()
        skin_box.addWidget(QLabel("WIDGET SKIN MATRIX:", self.hud))
        skin_dropdown = QComboBox(self.hud)
        skin_dropdown.addItems(["CYBER_HUD", "KAWAII_PET", "ZEN_OASIS"])
        skin_dropdown.setCurrentText(self.active_skin)
        
        def push_skin_update(val):
            self.dispatch_api_call("/api/config/skin", "POST", {"skin_name": val}, "UPDATE_SKIN")
            self.swap_theme_engine(val)
        
        skin_dropdown.currentTextChanged.connect(push_skin_update)
        skin_box.addWidget(skin_dropdown)
        layout.addLayout(skin_box)
        
        list_view = QListWidget(self.hud)
        for task in self.todos: 
            list_view.addItem(task)
        
        def finalize_task_item(item):
            text = item.text()
            self.dispatch_api_call("/api/tasks/complete", "POST", {"task_text": text}, "COMPLETE_TASK")
            self.todos.remove(text)
            self.play_chime(high_pitch=True)
            list_view.takeItem(list_view.row(item))
        
        list_view.itemDoubleClicked.connect(finalize_task_item)
        layout.addWidget(list_view)
        
        add_btn = QPushButton("+ Register New Milestone Target", self.hud)
        
        def write_new_target():
            text, ok = QInputDialog.getText(self.hud, 'Log Cloud Milestone', 'Enter task description:')
            if ok and text.strip():
                new_str = text.strip()
                self.dispatch_api_call("/api/tasks", "POST", {"task_text": new_str}, "ADD_TASK")
                self.todos.append(new_str)
                list_view.addItem(new_str)
                self.play_chime(high_pitch=True)
        
        add_btn.clicked.connect(write_new_target)
        layout.addWidget(add_btn)
        self.hud.show()

    def swap_theme_engine(self, skin_name):
        self.active_skin = skin_name
        self.apply_button_aesthetics()
        self.play_chime(high_pitch=True)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.open_global_dashboard_hud()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 212, self.y())if name == "main":app = QApplication(sys.argv)toy = AuraCloudPremiumWidget()toy.show()sys.exit(app.exec())