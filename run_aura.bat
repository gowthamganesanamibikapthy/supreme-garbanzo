@echo off
title AURA Production Engine Orchestration Launcher
echo Initializing AURA Eco-System Microservices...

echo Starting Backend Cloud Service Core (FastAPI)...
start /B cmd /c "cd core_backend && python app_service.py"

echo Waiting for database network handshakes to settle...
timeout /t 3 /nobreak >nul

echo Launching Frontend Vector Graphical Client Overlay (PyQt6)...
cd desktop_frontend
start "" python main_client.py

echo Modules deployed. Operational.
exit
