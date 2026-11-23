#!/bin/bash
# macos: dois cliques. na primeira vez cria o ambiente e instala o pygame
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
    PY=$(command -v python3.12 || command -v /opt/homebrew/opt/python@3.12/bin/python3.12 || command -v python3)
    "$PY" -m venv .venv && .venv/bin/pip install -r requirements.txt
fi
.venv/bin/python main.py
