import configuracoes as cfg

x = 0.0
y = 0.0
vy = 0.0
vx = 0.0
no_chao = False
direcao = "leste"   # para qual lado ela olha, só muda o desenho
# o que a leva além das próprias pernas: a esteira sob os pés e, no ar, o
# embalo com que saiu dela
arrasto = 0.0
embalo = 0.0
# chão andado desde o último passo, os passos dados no andar e se ela está
# no ar por ter pulado (cair de uma borda não é pulo)
andado = 0.0
passos = 0
pulando = False
# se a tecla de pulo estava apertada no quadro anterior, por quanto tempo o
# pedido de pulo ainda vale e se ela saiu do lugar no último quadro
tecla_de_pulo = False
pedido_de_pulo = 0.0
andou = False


def posicionar(inicio):
    global x, y, vy, vx, no_chao, direcao, arrasto, embalo, andado, passos, pulando
    global tecla_de_pulo, pedido_de_pulo, andou
    tecla_de_pulo = False
    pedido_de_pulo = 0.0
    andou = False
    x = float(inicio[0])
    y = float(inicio[1])
    vy = 0.0
    vx = 0.0
    no_chao = False
    direcao = "leste"
    arrasto = 0.0
    embalo = 0.0
    andado = 0.0
    passos = 0
    pulando = False


def levar(esteira):
    # no chão, vale a esteira em que pisa, e é esse o embalo que ela leva se
    # pular; no ar, o embalo continua até tocar o chão
    global arrasto, embalo
    if no_chao:
        arrasto = esteira
        embalo = esteira
    else:
        arrasto = embalo


def contar_passos(tempo):
    # só o que ela faz com as próprias pernas: 54 px andados no chão são um
    # passo, e um pulo, ao pousar, vale três (é o chão que ele cobre). ser
    # levada, cair e ficar parada não contam, nem andar contra uma parede
    # sem sair do lugar. devolve os passos deste quadro
    global andado, passos, pulando
    novos = 0
    if no_chao and pulando:
        pulando = False
        novos = cfg.passos_do_pulo
    if no_chao and vx != 0 and andou:
        andado = andado + abs(vx) * tempo
        inteiros = int(andado // cfg.passo_px)
        andado = andado - inteiros * cfg.passo_px
        novos = novos + inteiros
    passos = passos + novos
    return novos


def ler_teclado(teclado, tempo=0.0):
    global vx, direcao, tecla_de_pulo, pedido_de_pulo
    vx = 0
    if teclado.key_pressed("LEFT") or teclado.key_pressed("A"):
        vx = -cfg.vel_jogador
        direcao = "oeste"
    if teclado.key_pressed("RIGHT") or teclado.key_pressed("D"):
        vx = cfg.vel_jogador
        direcao = "leste"
    # o pulo sai quando a tecla desce, não enquanto ela fica apertada: segurar
    # não repete. o pedido vale um instante, para quem aperta antes de pousar
    apertada = teclado.key_pressed("SPACE") or teclado.key_pressed("W") or teclado.key_pressed("UP")
    pedido_de_pulo = cfg.memoria_do_pulo if apertada and not tecla_de_pulo else max(0.0, pedido_de_pulo - tempo)
    tecla_de_pulo = apertada
    if pedido_de_pulo > 0 and no_chao:
        pedido_de_pulo = 0.0
        pular()


def parar():
    # controles travados: a detecção pela câmera
    global vx
    vx = 0


def pular():
    global vy, no_chao, pulando
    vy = -cfg.vel_pulo
    no_chao = False
    pulando = True


def bloqueios(fase):
    # paredes mais portas fechadas: tudo que barra passagem
    lista = []
    for p in fase["paredes"]:
        lista.append([p[0], p[1], cfg.tile, cfg.tile])
    for porta in fase["portas"]:
        if not porta["aberta"]:
            lista.append([porta["x"], porta["y"], cfg.tile, cfg.altura_porta])
    # gaveta aberta é tábua; viga de ferro é chão onde estiver
    for gaveta in fase["gavetas"]:
        if gaveta["aberta"]:
            lista.append([gaveta["x"], gaveta["y"], cfg.tile, cfg.altura_gaveta])
    for viga in fase["vigas"]:
        lista.append([viga["x"], viga["y"], viga["largura"], cfg.altura_viga])
    return lista


def mover_horizontal(tempo, solidos):
    global x, andou
    # as pernas mais o que a leva: é a soma que decide de que lado ela bate
    v = vx + arrasto
    antes = x
    x = x + v * tempo
    for s in solidos:
        if cfg.colidiu(x, y, cfg.largura_jogador, cfg.altura_jogador,
                       s[0], s[1], s[2], s[3]):
            if v > 0:
                x = s[0] - cfg.largura_jogador
            elif v < 0:
                x = s[0] + s[2]
    andou = abs(x - antes) > 0.01


def mover_vertical(tempo, solidos):
    global y, vy, no_chao
    vy = vy + cfg.gravidade * tempo
    y = y + vy * tempo
    no_chao = False
    for s in solidos:
        if cfg.colidiu(x, y, cfg.largura_jogador, cfg.altura_jogador,
                       s[0], s[1], s[2], s[3]):
            if vy > 0:
                y = s[1] - cfg.altura_jogador
                vy = 0
                no_chao = True
            elif vy < 0:
                y = s[1] + s[3]
                vy = 0


def encostou(bx, by, bl, ba):
    return cfg.colidiu(x, y, cfg.largura_jogador, cfg.altura_jogador, bx, by, bl, ba)
