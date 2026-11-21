import configuracoes as cfg
import fases
import jogador
import mecanismos
import animacao
import efeitos
import enquadramento
import investigacao

# o andar em curso e um quadro de jogo. não importa pygame: os testes em
# testes/ rodam exatamente este código, sem janela
# abertas: as trancas já vencidas neste andar, que o recomeço não fecha de
# novo; abriu: a tranca que abriu neste quadro, para a história comentar
andar = {"indice": 0, "fase": None, "e_solto": True, "detectada": None, "interrompeu": False,
         "abertas": set(), "abriu": None}

# o tempo é anotado, nunca elimina: total da corrida e de cada andar; onde
# ela começou (só a que parte do andar 1 vale recorde do total), os passos
# que a íris conta, se ela já acionou uma alavanca e os flagrantes da câmera
# em cada andar, que pesam na pontuação, com as placas de autor que ela leu
# (quem anota as placas é o main, pela narrativa)
# usados: os tipos de coisa em que ela já mexeu com E ("alavanca", "gaveta",
# "eco"); enquanto um falta, a tecla aparece sobre ele
# caderno: as pistas lidas na noite, na ordem, como (andar, pista); erros: os
# segredos errados confirmados em cada andar, que também ficam anotados
corrida = {"total": 0.0, "andares": {}, "partida": 0, "passos": 0, "acionou": False, "deteccoes": {},
           "placas": set(), "usados": set(), "caderno": [], "erros": {}}

# o que aconteceu neste quadro fora dos mecanismos: "reinicio" (tecla r),
# "detectada" e "retorno" (o andar recomeça depois da detecção), e o que a
# investigação fez: "pista", "roda", "tranca_abre", "tranca_erro"
sinais = []


def nova_corrida(partida=0):
    corrida["total"] = 0.0
    corrida["andares"] = {}
    corrida["partida"] = partida
    corrida["passos"] = 0
    corrida["acionou"] = False
    corrida["deteccoes"] = {}
    corrida["placas"] = set()
    corrida["usados"] = set()
    corrida["caderno"] = []
    corrida["erros"] = {}


def anotar(tempo):
    # conta só com o jogo correndo; a detecção também conta: a noite fica mais longa
    corrida["total"] = corrida["total"] + tempo
    indice = andar["indice"]
    corrida["andares"][indice] = corrida["andares"].get(indice, 0.0) + tempo


def carregar_andar(indice, abertas=()):
    # abertas: enigmas que já chegam resolvidos (o recomeço do mesmo andar)
    andar["indice"] = indice
    andar["fase"] = fases.carregar(indice)
    andar["detectada"] = None
    andar["abertas"] = set(abertas)
    andar["abriu"] = None
    for tranca in andar["fase"]["trancas"]:
        tranca["ligada"] = tranca["enigma"] in andar["abertas"]
    investigacao.fechar()
    jogador.posicionar(andar["fase"]["inicio"])
    enquadramento.saltar(andar["fase"]["largura"])
    animacao.reiniciar()
    # a cena nova é desenhada neste mesmo quadro, antes de efeitos.atualizar
    efeitos.reiniciar(andar["fase"])


def reiniciar_andar():
    # tecla r e detecção pela câmera. no treino, que é comprido, a íris volta
    # ao começo da sala em que estava, e não ao começo de tudo
    # a tranca que ela já abriu continua aberta: o segredo não se esquece
    licao = fases.licao_em(andar["fase"], jogador.x + cfg.largura_jogador / 2)
    carregar_andar(andar["indice"], andar["abertas"])
    if licao is not None:
        x = licao[0] * cfg.tile + (cfg.tile - cfg.largura_jogador) // 2
        jogador.posicionar([x, andar["fase"]["inicio"][1]])
        enquadramento.saltar(andar["fase"]["largura"])


def mover(fase, tempo, teclado):
    # a caixa desliza antes, e a íris, barrada por ela, anda junto
    no_chao_antes = jogador.no_chao
    # detectada, ou olhando os monitores, a íris não anda
    if andar["detectada"] is None and fase["olhar"] is None:
        jogador.ler_teclado(teclado, tempo)
    else:
        jogador.parar()
    jogador.levar(mecanismos.esteira_sob_os_pes(fase))
    solidos = jogador.bloqueios(fase)
    empurrou = mecanismos.empurrar_caixas(fase, tempo)
    jogador.mover_horizontal(tempo, solidos + mecanismos.solidos_das_caixas(fase))
    jogador.mover_vertical(tempo, solidos)
    mecanismos.cair_caixas(fase, tempo)
    mecanismos.apoiar_no_topo_da_caixa(fase, tempo)
    if no_chao_antes and not jogador.no_chao and jogador.embalo != 0:
        fase["eventos"].append("lancada")
    return empurrou


def acionar(fase, teclado):
    acionou = False
    if andar["detectada"] is None:
        livre = andar["e_solto"]
        # um E só faz uma coisa: o eco primeiro, depois alavanca, gaveta,
        # monitores e, por último, a pista e a tranca
        for tipo, mexer in (("eco", mecanismos.acionar_eco), ("alavanca", mecanismos.acionar_alavancas),
                            ("gaveta", mecanismos.acionar_gavetas), ("monitores", mecanismos.acionar_monitores),
                            ("pista", investigacao.acionar_pistas), ("tranca", investigacao.acionar_trancas)):
            if mexer(fase, teclado, livre):
                acionou = True
                corrida["usados"].add(tipo)
                break
        if investigacao.aberto["tipo"] == "pista":
            anotar_pista(investigacao.aberto["pista"])
    # tecla nova de mexer, de andar ou de pular: o que interrompe o olhar
    andar["interrompeu"] = (andar["e_solto"] and teclado.key_pressed("E")) or \
        any(teclado.key_pressed(tecla) for tecla in ("LEFT", "RIGHT", "A", "D", "SPACE"))
    andar["e_solto"] = not teclado.key_pressed("E")
    return acionou


def anotar_pista(nome):
    # a pista lida entra no caderno da noite, uma vez só
    entrada = (andar["indice"], nome)
    if entrada not in corrida["caderno"]:
        corrida["caderno"].append(entrada)
        sinais.append("pista_nova")


def em_modal():
    # pista, tranca ou caderno aberto: o andar espera e o tempo não corre
    return investigacao.aberto["tipo"] is not None


def recolher():
    # o que a investigação fez neste quadro vira sinal; o erro fica anotado
    for evento in investigacao.eventos:
        sinais.append(evento)
        if evento == "tranca_erro":
            corrida["erros"][andar["indice"]] = corrida["erros"].get(andar["indice"], 0) + 1
        elif evento == "tranca_abre":
            andar["abriu"] = investigacao.aberto["tranca"]["enigma"]
            andar["abertas"].add(andar["abriu"])
    investigacao.eventos[:] = []


def investigar(tempo, teclado):
    # um quadro com algo aberto: só a investigação anda
    efeitos.eventos[:] = []
    investigacao.atualizar(tempo, teclado, corrida["caderno"])
    andar["e_solto"] = not teclado.key_pressed("E")
    recolher()


def desfecho(fase, detectou, tempo):
    # detectada: controles travados, a cena dura e o andar recomeça
    if andar["detectada"] is not None:
        andar["detectada"] = andar["detectada"] + tempo
        if andar["detectada"] >= cfg.duracao_deteccao:
            reiniciar_andar()
            sinais.append("retorno")
        return None
    if detectou:
        andar["detectada"] = 0.0
        corrida["deteccoes"][andar["indice"]] = corrida["deteccoes"].get(andar["indice"], 0) + 1
        animacao.iniciar_deteccao()
        efeitos.tremer()
        sinais.append("detectada")
        return None
    if mecanismos.tocou_diamante(fase):
        return "diamante"
    if mecanismos.chegou_na_saida(fase):
        return "saida"
    return None


def atualizar(tempo, teclado):
    # um quadro de jogo; devolve "saida", "diamante" ou None
    fase = andar["fase"]
    sinais[:] = []
    fase["eventos"][:] = []
    andar["abriu"] = None
    if em_modal():
        investigar(tempo, teclado)
        return None
    if teclado.key_down("C") and andar["detectada"] is None and fase["olhar"] is None:
        investigacao.abrir_caderno(corrida["caderno"])
        recolher()
        return None
    # r recomeça; na cena da detecção, depois de um instante, também: ela
    # não precisa durar os dois segundos para quem já entendeu
    detectada = andar["detectada"]
    if teclado.key_down("R") and (detectada is None or detectada >= cfg.espera_da_deteccao):
        reiniciar_andar()
        sinais.append("reinicio" if detectada is None else "retorno")
        return None
    empurrou = mover(fase, tempo, teclado)
    mecanismos.atualizar_botoes(fase, tempo)
    acionou = acionar(fase, teclado)
    corrida["acionou"] = corrida["acionou"] or acionou
    passos = jogador.contar_passos(tempo)
    corrida["passos"] = corrida["passos"] + passos
    mecanismos.atualizar_gavetas(fase, tempo)
    mecanismos.atualizar_portas(fase, tempo, passos)
    mecanismos.atualizar_vigas(fase, tempo)
    mecanismos.atualizar_esteiras(fase)
    detectou = mecanismos.atualizar_cameras(fase, tempo)
    animacao.atualizar(tempo, jogador.no_chao, jogador.vx, jogador.vy, empurrou, acionou)
    mecanismos.atualizar_eco(fase, tempo, (animacao.estado, animacao.quadro_atual()))
    efeitos.atualizar(tempo, fase)
    mecanismos.atualizar_olhar(fase, tempo, andar["interrompeu"] or andar["detectada"] is not None)
    enquadramento.focar(mecanismos.ponto_do_olhar(fase))
    enquadramento.atualizar(tempo)
    # o que está pintado na parede se anota de passagem
    for nome in investigacao.notar_de_passagem(fase):
        anotar_pista(nome)
        sinais.append("pista")
    recolher()
    return desfecho(fase, detectou, tempo)
