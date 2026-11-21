import configuracoes as cfg

# o estado das falas: a conversa, que para o jogo (abertura e final), e o
# aviso, a linha do rádio que passa por cima do jogo sem travar nada.
# uma fala é (quem, retrato, texto). não desenha e não importa pygame

conversa = {"falas": [], "indice": 0, "tempo": 0.0}

# a linha em curso, o tempo dela e as que esperam a vez
aviso = {"fala": None, "tempo": 0.0, "fila": []}

# o que aconteceu neste quadro, para o som: "abre", "fecha" e "voz:quem"
eventos = []


def letras_ate(tempo, texto):
    return min(len(texto), int(tempo * cfg.letras_por_segundo))


def vozes(antes, agora, fala):
    # uma sílaba a cada tantas letras novas; espaço não fala
    quem, _, texto = fala
    for i in range(antes, agora):
        if i % cfg.letras_por_voz == 0 and texto[i] != " " and quem is not None:
            eventos.append("voz:" + quem)
            return


def iniciar(falas):
    conversa["falas"] = list(falas)
    conversa["indice"] = 0
    conversa["tempo"] = 0.0


def ativa():
    return conversa["indice"] < len(conversa["falas"])


def fala_atual():
    return conversa["falas"][conversa["indice"]]


def letras():
    return letras_ate(conversa["tempo"], fala_atual()[2])


def escrita():
    return letras() >= len(fala_atual()[2])


def avancar():
    # primeiro termina de escrever a linha; só depois passa à seguinte
    if not ativa():
        return
    if not escrita():
        conversa["tempo"] = 9999.0
        return
    conversa["indice"] = conversa["indice"] + 1
    conversa["tempo"] = 0.0


def encerrar():
    conversa["indice"] = len(conversa["falas"])


def atualizar(passo):
    eventos[:] = []
    if not ativa():
        return
    antes = letras()
    conversa["tempo"] = conversa["tempo"] + passo
    vozes(antes, letras(), fala_atual())


def avisar(fala):
    aviso["fila"].append(fala)


def calar():
    # andar novo ou volta ao menu: nada fica falando sozinho
    aviso["fala"] = None
    aviso["fila"] = []


def duracao_do_aviso(texto):
    escrever = len(texto) / cfg.letras_por_segundo
    return escrever + cfg.tempo_aviso + cfg.tempo_aviso_por_letra * len(texto)


def letras_do_aviso():
    return letras_ate(aviso["tempo"], aviso["fala"][2])


def opacidade_do_aviso():
    # entra e sai em 0,2 s
    if aviso["fala"] is None:
        return 0.0
    resta = duracao_do_aviso(aviso["fala"][2]) - aviso["tempo"]
    return max(0.0, min(1.0, aviso["tempo"] / 0.2, resta / 0.2))


def atualizar_aviso(passo):
    # roda só com o jogo correndo
    eventos[:] = []
    if aviso["fala"] is None:
        if not aviso["fila"]:
            return
        aviso["fala"] = aviso["fila"].pop(0)
        aviso["tempo"] = 0.0
        if aviso["fala"][0] == "selene":
            eventos.append("abre")
    antes = letras_do_aviso()
    aviso["tempo"] = aviso["tempo"] + passo
    vozes(antes, letras_do_aviso(), aviso["fala"])
    if aviso["tempo"] >= duracao_do_aviso(aviso["fala"][2]):
        if aviso["fala"][0] == "selene":
            eventos.append("fecha")
        aviso["fala"] = None
