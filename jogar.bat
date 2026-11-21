@echo off
rem windows: dois cliques. na primeira vez cria o ambiente e instala o pygame
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    py -3.12 -m venv .venv || python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
)
.venv\Scripts\python main.py
