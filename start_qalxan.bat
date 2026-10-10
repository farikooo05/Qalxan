@echo off
rem Double-click to start Qalxan and open the dashboard.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Setting up Python environment, first run only...
  python -m venv .venv
  .venv\Scripts\python.exe -m pip install -r requirements.txt
)
if not exist "models\qalxan.joblib" .venv\Scripts\python.exe scripts\train.py
start "" http://localhost:8000
.venv\Scripts\python.exe -m uvicorn qalxan.api:app --host 0.0.0.0 --port 8000
pause
