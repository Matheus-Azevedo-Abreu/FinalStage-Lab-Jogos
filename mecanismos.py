import math
import configuracoes as cfg
import jogador

# regras dos objetos do andar: caixas, botões, alavancas, canais, portas,
# câmeras, saída e diamante. não desenha e não importa pygame

# somar 1/60 muitas vezes deixa resíduo: abaixo disto, o tempo acabou
quase_zero = 1e-9


def solidos_das_caixas(fase, ignorar=None):
    return [[c["x"], c["y"], cfg.tile, cfg.tile] for c in fase["caixas"] if c is not ignorar]


def solidos_para_caixa(fase, ignorar):
    return jogador.bloqueios(fase) + solidos_das_caixas(fase, ignorar)


def encostada(caixa):
    # borda com borda no sentido do movimento; no ar a caixa é só parede
    if not jogador.no_chao:
        return False
    if jogador.y >= caixa["y"] + cfg.tile or jogador.y + cfg.altura_jogador <= caixa["y"]:
        return False
    if jogador.vx > 0:
        return abs(jogador.x + cfg.largura_jogador - caixa["x"]) < 0.01
    if jogador.vx < 0:
        return abs(jogador.x - (caixa["x"] + cfg.tile)) < 0.01
    return False


def celula_livre(fase, caixa, destino):
    for s in solidos_para_caixa(fase, caixa):
        if cfg.colidiu(destino, caixa["y"], cfg.tile, cfg.tile, s[0], s[1], s[2], s[3]):
            return False
    return True


def escolher_alvo(fase, caixa):
    # a célula seguinte no sentido do empurrão, se estiver livre
    destino = caixa["x"] + (cfg.tile if jogador.vx > 0 else -cfg.tile)
    if celula_livre(fase, caixa, destino):
        caixa["alvo"] = destino


def deslizar(caixa, tempo):
    # anda até o alvo e para exatamente nele, alinhada à grade
    passo = cfg.vel_empurrao * tempo
    distancia = caixa["alvo"] - caixa["x"]
    if abs(distancia) <= passo:
        caixa["x"] = caixa["alvo"]
        caixa["alvo"] = None
    else:
        caixa["x"] = caixa["x"] + (passo if distancia > 0 else -passo)


def empurrar_caixas(fase, tempo):
    # roda antes de a íris andar: a caixa desliza um tile por empurrão e a
    # íris, barrada por ela, avança junto. devolve True se está empurrando
    empurrando = False
    for caixa in fase["caixas"]:
        # caixa caindo não é empurrada: só a apoiada tem vy zerado
        if encostada(caixa) and caixa["vy"] == 0:
            empurrando = True
            if caixa["alvo"] is None:
                escolher_alvo(fase, caixa)
        if caixa["alvo"] is not None:
            deslizar(caixa, tempo)
    return empurrando


def cair_caixas(fase, tempo):
    for caixa in fase["caixas"]:
        caixa["vy"] = caixa["vy"] + cfg.gravidade * tempo
        caixa["y"] = caixa["y"] + caixa["vy"] * tempo
        for s in solidos_para_caixa(fase, caixa):
            if cfg.colidiu(caixa["x"], caixa["y"], cfg.tile, cfg.tile,
                           s[0], s[1], s[2], s[3]):
                if caixa["vy"] > 0:
                    caixa["y"] = s[1] - cfg.tile
                    caixa["vy"] = 0


def caixa_embaixo(fase, caixa):
    # a caixa em que esta se apoia, ou None se o apoio é o chão (ou o ar)
    for outra in fase["caixas"]:
        if outra is not caixa and outra["y"] == caixa["y"] + cfg.tile and abs(outra["x"] - caixa["x"]) < cfg.tile:
            return outra
    return None


def apoiar_no_topo_da_caixa(fase, tempo):
    for caixa in fase["caixas"]:
        if jogador.encostou(caixa["x"], caixa["y"], cfg.tile, cfg.tile):
            pes_antes = jogador.y + cfg.altura_jogador - jogador.vy * tempo
            if jogador.vy > 0 and pes_antes <= caixa["y"]:
                jogador.y = caixa["y"] - cfg.altura_jogador
                jogador.vy = 0
                jogador.no_chao = True


def eco_encosta(fase, x, y, largura, altura):
    # o eco tem o corpo da íris, no lugar em que ela esteve
    atual = fase["eco"]["atual"]
    return atual is not None and cfg.colidiu(atual[0], atual[1], cfg.largura_jogador, cfg.altura_jogador,
                                             x, y, largura, altura)


def com_peso(fase, botao):
    # a íris, o eco dela ou uma caixa em cima
    if jogador.encostou(botao["x"], botao["y"], cfg.tile, cfg.altura_botao):
        return True
    if eco_encosta(fase, botao["x"], botao["y"], cfg.tile, cfg.altura_botao):
        return True
    for caixa in fase["caixas"]:
        if cfg.colidiu(caixa["x"], caixa["y"], cfg.tile, cfg.tile,
                       botao["x"], botao["y"], cfg.tile, cfg.altura_botao):
            return True
    return False


def atualizar_botoes(fase, tempo):
    # a memória só conta nos canais "todos": botão solto ainda vale pelos
    # segundos que o andar declara em "memorias" para o canal (0 por padrão)
    for botao in fase["botoes"]:
        botao["pressionado"] = com_peso(fase, botao)
        if botao["pressionado"]:
            botao["memoria"] = fase["memorias"].get(botao["canal"], 0.0)
        else:
            botao["memoria"] = max(0.0, botao["memoria"] - tempo)


def acionar_alavancas(fase, teclado, tecla_livre):
    acionou = False
    for alavanca in fase["alavancas"]:
        perto = jogador.encostou(alavanca["x"], alavanca["y"],
                                 cfg.largura_alavanca, cfg.altura_alavanca)
        if perto and teclado.key_pressed("E") and tecla_livre:
            alavanca["ligada"] = not alavanca["ligada"]
            acionou = True
    return acionou


def tabua(gaveta):
    return [gaveta["x"], gaveta["y"], cfg.tile, cfg.altura_gaveta]


def ao_alcance(gaveta):
    # ao lado ou logo abaixo dela, à distância de um braço; nunca no lugar
    # em que a tábua vai aparecer
    if jogador.encostou(*tabua(gaveta)):
        return False
    return cfg.colidiu(jogador.x - 14, jogador.y - 20, cfg.largura_jogador + 28, cfg.altura_jogador + 28,
                       gaveta["x"], gaveta["y"], cfg.tile, cfg.tile)


def acionar_gavetas(fase, teclado, tecla_livre):
    # puxar uma gaveta já aberta dá corda de novo no tempo dela
    acionou = False
    for gaveta in fase["gavetas"]:
        if tecla_livre and teclado.key_pressed("E") and ao_alcance(gaveta):
            if not gaveta["aberta"]:
                fase["eventos"].append("gaveta_abrindo")
            gaveta["aberta"] = True
            gaveta["resta"] = cfg.tempo_gaveta
            acionou = True
    return acionou


def atualizar_gavetas(fase, tempo):
    # fecha sozinha, com quem estiver em cima: a mola não espera ninguém
    for gaveta in fase["gavetas"]:
        if gaveta["aberta"]:
            gaveta["resta"] = gaveta["resta"] - tempo
            if gaveta["resta"] <= quase_zero:
                gaveta["aberta"] = False
                fase["eventos"].append("gaveta_fechando")


def marcas_da_gaveta(gaveta):
    return math.ceil(gaveta["resta"] - quase_zero) if gaveta["aberta"] else 0


def sobre_a_viga(viga):
    # a íris de pé nela: os pés na face de cima
    return (jogador.no_chao and abs(jogador.y + cfg.altura_jogador - viga["y"]) < 0.5 and
            jogador.x + cfg.largura_jogador > viga["x"] and jogador.x < viga["x"] + viga["largura"])


def viga_livre(fase, viga, x, y):
    # o lugar seguinte não pode ter a íris nem caixa: o ferro espera
    if cfg.colidiu(jogador.x, jogador.y, cfg.largura_jogador, cfg.altura_jogador,
                   x, y, viga["largura"], cfg.altura_viga):
        return False
    for caixa in fase["caixas"]:
        if cfg.colidiu(caixa["x"], caixa["y"], cfg.tile, cfg.tile, x, y, viga["largura"], cfg.altura_viga):
            return False
    return True


def atualizar_vigas(fase, tempo):
    # cada viga corre para o lugar que as alavancas dela mandam (número ímpar
    # ligado: o outro lugar). não anda com a íris em cima nem por cima dela
    for viga in fase["vigas"]:
        alvo = viga["outro"] if porta_acionada(fase, viga) != viga["invertida"] else viga["repouso"]
        dx, dy = alvo[0] - viga["x"], alvo[1] - viga["y"]
        distancia = math.hypot(dx, dy)
        andando = False
        if distancia > 0 and not sobre_a_viga(viga):
            passo = min(distancia, cfg.vel_viga * tempo)
            x, y = viga["x"] + dx / distancia * passo, viga["y"] + dy / distancia * passo
            if viga_livre(fase, viga, x, y):
                viga["x"], viga["y"] = x, y
                andando = True
        if andando and not viga["andando"]:
            fase["eventos"].append("viga")
        viga["andando"] = andando


def perto_da_marca(fase):
    for marca in fase["eco"]["marcas"]:
        if jogador.encostou(marca[0], marca[1], cfg.tile, cfg.tile):
            return marca
    return None


def soltar_eco(fase):
    # a gravação acaba: a íris volta ao ponto em que começou e o eco repete,
    # uma vez, tudo o que ela fez
    eco = fase["eco"]
    eco["gravando"] = False
    jogador.x, jogador.y = eco["origem"]
    jogador.vy = 0.0
    eco["tocando"] = len(eco["fita"]) > 0
    eco["indice"] = 0
    fase["eventos"].append("eco_toca")


def acionar_eco(fase, teclado, tecla_livre):
    # na marca, E começa a gravar; gravando, E em qualquer lugar solta o eco
    eco = fase["eco"]
    if not (tecla_livre and teclado.key_pressed("E")):
        return False
    if eco["gravando"]:
        soltar_eco(fase)
        return True
    marca = perto_da_marca(fase)
    if marca is not None and jogador.no_chao:
        eco.update({"gravando": True, "fita": [], "tempo": 0.0, "tocando": False, "atual": None,
                    "origem": (jogador.x, jogador.y), "marca": marca})
        fase["eventos"].append("eco_grava")
        return True
    return False


def atualizar_eco(fase, tempo, pose):
    # gravando, guarda onde a íris está e como; tocando, o eco ocupa o lugar
    # do quadro da vez e some quando a fita acaba
    eco = fase["eco"]
    if eco["gravando"]:
        eco["fita"].append((jogador.x, jogador.y, jogador.direcao) + pose)
        eco["tempo"] = eco["tempo"] + tempo
        if eco["tempo"] >= cfg.tempo_eco - quase_zero:
            soltar_eco(fase)
    elif eco["tocando"]:
        eco["atual"] = eco["fita"][eco["indice"]]
        eco["indice"] = eco["indice"] + 1
        if eco["indice"] >= len(eco["fita"]):
            eco["tocando"] = False
    else:
        eco["atual"] = None


def diante_dos_monitores(fase):
    return fase["mirante"] is not None and jogador.no_chao and jogador.encostou(*fase["mirante"])


def acionar_monitores(fase, teclado, tecla_livre):
    # E diante dos monitores da cássia: a visão passa pelas câmeras do andar,
    # uma de cada vez, da esquerda para a direita
    pode = fase["olhar"] is None and fase["cameras"] and diante_dos_monitores(fase)
    if pode and tecla_livre and teclado.key_pressed("E"):
        fase["olhar"] = {"vez": 0, "tempo": 0.0}
        fase["eventos"].append("olhar")
        return True
    return False


def ponto_da_camera(fase, camera):
    # o meio do cone, como está agora: para onde a visão vai ao mostrá-la
    raios = leque(fase, camera)
    dx, dy, distancia = raios[len(raios) // 2]
    lx, ly = lente(camera)
    return lx + dx * distancia / 2, ly + dy * distancia / 2


def ponto_do_olhar(fase):
    # o ponto que a visão mostra enquanto a íris olha os monitores, ou None
    if fase["olhar"] is None:
        return None
    cameras = sorted(fase["cameras"], key=lambda camera: camera["x"])
    return ponto_da_camera(fase, cameras[fase["olhar"]["vez"]])


def atualizar_olhar(fase, tempo, interrompeu):
    # cada câmera fica na visão por um tempo; qualquer tecla de andar, pular
    # ou mexer devolve a visão à íris
    olhar = fase["olhar"]
    if olhar is None:
        return
    olhar["tempo"] = olhar["tempo"] + tempo
    if interrompeu and olhar["tempo"] > 0.25:
        fase["olhar"] = None
    elif olhar["tempo"] >= cfg.tempo_de_olhar:
        olhar["vez"] = olhar["vez"] + 1
        olhar["tempo"] = 0.0
        if olhar["vez"] >= len(fase["cameras"]):
            fase["olhar"] = None
        else:
            fase["eventos"].append("olhar")


def sentido_da_esteira(fase, celula):
    # o da célula, senão o do andar; o canal ligado repinta todas ao contrário
    sentido = fase["esteiras"][celula] or fase["esteira"]["sentido"]
    if esteiras_invertidas(fase):
        return "esquerda" if sentido == "direita" else "direita"
    return sentido


def esteiras_invertidas(fase):
    # número ímpar de inversores ligados: um desfaz o outro
    canais = fase["esteira"].get("canais", [])
    return sum(1 for canal in canais if canal_ativo(fase, canal)) % 2 == 1


def atualizar_esteiras(fase):
    # só avisa quando as setas mudam de lado
    agora = esteiras_invertidas(fase)
    if agora != fase["esteira"].get("antes", False):
        fase["eventos"].append("esteira")
    fase["esteira"]["antes"] = agora


def esteira_sob_os_pes(fase):
    # velocidade com que o chão leva a íris: 0 fora de esteira
    if not jogador.no_chao:
        return 0.0
    meio = jogador.x + cfg.largura_jogador / 2
    celula = (int(meio // cfg.tile) * cfg.tile, int((jogador.y + cfg.altura_jogador) // cfg.tile) * cfg.tile)
    if celula not in fase["esteiras"]:
        return 0.0
    return cfg.vel_esteira if sentido_da_esteira(fase, celula) == "direita" else -cfg.vel_esteira


def controle_ativo(controle, regra):
    if "ligada" in controle:
        return controle["ligada"]
    if regra == "todos":
        return controle["pressionado"] or controle["memoria"] > 0
    return controle["pressionado"]


def atualizar_canais(fase):
    # "qualquer": basta um controle ativo; "todos": precisa de todos
    # a tranca de segredo aberta vale como alavanca ligada
    por_canal = {}
    for controle in fase["botoes"] + fase["alavancas"] + fase["trancas"]:
        por_canal.setdefault(controle["canal"], []).append(controle)
    fase["canais"] = {}
    for canal, controles in por_canal.items():
        regra = fase["regras"].get(canal, "qualquer")
        ativos = [controle_ativo(c, regra) for c in controles]
        fase["canais"][canal] = all(ativos) if regra == "todos" else any(ativos)


def canal_ativo(fase, canal):
    return fase["canais"].get(canal, False)


def fontes_da_porta(fase, porta):
    # quantos controles do canal "todos" já valem, e quantos são: (ativos,
    # total). None quando não há o que contar: canal comum, um controle só
    # ou porta de paridade
    regra = fase["regras"].get(porta["canal"], "qualquer")
    if regra != "todos" or porta["canais"]:
        return None
    controles = [c for c in fase["botoes"] + fase["alavancas"] if c["canal"] == porta["canal"]]
    if len(controles) < 2:
        return None
    return sum(1 for c in controles if controle_ativo(c, regra)), len(controles)


def porta_acionada(fase, porta):
    # com vários canais, vale a paridade: cada alavanca ligada desfaz a outra
    if porta["canais"]:
        return sum(1 for canal in porta["canais"] if canal_ativo(fase, canal)) % 2 == 1
    return canal_ativo(fase, porta["canal"])


def vao_ocupado(fase, porta):
    # fechar por cima da íris a prendia na parede: a colisão horizontal
    # só resolve com vx != 0
    if jogador.encostou(porta["x"], porta["y"], cfg.tile, cfg.altura_porta):
        return True
    if eco_encosta(fase, porta["x"], porta["y"], cfg.tile, cfg.altura_porta):
        return True
    for caixa in fase["caixas"]:
        if cfg.colidiu(caixa["x"], caixa["y"], cfg.tile, cfg.tile,
                       porta["x"], porta["y"], cfg.tile, cfg.altura_porta):
            return True
    return False


def fechar_se_livre(fase, porta):
    if porta["aberta"] and not vao_ocupado(fase, porta):
        porta["aberta"] = False


def atualizar_porta_de_botao(fase, porta, ligada, tempo):
    # fecha 3 s depois de perder o acionamento
    porta["contando"] = not ligada and porta["folga"] > 0
    if ligada:
        porta["folga"] = cfg.folga_porta
        porta["aberta"] = True
        return
    porta["folga"] = max(0.0, porta["folga"] - tempo)
    if porta["folga"] <= quase_zero:
        fechar_se_livre(fase, porta)


def atualizar_porta_de_alavanca(fase, porta, ligada):
    if ligada:
        porta["aberta"] = True
    else:
        fechar_se_livre(fase, porta)


def atualizar_porta_de_relogio(fase, porta, ativo, tempo, passos):
    # abre na passagem de desligado para ligado e fecha depois de duracao,
    # mesmo com o canal ainda ativo; só reabre numa nova ativação. com
    # "passos", o que ela conta são os passos da íris, não os segundos
    if ativo and not porta["ativo_antes"]:
        porta["aberta"] = True
        porta["restante"] = porta["passos"] or porta["duracao"]
    porta["ativo_antes"] = ativo
    porta["restante"] = max(0.0, porta["restante"] - (passos if porta["passos"] else tempo))
    if porta["restante"] <= quase_zero:
        fechar_se_livre(fase, porta)


def atualizar_portas(fase, tempo, passos=0):
    # a invertida abre com o canal desligado; nenhuma fecha com o vão ocupado
    atualizar_canais(fase)
    for porta in fase["portas"]:
        ativo = porta_acionada(fase, porta)
        ligada = ativo != porta["invertida"]
        if porta["tipo"] == "relogio":
            atualizar_porta_de_relogio(fase, porta, ativo, tempo, passos)
        elif porta["tipo"] == "botao":
            atualizar_porta_de_botao(fase, porta, ligada, tempo)
        else:
            # a de alavanca e a de segredo: abertas enquanto o canal vale
            atualizar_porta_de_alavanca(fase, porta, ligada)


def marcas_de_tempo(porta):
    # uma marca por segundo restante: porta de botão em contagem, relógio aberto
    if porta["tipo"] == "relogio" and porta["aberta"]:
        return math.ceil(porta["restante"] - quase_zero)
    if porta["tipo"] == "botao" and porta["contando"]:
        return math.ceil(porta["folga"] - quase_zero)
    return 0


def lente(camera):
    # o ponto de onde a câmera vê: a lente do png, espelhada com ele
    dx, dy = cfg.lente_camera
    if camera["direcao"] == "esquerda":
        dx = cfg.tile - 1 - dx
    return camera["x"] + dx, camera["y"] + dy


def no_leque(camera, x, y):
    # dentro do cone: ao alcance da lente e entre os dois raios da borda
    lx, ly = lente(camera)
    dx, dy = x - lx, y - ly
    if camera["direcao"] == "esquerda":
        dx = -dx
    if math.hypot(dx, dy) > camera["alcance"] * cfg.tile:
        return False
    angulo = math.degrees(math.atan2(dy, dx))
    return abs(angulo - camera["inclinacao"]) <= camera["abertura"] / 2


def portas_que_cegam(fase):
    # células das portas fechadas: com as paredes, é o que corta a visão
    celulas = set()
    for porta in fase["portas"]:
        if not porta["aberta"]:
            celulas.add((porta["x"], porta["y"]))
            celulas.add((porta["x"], porta["y"] + cfg.tile))
    return celulas


def alcance_do_raio(fase, fechadas, x, y, dx, dy, limite):
    # até onde vai um raio saído de (x, y) na direção unitária (dx, dy):
    # a primeira célula de parede ou de porta fechada, ou o limite. anda de
    # fronteira em fronteira da grade; caixa não corta
    t = cfg.tile
    cx, cy = int(x // t), int(y // t)
    passo_x, passo_y = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
    longe = float("inf")
    proximo_x = ((cx + (dx > 0)) * t - x) / dx if dx != 0 else longe
    proximo_y = ((cy + (dy > 0)) * t - y) / dy if dy != 0 else longe
    salto_x = t / abs(dx) if dx != 0 else longe
    salto_y = t / abs(dy) if dy != 0 else longe
    while True:
        if proximo_x < proximo_y:
            distancia, proximo_x, cx = proximo_x, proximo_x + salto_x, cx + passo_x
        else:
            distancia, proximo_y, cy = proximo_y, proximo_y + salto_y, cy + passo_y
        if distancia >= limite:
            return limite
        celula = (cx * t, cy * t)
        if celula in fase["celulas_parede"] or celula in fechadas:
            return distancia


def leque(fase, camera):
    # o cone como a câmera o vê agora: um raio por fatia da abertura, cada um
    # com a direção e a distância até onde chega. é o que se desenha, e porta
    # fechada ou parede o encurtam
    lx, ly = lente(camera)
    fechadas = portas_que_cegam(fase)
    limite = camera["alcance"] * cfg.tile
    sentido = 1 if camera["direcao"] == "direita" else -1
    primeiro = camera["inclinacao"] - camera["abertura"] / 2
    raios = []
    for i in range(cfg.raios_do_cone + 1):
        angulo = math.radians(primeiro + camera["abertura"] * i / cfg.raios_do_cone)
        dx, dy = sentido * math.cos(angulo), math.sin(angulo)
        raios.append((dx, dy, alcance_do_raio(fase, fechadas, lx, ly, dx, dy, limite)))
    return raios


def pontos_do_corpo():
    # a íris para a câmera: três colunas de pontos, da cabeça aos pés
    return [(jogador.x + dx, jogador.y + dy) for dx in (2, 8, 14) for dy in (4, 18, 32, 44)]


def vendo(fase, camera):
    # basta um ponto do corpo dentro do cone e com a linha até a lente livre
    lx, ly = lente(camera)
    fechadas = None
    for x, y in pontos_do_corpo():
        if not no_leque(camera, x, y):
            continue
        if fechadas is None:
            fechadas = portas_que_cegam(fase)
        distancia = math.hypot(x - lx, y - ly)
        if distancia < 1:
            return True
        livre = alcance_do_raio(fase, fechadas, lx, ly, (x - lx) / distancia, (y - ly) / distancia, distancia)
        if livre >= distancia - 0.01:
            return True
    return False


def atualizar_cameras(fase, tempo):
    # soma o tempo com a íris vista e zera na hora em que ela some.
    # devolve True quando uma câmera chega ao tempo de detecção
    detectada = False
    for camera in fase["cameras"]:
        if camera["canal"] is not None and canal_ativo(fase, camera["canal"]):
            camera["estado"] = "desligada"
            camera["contador"] = 0.0
            continue
        camera["contador"] = camera["contador"] + tempo if vendo(fase, camera) else 0.0
        camera["estado"] = "alerta" if camera["contador"] > 0 else "vigiando"
        if camera["contador"] >= cfg.tempo_deteccao - quase_zero:
            detectada = True
    return detectada


def saida_aberta(fase):
    # a saída com canal só deixa passar depois que a tranca dele abriu
    return fase["canal_da_saida"] is None or canal_ativo(fase, fase["canal_da_saida"])


def chegou_na_saida(fase):
    s = fase["saida"]
    return s is not None and saida_aberta(fase) and jogador.encostou(s[0], s[1], cfg.tile, cfg.altura_porta)


def camera_que_acende(fase, tinta):
    # a tinta só aparece dentro do cone de uma câmera ligada, com a linha
    # até a lente livre: devolve essa câmera, ou None
    fechadas = portas_que_cegam(fase)
    for camera in fase["cameras"]:
        if camera["estado"] == "desligada" or not no_leque(camera, tinta["x"], tinta["y"]):
            continue
        lx, ly = lente(camera)
        distancia = math.hypot(tinta["x"] - lx, tinta["y"] - ly)
        dx, dy = (tinta["x"] - lx) / distancia, (tinta["y"] - ly) / distancia
        if alcance_do_raio(fase, fechadas, lx, ly, dx, dy, distancia) >= distancia - 0.01:
            return camera
    return None


def tocou_diamante(fase):
    d = fase["diamante"]
    return d is not None and jogador.encostou(d[0], d[1], cfg.tile, cfg.altura_porta)
