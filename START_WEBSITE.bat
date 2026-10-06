@echo off
cd /d "%~dp0"
start "" http://127.0.0.1:5000
python -m pip install -r requirements.txt
python web_app.py
pause
