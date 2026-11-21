import configuracoes as cfg

# passagem de um andar a outro: a tela escurece, mostra o andar e clareia.
# enquanto dura, o jogo fica parado. não desenha e não importa pygame
passagem = {"etapa": None, "tempo": 0.0, "destino": None}

duracoes = {"escurecendo": "tempo_escurecer", "cartao": "tempo_cartao", "clareando": "tempo_clarear"}
seguinte = {"escurecendo": "cartao", "cartao": "clareando", "clareando": None}


def iniciar(destino, escurecer=True):
    # destino: índice do andar, ou "fim"; sem escurecer, começa já no cartão
    passagem["etapa"] = "escurecendo" if escurecer else "cartao"
    passagem["tempo"] = 0.0
    passagem["destino"] = destino


def ativa():
    return passagem["etapa"] is not None


def atualizar(passo):
    # devolve o destino no quadro em que a tela fica toda escura
    if not ativa():
        return None
    passagem["tempo"] = passagem["tempo"] + passo
    etapa = passagem["etapa"]
    if passagem["tempo"] < getattr(cfg, duracoes[etapa]):
        return None
    passagem["etapa"] = seguinte[etapa]
    passagem["tempo"] = 0.0
    return passagem["destino"] if etapa == "escurecendo" else None


def escuridao():
    # de 0 (nada) a 1 (tela preta)
    etapa, t = passagem["etapa"], passagem["tempo"]
    if etapa == "escurecendo":
        return t / cfg.tempo_escurecer
    if etapa == "cartao":
        return 1.0
    if etapa == "clareando":
        return 1.0 - t / cfg.tempo_clarear
    return 0.0


def cartao():
    # opacidade do nome do andar: entra e sai em 0,25 s dentro do cartão
    if passagem["etapa"] != "cartao" or passagem["destino"] == "fim":
        return 0.0
    t, total = passagem["tempo"], cfg.tempo_cartao
    return max(0.0, min(1.0, t / 0.25, (total - t) / 0.25))
