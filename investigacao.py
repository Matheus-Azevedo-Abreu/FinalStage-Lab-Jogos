import configuracoes as cfg
import jogador
import documentos

# a investigação (docs/andares.md, versão 7): pistas que a íris examina,
# trancas de segredo e o caderno do que ela já leu. com uma dessas coisas
# aberta o andar espera: nada se move e o tempo não é anotado.
# não desenha e não importa pygame

# o que está aberto por cima do andar: "pista", "tranca", "caderno" ou None.
# tempo: há quanto está aberto; erro e acerto: quanto resta do tranco da
# tranca errada e do instante da certa; linha: a escolhida no caderno;
# do_caderno: a pista foi aberta por ele, e fechar volta a ele
aberto = {"tipo": None, "pista": None, "tranca": None, "roda": 0, "tempo": 0.0,
          "erro": 0.0, "acerto": 0.0, "linha": 0, "do_caderno": False}

# o que aconteceu neste quadro, para o som e para a corrida: "pista",
# "roda", "tranca_abre", "tranca_erro"
eventos = []


def fechar():
    aberto.update({"tipo": None, "pista": None, "tranca": None, "do_caderno": False, "erro": 0.0, "acerto": 0.0})


def meio_da_iris():
    return jogador.x + cfg.largura_jogador / 2


def ao_alcance(coisa):
    # no chão, com o meio do corpo diante da célula dela ou da de baixo
    folga = cfg.folga_da_pista
    if not jogador.no_chao or not (coisa["x"] - folga <= meio_da_iris() <= coisa["x"] + cfg.tile + folga):
        return False
    return jogador.encostou(coisa["x"] - folga, coisa["y"], cfg.tile + 2 * folga, 2 * cfg.tile)


def mais_perto(coisas):
    # entre as que estão ao alcance, a de meio mais próximo do meio da íris
    perto = [coisa for coisa in coisas if ao_alcance(coisa)]
    if not perto:
        return None
    return min(perto, key=lambda coisa: abs(coisa["x"] + cfg.tile / 2 - meio_da_iris()))


def pista_ao_alcance(fase):
    return mais_perto(fase["pistas"])


def tranca_ao_alcance(fase):
    return mais_perto([tranca for tranca in fase["trancas"] if not tranca["ligada"]])


def abrir_pista(nome, do_caderno=False):
    aberto.update({"tipo": "pista", "pista": nome, "do_caderno": do_caderno, "tempo": 0.0})
    eventos.append("pista")


def acionar_pistas(fase, teclado, tecla_livre):
    pista = pista_ao_alcance(fase)
    if pista is None or not (tecla_livre and teclado.key_pressed("E")):
        return False
    pista["lida"] = True
    abrir_pista(pista["nome"])
    return True


def notar_de_passagem(fase):
    # a pista "auto" (pintada na parede, grande) se anota sozinha quando a
    # íris passa pela coluna dela, em qualquer altura: devolve as recém-notadas
    notadas = []
    for pista in fase["pistas"]:
        if pista["auto"] and not pista["lida"] and pista["x"] - cfg.tile // 2 <= meio_da_iris() <= pista["x"] + cfg.tile * 3 // 2:
            pista["lida"] = True
            notadas.append(pista["nome"])
    return notadas


def acionar_trancas(fase, teclado, tecla_livre):
    tranca = tranca_ao_alcance(fase)
    if tranca is None or not (tecla_livre and teclado.key_pressed("E")):
        return False
    aberto.update({"tipo": "tranca", "tranca": tranca, "roda": 0, "tempo": 0.0, "erro": 0.0, "acerto": 0.0})
    eventos.append("roda")
    return True


def abrir_caderno(entradas):
    aberto.update({"tipo": "caderno", "tempo": 0.0, "linha": max(0, min(aberto["linha"], len(entradas) - 1))})
    eventos.append("pista")


def apertou(teclado, *teclas):
    return any(teclado.key_down(tecla) for tecla in teclas)


def simbolos_da_tranca(tranca):
    return documentos.rodas[documentos.enigmas[tranca["enigma"]]["rodas"]]


def mostrado(tranca):
    # o que as rodas mostram agora, uma posição por roda
    simbolos = simbolos_da_tranca(tranca)
    return [simbolos[posicao] for posicao in tranca["posicoes"]]


def conferir(tranca):
    # segredo certo: a tranca fica aberta para sempre; errado, fica anotado
    if mostrado(tranca) == documentos.enigmas[tranca["enigma"]]["segredo"]:
        tranca["ligada"] = True
        aberto["acerto"] = cfg.tempo_do_acerto
        eventos.append("tranca_abre")
    else:
        tranca["erros"] = tranca["erros"] + 1
        aberto["erro"] = cfg.tempo_do_erro
        eventos.append("tranca_erro")


def girar(tranca, teclado):
    # esquerda e direita escolhem a roda; cima e baixo giram; um algarismo
    # digitado entra na roda da vez e passa à seguinte
    posicoes = tranca["posicoes"]
    simbolos = simbolos_da_tranca(tranca)
    antes = (aberto["roda"], list(posicoes))
    if apertou(teclado, "LEFT", "A"):
        aberto["roda"] = (aberto["roda"] - 1) % len(posicoes)
    if apertou(teclado, "RIGHT", "D"):
        aberto["roda"] = (aberto["roda"] + 1) % len(posicoes)
    for tecla, passo in (("UP", 1), ("W", 1), ("DOWN", -1), ("S", -1)):
        if teclado.key_down(tecla):
            posicoes[aberto["roda"]] = (posicoes[aberto["roda"]] + passo) % len(simbolos)
    for simbolo in simbolos:
        if len(simbolo) == 1 and teclado.key_down(simbolo):
            posicoes[aberto["roda"]] = simbolos.index(simbolo)
            aberto["roda"] = min(aberto["roda"] + 1, len(posicoes) - 1)
    if antes != (aberto["roda"], posicoes):
        eventos.append("roda")


def atualizar_tranca(tempo, teclado):
    tranca = aberto["tranca"]
    if aberto["acerto"] > 0:
        # as rodas ficam um instante na tela, certas, e a tranca se fecha sozinha
        aberto["acerto"] = aberto["acerto"] - tempo
        if aberto["acerto"] <= 0:
            fechar()
        return
    aberto["erro"] = max(0.0, aberto["erro"] - tempo)
    if apertou(teclado, "ESC", "C"):
        fechar()
        return
    girar(tranca, teclado)
    if aberto["tempo"] > cfg.espera_do_modal and apertou(teclado, "ENTER", "E"):
        conferir(tranca)


def atualizar_pista(teclado, entradas):
    # a tecla que abriu não fecha: só vale depois de um instante
    fecha = apertou(teclado, "ESC", "C") or (aberto["tempo"] > cfg.espera_do_modal and apertou(teclado, "E", "ENTER"))
    if fecha:
        if aberto["do_caderno"]:
            abrir_caderno(entradas)
        else:
            fechar()


def atualizar_caderno(teclado, entradas):
    if apertou(teclado, "ESC", "C"):
        fechar()
        return
    antes = aberto["linha"]
    if apertou(teclado, "UP", "W"):
        aberto["linha"] = max(0, aberto["linha"] - 1)
    if apertou(teclado, "DOWN", "S"):
        aberto["linha"] = min(max(0, len(entradas) - 1), aberto["linha"] + 1)
    if antes != aberto["linha"]:
        eventos.append("roda")
    if entradas and aberto["tempo"] > cfg.espera_do_modal and apertou(teclado, "E", "ENTER"):
        abrir_pista(entradas[aberto["linha"]][1], True)


def atualizar(tempo, teclado, entradas):
    # um quadro com algo aberto; entradas: o caderno, [(andar, pista)]
    aberto["tempo"] = aberto["tempo"] + tempo
    if aberto["tipo"] == "pista":
        atualizar_pista(teclado, entradas)
    elif aberto["tipo"] == "tranca":
        atualizar_tranca(tempo, teclado)
    elif aberto["tipo"] == "caderno":
        atualizar_caderno(teclado, entradas)
