#!/bin/bash
# linux: dois cliques (ou botão direito, executar como programa), ou no terminal: bash "Jogar no Linux.sh"
# na primeira vez cria o ambiente e instala o pygame
script=$(readlink -f "$0")
cd "$(dirname "$script")"

falhar() {
    echo
    echo "$1"
    read -r -p "aperte enter para fechar." _
    exit 1
}

# aberto por dois cliques não há terminal; abre um, para a instalação e os erros aparecerem
abrir_no_terminal() {
    [ -t 1 ] || [ -z "$DISPLAY$WAYLAND_DISPLAY" ] || [ "$1" = "--no-terminal" ] && return
    for terminal in "ptyxis --" "kgx --" "gnome-terminal --" "konsole -e" "xfce4-terminal -x" \
                    "mate-terminal -x" "x-terminal-emulator -e" "xterm -e"; do
        if command -v "${terminal%% *}" > /dev/null; then
            exec ${terminal} bash "$script" --no-terminal
        fi
    done
}

# o pygame 2.6.1 tem pacote pronto do python 3.8 ao 3.13
python_que_serve() {
    for candidato in python3.12 python3.13 python3.11 python3.10 python3; do
        if command -v "$candidato" > /dev/null &&
           "$candidato" -c "import sys; sys.exit(not (3, 8) <= sys.version_info[:2] <= (3, 13))" 2> /dev/null; then
            echo "$candidato"
            return
        fi
    done
}

if [ -x .venv/bin/python ] && .venv/bin/python -c "import pygame" 2> /dev/null; then
    exec .venv/bin/python main.py
fi

abrir_no_terminal "$1"
PY=$(python_que_serve)
[ -n "$PY" ] || falhar "não achei python de 3.8 a 3.13. instale o python 3.12 e rode de novo."

# se o pygame já está no python do computador, não instala nada
if "$PY" -c "import pygame" 2> /dev/null; then
    exec "$PY" main.py
fi

echo "primeira vez: preparando o jogo com $PY (precisa de internet)..."
rm -rf .venv
if "$PY" -m venv .venv 2> /dev/null && .venv/bin/pip install -r requirements.txt; then
    exec .venv/bin/python main.py
fi

# sem o módulo venv (comum no ubuntu), instala o pygame só para o usuário
rm -rf .venv
"$PY" -m pip install --user -r requirements.txt ||
    "$PY" -m pip install --user --break-system-packages -r requirements.txt ||
    falhar "não consegui instalar o pygame. no terminal: $PY -m pip install --user pygame==2.6.1"
exec "$PY" main.py
