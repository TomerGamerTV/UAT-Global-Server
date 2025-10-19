@echo off
setlocal
cd /d "%~dp0"
git pull --autostash -X ours --no-edit
python -m pip install -r requirements.txt
set UAT_AUTORESTART=1
python main.py
