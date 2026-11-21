import math
import configuracoes as cfg
import jogador

# a visão que segue a íris: guarda só a posição, não desenha nem importa pygame

# canto superior esquerdo da visão, em px de mundo, e a largura do andar;
# adiante é a antecipação em curso, chao a altura do último apoio da íris
# foco: ponto do mundo que a visão segue no lugar da íris (os monitores do
# andar 8 mostram as câmeras), ou None
visao = {"x": 0.0, "y": 0.0, "largura_mundo": cfg.largura_fundo, "adiante": 0.0, "chao": 0.0,
         "vx": 0.0, "vy": 0.0, "foco": None}


def largura_visao():
    return cfg.largura_tela / cfg.escala_mundo


def altura_visao():
    return cfg.altura_tela / cfg.escala_mundo


def atualizar_adiante(passo):
    # cresce aos poucos na direção da caminhada e some com a íris parada
    sentido = 1 if jogador.vx > 0 else -1 if jogador.vx < 0 else 0
    falta = sentido * cfg.antecipacao - visao["adiante"]
    visao["adiante"] = visao["adiante"] + falta * min(1.0, cfg.suavizacao_antecipacao * passo)


def focar(ponto):
    # a visão passa a seguir o ponto dado; None a devolve à íris
    visao["foco"] = ponto


def alvo():
    # na vertical, segue o chão em que a íris pisa: o pulo não balança a visão
    # na queda, o alvo desce com ela: a visão sai antes e não leva tranco
    if jogador.no_chao:
        visao["chao"] = jogador.y
    if visao["foco"] is not None:
        return visao["foco"]
    return (jogador.x + cfg.largura_jogador / 2 + visao["adiante"],
            max(visao["chao"], jogador.y) + cfg.altura_jogador / 2)


def limitar(x, y):
    # nunca mostra fora do andar
    x = max(0, min(x, visao["largura_mundo"] - largura_visao()))
    y = max(0, min(y, cfg.altura_mundo - altura_visao()))
    return x, y


def saltar(largura_mundo):
    # início e reinício do andar: direto para a íris, sem suavização
    visao["largura_mundo"] = largura_mundo
    visao["adiante"] = 0.0
    visao["vx"] = 0.0
    visao["vy"] = 0.0
    visao["chao"] = jogador.y
    visao["foco"] = None
    cx, cy = alvo()
    visao["x"], visao["y"] = limitar(cx - largura_visao() / 2, cy - altura_visao() / 2)


def amortecer(atual, alvo, velocidade, tempo_suave, passo):
    # mola criticamente amortecida: a visão acelera e freia aos poucos, sem
    # tranco quando o alvo muda de lugar. devolve a posição e a velocidade
    omega = 2.0 / tempo_suave
    x = omega * passo
    queda = 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)
    distancia = atual - alvo
    temporario = (velocidade + omega * distancia) * passo
    return alvo + (distancia + temporario) * queda, (velocidade - omega * temporario) * queda


def desejado(atual, centro, zona, tamanho):
    # dentro da zona morta a visão fica onde está; fora, o alvo é a borda dela
    meio = atual + tamanho / 2
    if abs(centro - meio) <= zona / 2:
        return atual
    borda = zona / 2 if centro > meio else -zona / 2
    return centro - borda - tamanho / 2


def conter(atual, inicio, tamanho_corpo, tamanho_visao):
    # a suavização atrasa; em queda longa isso tiraria a íris da visão
    menor = inicio + tamanho_corpo + cfg.margem_visao - tamanho_visao
    maior = inicio - cfg.margem_visao
    return max(menor, min(atual, maior))


def atualizar(passo):
    atualizar_adiante(passo)
    cx, cy = alvo()
    alvo_x, alvo_y = limitar(desejado(visao["x"], cx, cfg.zona_morta_x, largura_visao()),
                             desejado(visao["y"], cy, cfg.zona_morta_y, altura_visao()))
    x, visao["vx"] = amortecer(visao["x"], alvo_x, visao["vx"], cfg.tempo_visao_x, passo)
    caindo = jogador.y > visao["chao"]
    y, visao["vy"] = amortecer(visao["y"], alvo_y, visao["vy"],
                               cfg.tempo_visao_queda if caindo else cfg.tempo_visao_y, passo)
    if visao["foco"] is None:
        x = conter(x, jogador.x, cfg.largura_jogador, largura_visao())
        y = conter(y, jogador.y, cfg.altura_jogador, altura_visao())
    visao["x"], visao["y"] = limitar(x, y)


def deslocamento():
    # parte inteira: o mundo é desenhado nela, pixel por pixel
    return math.floor(visao["x"]), math.floor(visao["y"])


def fracao():
    # o que sobra vira deslocamento na tela, em pixels de tela: a câmera anda
    # suave, sem saltar de escala_mundo em escala_mundo
    ox, oy = deslocamento()
    return visao["x"] - ox, visao["y"] - oy


def visivel(x, y, largura, altura):
    # um pixel a mais em cada eixo, para a fração da câmera
    ox, oy = deslocamento()
    return (x + largura > ox and x < ox + largura_visao() + 1 and
            y + altura > oy and y < oy + altura_visao() + 1)
