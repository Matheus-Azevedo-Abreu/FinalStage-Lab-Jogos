import math
import time
import configuracoes as cfg
import graficos
import mecanismos
import efeitos

# o cenário de cada autor (docs/historia.md), posto onde o quebra-cabeça
# acontece. só desenha. os objetos "vivos" mostram o estado do andar: o
# relógio do quaresma marca a hora de verdade, os monitores da cássia mostram
# o que cada câmera vê, a lousa do aníbal diz quais botões do canal já valem


def arte_de(objeto):
    # o objeto recortado do fundo escurece como ele
    return graficos.escurecida(objeto["arte"], cfg.escurecer_fundo)


def posicao(objeto, arte):
    # de pé no chão da célula, ou pendurado a partir do alto dela
    x = objeto["coluna"] * cfg.tile + objeto.get("dx", 0)
    if objeto.get("parede"):
        return x, objeto["linha"] * cfg.tile + objeto.get("dy", 0)
    return x, (objeto["linha"] + 1) * cfg.tile - arte.height + cfg.pe_do_cenario + objeto.get("dy", 0)


def desenhar_ponteiros(x, y):
    # as doze marcas e os três ponteiros, na hora que o computador marca
    cx, cy = x + cfg.centro_do_relogio[0], y + cfg.centro_do_relogio[1]
    raio = cfg.raio_do_relogio
    for hora in range(12):
        angulo = math.radians(hora * 30)
        dx, dy = math.sin(angulo), -math.cos(angulo)
        graficos.linha_no_mundo(cfg.cor_ponteiro, cx + dx * (raio - 2), cy + dy * (raio - 2), cx + dx * raio, cy + dy * raio)
    agora = time.localtime()
    ponteiros = (((agora.tm_hour % 12 + agora.tm_min / 60) * 30, raio * 0.5, cfg.cor_ponteiro),
                 ((agora.tm_min + agora.tm_sec / 60) * 6, raio * 0.8, cfg.cor_ponteiro),
                 (agora.tm_sec * 6, raio * 0.85, cfg.cor_segundos))
    for graus, comprimento, cor in ponteiros:
        angulo = math.radians(graus)
        graficos.linha_no_mundo(cor, cx, cy, cx + math.sin(angulo) * comprimento, cy - math.cos(angulo) * comprimento)


def desenhar_telas(fase, x, y):
    # um monitor por câmera, da esquerda para a direita do andar
    cameras = sorted(fase["cameras"], key=lambda camera: camera["x"])
    quadro = int(efeitos.relogio["tempo"] * 8)
    for n, (tx, ty) in enumerate(cfg.telas_dos_monitores):
        if n < len(cameras):
            estado = {"desligada": "estatica"}.get(cameras[n]["estado"], cameras[n]["estado"])
            passo = quadro % 3 if estado == "estatica" else (quadro // 2 % 2 if estado == "alerta" else quadro // 2 % 14)
            graficos.superficie_no_mundo(graficos.tela_de_monitor(estado, n + 1, passo), x + tx, y + ty)
        elif n == cfg.tela_de_estatica:
            graficos.superficie_no_mundo(graficos.tela_de_monitor("estatica", 0, quadro % 3), x + tx, y + ty)


def desenhar_giz(fase, canal, x, y):
    # o esquema da sala, a giz: a marca do canal, um quadrado por controle
    # (cheio quando ele já vale), a seta e a porta, que se abre no desenho
    ax, ay, largura, altura = cfg.area_da_lousa
    controles = sorted([c for c in fase["botoes"] + fase["alavancas"] if c["canal"] == canal], key=lambda c: c["x"])
    regra = fase["regras"].get(canal, "qualquer")
    forma = fase["marcas"].get(canal)
    if forma is not None:
        graficos.superficie_no_mundo(graficos.marca_de_canal(forma), x + ax + 2, y + ay + 2)
    total = len(controles) * 9 + max(0, len(controles) - 1) * 4 + 9 + 9
    px = x + ax + (largura - total) // 2
    py = y + ay + 15
    for n, controle in enumerate(controles):
        vale = mecanismos.controle_ativo(controle, regra)
        graficos.retangulo_no_mundo(cfg.cor_giz if vale else cfg.cor_giz_apagado, px, py, 9, 9)
        if not vale:
            graficos.retangulo_no_mundo((27, 24, 48), px + 1, py + 1, 7, 7)
        px = px + 9
        if n < len(controles) - 1:
            graficos.retangulo_no_mundo(cfg.cor_giz_apagado, px + 1, py + 4, 2, 1)
            px = px + 4
    ativo = mecanismos.canal_ativo(fase, canal)
    cor = cfg.cor_giz if ativo else cfg.cor_giz_apagado
    graficos.retangulo_no_mundo(cor, px + 2, py + 4, 5, 1)
    graficos.retangulo_no_mundo(cor, px + 5, py + 3, 1, 3)
    px = px + 9
    # a porta: fechada, a folha cheia; aberta, só o batente
    graficos.retangulo_no_mundo(cor, px, py - 3, 8, 13)
    graficos.retangulo_no_mundo((27, 24, 48), px + 1, py - 2, 6 if ativo else 1, 12)


def desenhar_lugares(fase):
    # o lugar de onde cada caixa saiu, marcado no chão: a ordem da selene
    arte = graficos.imagem("lugar-da-caixa.png")
    if arte is None or not fase["marcar_lugares"]:
        return
    for x, y in fase["lugares"]:
        graficos.no_mundo(arte, x, y)


def desenhar(fase):
    # atrás das peças do andar e de todo mecanismo
    for objeto in fase["cenario"]:
        arte = arte_de(objeto)
        if arte is None:
            continue
        x, y = posicao(objeto, arte)
        graficos.no_mundo(arte, x, y)
        if objeto.get("vivo") == "relogio":
            desenhar_ponteiros(x, y)
        elif objeto.get("vivo") == "monitores":
            desenhar_telas(fase, x, y)
        elif objeto.get("vivo") == "lousa":
            desenhar_giz(fase, objeto["canal"], x, y)
    desenhar_lugares(fase)


def preparar(fase):
    # tudo o que o cenário do andar desenha, pronto antes do laço
    for objeto in fase["cenario"]:
        arte_de(objeto)
        if objeto.get("vivo") == "monitores":
            for numero in range(len(cfg.telas_dos_monitores) + 1):
                for quadro in range(14):
                    graficos.tela_de_monitor("vigiando", numero, quadro)
                for quadro in range(3):
                    graficos.tela_de_monitor("estatica", numero, quadro)
                for quadro in range(2):
                    graficos.tela_de_monitor("alerta", numero, quadro)
    graficos.imagem("lugar-da-caixa.png")
