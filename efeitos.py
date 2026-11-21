import math
import configuracoes as cfg
import jogador
import animacao
import mecanismos

# efeitos derivados do estado de jogo: transições dos mecanismos, poeira e
# a lista de eventos do quadro. só lê o jogo, nunca o altera; não importa pygame

# fase em curso; ao trocar, tudo recomeça parado
fase_atual = {"fase": None}

# por mecanismo, na ordem da fase: [último estado visto, tempo desde a troca]
transicoes = {"portas": [], "alavancas": [], "botoes": []}
campo_do_estado = {"portas": "aberta", "alavancas": "ligada", "botoes": "pressionado"}

# nome do evento quando o mecanismo troca de estado: [False, True]
nomes_de_troca = {
    "portas": ["porta_fechando", "porta_abrindo"],
    "alavancas": ["alavanca", "alavanca"],
    "botoes": ["botao_solto", "botao_pressionado"],
}

# tempo corrido no andar: brilho do diamante em laço
relogio = {"tempo": 0.0}

# último alvo de cada caixa: alvo novo é um empurrão que começa
alvos_caixas = []

# poeiras no ar: [chave em cfg.efeitos, x, y, tempo, direção]
poeiras = []

# o que a íris fazia no quadro anterior
anterior = {"estado": animacao.estado, "quadro": 0}

# o que aconteceu neste quadro, em nomes: quem toca som lê daqui (som.py).
# a lista é refeita a cada atualizar
eventos = []

# por caixa, se caía no quadro anterior; por porta, as marcas de tempo; por
# câmera, o estado: a mudança vira evento
memoria = {"caindo": [], "marcas": [], "cameras": []}

# tremor da visão no flagrante: tempo que resta
tremor = {"resta": 0.0}

# queda mais lenta que isto não faz barulho: é a caixa assentando
queda_audivel = 150


def reiniciar(fase):
    fase_atual["fase"] = fase
    # tempo alto: nada começa no meio de uma transição
    for nome in transicoes:
        transicoes[nome] = [[m[campo_do_estado[nome]], 99.0] for m in fase[nome]]
    alvos_caixas[:] = [c["alvo"] for c in fase["caixas"]]
    poeiras[:] = []
    eventos[:] = []
    tremor["resta"] = 0.0
    memoria["caindo"] = [False for _ in fase["caixas"]]
    memoria["marcas"] = [mecanismos.marcas_de_tempo(p) for p in fase["portas"]]
    memoria["cameras"] = [c["estado"] for c in fase["cameras"]]
    relogio["tempo"] = 0.0
    anterior["estado"] = animacao.estado
    anterior["quadro"] = 0


def atualizar_transicoes(fase, passo):
    for nome, lista in transicoes.items():
        campo = campo_do_estado[nome]
        for mecanismo, registro in zip(fase[nome], lista):
            if mecanismo[campo] != registro[0]:
                registro[0] = mecanismo[campo]
                registro[1] = 0.0
                eventos.append(nomes_de_troca[nome][registro[0]])
            else:
                registro[1] = registro[1] + passo


def levantar_poeira(chave, x, y, direcao):
    poeiras.append([chave, x, y, 0.0, direcao])


def poeira_dos_pes():
    # centrada nos pés, com a base no chão
    x = jogador.x + cfg.largura_jogador // 2 - 8
    y = jogador.y + cfg.altura_jogador - 16
    levantar_poeira("poeira_passo", x, y, jogador.direcao)


def poeira_da_iris():
    # passo nos quadros de apoio da caminhada; aterrissagem ao tocar o chão
    estado = animacao.estado
    quadro = animacao.quadro_atual()
    if estado == "andando" and quadro in cfg.passos_andando:
        if anterior["estado"] != "andando" or anterior["quadro"] != quadro:
            poeira_dos_pes()
            eventos.append("passo")
    if anterior["estado"] in animacao.no_ar and estado not in animacao.no_ar:
        poeira_dos_pes()
        eventos.append("pouso")
    if estado == "preparando" and anterior["estado"] not in animacao.no_ar:
        eventos.append("pulo")
    anterior["estado"] = estado
    anterior["quadro"] = quadro


def rastro_da_caixa(fase, caixa):
    # o que a caixa levanta ao ser empurrada: poeira, se arrasta no chão;
    # atrito na junta, se arrasta por cima de outra caixa parada; nada, se
    # a de baixo vai junto (a pilha anda inteira e só a de baixo toca o chão)
    embaixo = mecanismos.caixa_embaixo(fase, caixa)
    if embaixo is None:
        return "poeira_caixa"
    return None if embaixo["alvo"] is not None else "raspao_caixa"


def poeira_das_caixas(fase):
    for i, caixa in enumerate(fase["caixas"]):
        if caixa["alvo"] is not None and caixa["alvo"] != alvos_caixas[i]:
            direcao = "leste" if caixa["alvo"] > caixa["x"] else "oeste"
            rastro = rastro_da_caixa(fase, caixa)
            if rastro is not None:
                levantar_poeira(rastro, caixa["x"], caixa["y"] + cfg.tile - 16, direcao)
            eventos.append("caixa")
        alvos_caixas[i] = caixa["alvo"]
        # caía de verdade e parou: o baque, com poeira só se foi no chão
        if memoria["caindo"][i] and caixa["vy"] == 0:
            eventos.append("caixa_caiu")
            if mecanismos.caixa_embaixo(fase, caixa) is None:
                levantar_poeira("poeira_caixa", caixa["x"], caixa["y"] + cfg.tile - 16, "leste")
        memoria["caindo"][i] = caixa["vy"] > queda_audivel


def eventos_das_portas(fase):
    # uma marca de tempo a menos é um segundo que passou: o tique
    for i, porta in enumerate(fase["portas"]):
        marcas = mecanismos.marcas_de_tempo(porta)
        if 0 < marcas < memoria["marcas"][i]:
            eventos.append("tique")
        memoria["marcas"][i] = marcas


def eventos_das_cameras(fase):
    for i, camera in enumerate(fase["cameras"]):
        if camera["estado"] != memoria["cameras"][i]:
            if camera["estado"] == "alerta":
                eventos.append("alerta")
            elif memoria["cameras"][i] == "alerta":
                eventos.append("alerta_fim")
        memoria["cameras"][i] = camera["estado"]


def atualizar(passo, fase):
    if fase is not fase_atual["fase"]:
        reiniciar(fase)
    eventos[:] = []
    relogio["tempo"] = relogio["tempo"] + passo
    tremor["resta"] = max(0.0, tremor["resta"] - passo)
    atualizar_transicoes(fase, passo)
    poeira_da_iris()
    poeira_das_caixas(fase)
    eventos_das_portas(fase)
    eventos_das_cameras(fase)
    for poeira in poeiras:
        poeira[3] = poeira[3] + passo
    poeiras[:] = [p for p in poeiras if p[3] < cfg.efeitos[p[0]][2]]


def tremer():
    tremor["resta"] = cfg.tempo_tremor


def deslocamento_do_tremor():
    # vaivém que morre junto com o tempo, em px de mundo; (0, 0) parado
    if tremor["resta"] <= 0:
        return 0.0, 0.0
    forca = cfg.forca_tremor * tremor["resta"] / cfg.tempo_tremor
    fase_do_vaivem = relogio["tempo"] * 70
    return forca * math.sin(fase_do_vaivem), forca * 0.5 * math.cos(fase_do_vaivem * 1.3)


def quadro_do_efeito(chave, tempo):
    _, quadros, duracao = cfg.efeitos[chave]
    return min(int(tempo / (duracao / quadros)), quadros - 1)


def quadro_da_porta(i, aberta):
    # quadro da tira porta-abrindo, ou None fora da transição; fechar é o inverso
    tempo = transicoes["portas"][i][1]
    if tempo >= cfg.efeitos["porta_abrindo"][2]:
        return None
    quadro = quadro_do_efeito("porta_abrindo", tempo)
    return quadro if aberta else cfg.efeitos["porta_abrindo"][1] - 1 - quadro


def quadro_do_brilho():
    _, quadros, duracao = cfg.efeitos["brilho"]
    return int(relogio["tempo"] / (duracao / quadros)) % quadros


def no_meio(nome, i):
    # alavanca ou botão acabou de trocar: mostra o quadro do meio
    return transicoes[nome][i][1] < cfg.tempo_meio
