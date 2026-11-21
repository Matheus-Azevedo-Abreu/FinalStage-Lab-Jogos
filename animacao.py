import configuracoes as cfg

# estado da animação da íris; só lê o estado de jogo, nunca o altera
estado = "parada"
tempo = 0.0
desde_empurrao = cfg.folga_empurrao


def reiniciar():
    global estado, tempo, desde_empurrao
    estado = "parada"
    tempo = 0.0
    desde_empurrao = cfg.folga_empurrao


# estados em que a íris está no ar
no_ar = ("preparando", "pulando", "caindo")


def em_curso(nome):
    # pose curta que toca uma vez e ainda não terminou
    return estado == nome and tempo < cfg.animacoes[nome][2]


def escolher_estado(no_chao, vx, vy, empurrando, acionou):
    # poses curtas: andar ou sair do chão interrompe
    if not no_chao:
        if vy < 0 and (estado not in no_ar or em_curso("preparando")):
            return "preparando"
        return "pulando" if vy < 0 else "caindo"
    if vx == 0 and (acionou or em_curso("acionando")):
        return "acionando"
    if vx == 0 and (estado in no_ar or em_curso("aterrissando")):
        return "aterrissando"
    if vx == 0:
        return "parada"
    if empurrando:
        return "empurrando"
    return "andando"


def iniciar_deteccao():
    # a íris vista pela câmera: toca uma vez e fica nela até o andar recomeçar
    global estado, tempo
    estado = "detectada"
    tempo = 0.0


def atualizar(passo, no_chao, vx, vy, empurrou, acionou):
    global estado, tempo, desde_empurrao
    if estado == "detectada":
        tempo = tempo + passo
        return
    desde_empurrao = 0.0 if empurrou else desde_empurrao + passo
    empurrando = desde_empurrao < cfg.folga_empurrao
    novo = escolher_estado(no_chao, vx, vy, empurrando, acionou)
    # troca de estado recomeça do primeiro quadro
    if novo != estado or (acionou and novo == "acionando"):
        estado = novo
        tempo = 0.0
    else:
        tempo = tempo + passo


def quadro_atual():
    _, quadros, duracao, repete = cfg.animacoes[estado]
    indice = int(tempo / (duracao / quadros))
    if repete:
        return indice % quadros
    return min(indice, quadros - 1)
