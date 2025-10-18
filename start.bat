@echo off
setlocal

git fetch --all
git reset --hard

git pull
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python main.py
