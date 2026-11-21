import math
import configuracoes as cfg
import graficos
import mecanismos
import jogador
import animacao
import efeitos
import enquadramento
import cenario
import investigacao

# só desenha: lê o estado de jogo e o da animação, nunca decide regra.
# tudo em coordenadas de mundo; o que fica fora da visão não é desenhado

# peça de construção de cada parede interna, calculada uma vez por fase:
# "pecas" para a peça comum, sem tema; "atlas", a coluna e a linha da folha
# do tema; "sombras", as células vazias logo abaixo de um maciço no ar
cache_pecas = {"fase": None, "pecas": [], "atlas": [], "sombras": []}

# os raios do cone de cada câmera, com o estado das portas em que valem
cache_cones = {"fase": None, "portas": None, "raios": []}


# desenho em coordenadas de mundo: posição arredondada, só o que está na visão
no_mundo = graficos.no_mundo
superficie_no_mundo = graficos.superficie_no_mundo
quadro_no_mundo = graficos.quadro_no_mundo


def desenhar_arte(chave, x, y):
    # png quando existe, bloco de cor quando não; ícone sem png não aparece
    nome, dx, dy = cfg.arte[chave]
    arte = graficos.imagem(nome)
    if arte is not None:
        no_mundo(arte, x + dx, y + dy)
        return
    if chave not in cfg.reserva:
        return

    largura, altura, cor, recuo = cfg.reserva[chave]
    no_mundo(graficos.bloco(largura, altura, cor), x, y + recuo)


def desenhar_tira(chave, quadro, x, y, direcao="leste"):
    # quadro de um efeito em tira; False quando o png falta
    nome, quadros, _ = cfg.efeitos[chave]
    par = graficos.tira(nome, quadros)
    if par is None:
        return False
    if direcao == "oeste":
        quadro = quadros - 1 - quadro
    quadro_no_mundo(par[direcao], quadro, x, y)
    return True


def desenhar_jogador():
    nome, quadros, _, _ = cfg.animacoes[animacao.estado]
    par = graficos.tira(nome, quadros)
    if par is None:
        largura, altura, cor, _ = cfg.reserva["jogador"]
        no_mundo(graficos.bloco(largura, altura, cor), jogador.x, jogador.y)
        return

    quadro = animacao.quadro_atual()
    # na tira espelhada a ordem dos quadros se inverte
    if jogador.direcao == "oeste":
        quadro = quadros - 1 - quadro
    quadro_no_mundo(par[jogador.direcao], quadro,
                    jogador.x - cfg.recuo_iris_x, jogador.y - cfg.recuo_iris_y)


def arquivos_da_coluna(fase):
    # a coluna da emenda é da mesma matéria do andar
    if fase["tema"] is None:
        return "divisoria.png", "divisoria-pe.png"
    return "tema-%s-divisoria.png" % fase["tema"], "tema-%s-divisoria-pe.png" % fase["tema"]


def desenhar_coluna(fase, x):
    # coluna sem colisão na junta de dois fundos: divisória escurecida, pé no chão
    nome_do_corpo, nome_do_pe = arquivos_da_coluna(fase)
    corpo = graficos.escurecida(nome_do_corpo, cfg.escurecer_coluna)
    pe = graficos.escurecida(nome_do_pe, cfg.escurecer_coluna)
    if corpo is None or pe is None:
        return
    chao = cfg.altura_mundo - 2 * cfg.tile
    for y in range(0, chao, cfg.tile):
        no_mundo(corpo, x, y)
    no_mundo(pe, x, chao)


def desenhar_fundo(janela, fase):
    # o pano de fundo da versão 8 tem a largura do andar e é desenhado uma vez
    # só; o fundo antigo, de 800 px, se repete, e cada junta ganha uma coluna
    fundo = graficos.escurecida(fase["fundo"], cfg.escurecer_fundo)
    if fundo is None:
        janela.set_background_color(cfg.cor_fundo)
        return False
    if fundo.width >= fase["largura"]:
        no_mundo(fundo, 0, 0)
        return True
    if fase["aberto"]:
        # a céu aberto não cabe coluna: as cópias se alternam com o espelho
        virado = graficos.escurecida_espelhada(fase["fundo"], cfg.escurecer_fundo)
        for i, x in enumerate(range(0, fase["largura"], cfg.largura_fundo)):
            no_mundo(virado if i % 2 else fundo, x, 0)
        return True
    for x in range(0, fase["largura"], cfg.largura_fundo):
        no_mundo(fundo, x, 0)
    for x in range(cfg.largura_fundo, fase["largura"], cfg.largura_fundo):
        desenhar_coluna(fase, x - cfg.tile // 2)
    return True


def peca(ocupadas, bordas, x, y):
    # laje sob vão, com ponta onde a plataforma acaba; coluna de um tile é
    # divisória, com pé no chão ou sobre um vão
    t = cfg.tile
    esquerda = (x - t, y) in ocupadas
    direita = (x + t, y) in ocupadas
    if (x, y - t) not in ocupadas:
        if esquerda and not direita:
            return "laje_direita"
        if direita and not esquerda:
            return "laje_esquerda"
        return "laje"
    if esquerda or direita:
        return "parede_interna"
    if (x, y + t) in ocupadas and (x, y + t) not in bordas:
        return "divisoria"
    return "divisoria_pe"


def coluna_do_atlas(ocupadas, bordas, x, y):
    # a peça do tema pela vizinhança: a máscara dos vizinhos ocupados (cima 1,
    # baixo 2, esquerda 4, direita 8), de 0 a 15; apoiada no chão do andar,
    # de 16 a 23 (cima 1, esquerda 2, direita 4). a borda conta como vizinha
    t = cfg.tile
    cima, baixo = (x, y - t) in ocupadas, (x, y + t) in ocupadas
    esquerda, direita = (x - t, y) in ocupadas, (x + t, y) in ocupadas
    if (x, y + t) in bordas:
        return 16 + cima + 2 * esquerda + 4 * direita
    return cima + 2 * baixo + 4 * esquerda + 8 * direita


def quantas_antes(ocupadas, bordas, x, y, dx, dy):
    # células do mesmo maciço em fila naquela direção, sem contar a borda
    n = 0
    while (x + (n + 1) * dx, y + (n + 1) * dy) in ocupadas and (x + (n + 1) * dx, y + (n + 1) * dy) not in bordas:
        n = n + 1
    return n


def linha_do_atlas(ocupadas, bordas, x, y):
    # o corpo do tema é um desenho de 64 x 64 ancorado no canto de cima, à
    # esquerda, do maciço: coluna par ou ímpar, mais 2 se a linha é ímpar
    t = cfg.tile
    return quantas_antes(ocupadas, bordas, x, y, -t, 0) % 2 + 2 * (quantas_antes(ocupadas, bordas, x, y, 0, -t) % 2)


def com_detalhe(x, y):
    # uma célula em cada tantas ganha o detalhe raro do tema (as linhas 4 a 7
    # do atlas): sempre as mesmas, pela posição, sem sorteio em execução
    coluna, linha = x // cfg.tile, y // cfg.tile
    return (coluna * 31 + linha * 17 + coluna * linha * 7) % cfg.raridade_do_detalhe == 0


def calcular_pecas(fase):
    ocupadas = {(p[0], p[1]) for p in fase["paredes"]}
    bordas = {(p[0], p[1]) for p in fase["paredes"] if p[2]}
    internas = [p for p in fase["paredes"] if not p[2]]
    cache_pecas["fase"] = fase
    cache_pecas["pecas"] = [(peca(ocupadas, bordas, p[0], p[1]), p) for p in internas]
    cache_pecas["atlas"] = [(coluna_do_atlas(ocupadas, bordas, p[0], p[1]),
                             linha_do_atlas(ocupadas, bordas, p[0], p[1]), p) for p in internas]
    cache_pecas["sombras"] = [(p[0], p[1] + cfg.tile) for p in internas if (p[0], p[1] + cfg.tile) not in ocupadas]


def pecas_da_fase(fase):
    if cache_pecas["fase"] is not fase:
        calcular_pecas(fase)
    return cache_pecas["pecas"]


def atlas_do_tema(fase):
    # cada andar é feito do que o autor dele deixou: a folha de peças do tema,
    # já cortada. sem tema, ou sem o png, vale a peça de construção comum
    if fase["tema"] is None:
        return None
    return graficos.atlas("tema-%s.png" % fase["tema"], cfg.tile)


def desenhar_sombras_das_pecas():
    # o que fica no ar faz sombra na parede logo abaixo: lê como prateleira
    for n, alfa in enumerate(cfg.sombra_da_peca):
        faixa = graficos.translucido(cfg.tile, 2, cfg.cor_sombra_da_peca, alfa)
        for x, y in cache_pecas["sombras"]:
            superficie_no_mundo(faixa, x, y + 2 * n)


def desenhar_caixa(fase, caixa):
    # a coisa que se empurra também é do andar
    arte = graficos.imagem(fase["arte_caixa"]) if fase["arte_caixa"] else None
    if arte is not None:
        no_mundo(arte, caixa["x"], caixa["y"])
    else:
        desenhar_arte("caixa", caixa["x"], caixa["y"])


def desenhar_paredes(fase, tem_fundo):
    # parede de borda só aparece sem fundo; a interna usa as peças de construção
    if not tem_fundo:
        for p in fase["paredes"]:
            if p[2]:
                no_mundo(graficos.bloco(cfg.tile, cfg.tile, cfg.cores["parede"]), p[0], p[1])
    comuns = pecas_da_fase(fase)
    folha = atlas_do_tema(fase)
    if folha is None:
        for chave, p in comuns:
            desenhar_arte(chave, p[0], p[1])
        return
    tem_detalhe = len(folha) > 4
    for coluna, linha, p in cache_pecas["atlas"]:
        if tem_detalhe and com_detalhe(p[0], p[1]):
            linha = linha + 4
        superficie_no_mundo(folha[linha][coluna], p[0], p[1])
    desenhar_sombras_das_pecas()


def numero_no_mundo(conteudo, cor, x, y, tamanho=16):
    # número com contorno escuro, centrado em x: lê-se sobre qualquer parede
    numero = graficos.texto(conteudo, tamanho, cor, "numero")
    sombra = graficos.texto(conteudo, tamanho, cfg.contorno_marca_canal, "numero")
    x = x - numero.get_width() // 2
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        superficie_no_mundo(sombra, x + dx, y + dy)
    superficie_no_mundo(numero, x, y)


def desenhar_marcas(porta):
    # um quadrado magenta por segundo restante, centrado acima do ícone
    marcas = mecanismos.marcas_de_tempo(porta)
    if porta["passos"]:
        # a porta que conta passos mostra o número dos que restam; fechada,
        # apagado, quantos ela dá a quem passa
        cor = cfg.cor_marca if marcas else cfg.cor_passos_apagados
        numero_no_mundo(str(marcas or porta["passos"]), cor, porta["x"] + cfg.tile // 2, porta["y"] - 30)
        return
    if marcas == 0:
        return
    passo = cfg.lado_marca + 2
    x = porta["x"] + (cfg.tile - marcas * passo + 2) // 2
    marca = graficos.translucido(cfg.lado_marca, cfg.lado_marca, cfg.cor_marca, 255)
    for i in range(marcas):
        superficie_no_mundo(marca, x + i * passo, porta["y"] - 20)


def desenhar_marca_de_canal(fase, canal, x, y):
    # canal sem marca não mostra nada: esconder a ligação pode ser o desafio
    forma = fase["marcas"].get(canal)
    if forma is not None:
        superficie_no_mundo(graficos.marca_de_canal(forma), x, y)


def desenhar_pinos(fase, porta):
    # porta de canal "todos": um pino por controle, aceso quando ele já vale;
    # a fila fica centrada acima do ícone e das marcas de tempo
    fontes = mecanismos.fontes_da_porta(fase, porta)
    if fontes is None:
        return
    ativos, total = fontes
    lado = cfg.lado_pino
    passo = lado + 3
    x = porta["x"] + (cfg.tile - total * passo + 3) // 2
    contorno = graficos.translucido(lado + 2, lado + 2, cfg.contorno_pino, 255)
    for n in range(total):
        cor = cfg.cor_pino_aceso if n < ativos else cfg.cor_pino_apagado
        superficie_no_mundo(contorno, x + n * passo - 1, porta["y"] - 29)
        superficie_no_mundo(graficos.translucido(lado, lado, cor, 255), x + n * passo, porta["y"] - 28)


def desenhar_portas(fase):
    for i, porta in enumerate(fase["portas"]):
        desenhar_arte("icone_" + porta["tipo"], porta["x"], porta["y"])
        desenhar_pinos(fase, porta)
        # à direita do ícone, que vai de x + 8 a x + 24; com vários canais,
        # as marcas seguem em fila para a direita
        for n, canal in enumerate(porta["canais"] or [porta["canal"]]):
            desenhar_marca_de_canal(fase, canal, porta["x"] + 25 + 9 * n, porta["y"] - 12)
            # a invertida leva a marca riscada: abre com o canal desligado
            if porta["invertida"] and canal in fase["marcas"]:
                superficie_no_mundo(graficos.risco_de_invertida(), porta["x"] + 25 + 9 * n, porta["y"] - 12)
        desenhar_marcas(porta)
        quadro = efeitos.quadro_da_porta(i, porta["aberta"])
        if quadro is not None and desenhar_tira("porta_abrindo", quadro, porta["x"], porta["y"]):
            continue
        desenhar_arte("porta_aberta" if porta["aberta"] else "porta_fechada", porta["x"], porta["y"])


def desenhar_diamante(fase):
    d = fase["diamante"]
    if d is None:
        return
    desenhar_arte("diamante", d[0], d[1])
    dx, dy = cfg.brilho_diamante
    desenhar_tira("brilho", efeitos.quadro_do_brilho(), d[0] + dx, d[1] + dy)


def desenhar_halo(x, y, raio=None, alfa=None):
    # centrado no ponto dado, por trás do objeto
    raio = raio or cfg.raio_halo
    superficie_no_mundo(graficos.halo(raio, cfg.cor_halo, alfa or cfg.alfa_halo), x - raio, y - raio)


def desenhar_halos(fase):
    # antes dos mecanismos: tudo o que é interativo ganha a luz quente
    meio = cfg.tile // 2
    for botao in fase["botoes"]:
        desenhar_halo(botao["x"] + meio, botao["y"] + 4)
    for alavanca in fase["alavancas"]:
        desenhar_halo(alavanca["x"] + 8, alavanca["y"] + meio)
    for caixa in fase["caixas"]:
        desenhar_halo(caixa["x"] + meio, caixa["y"] + meio)
    if fase["placa"] is not None:
        desenhar_halo(fase["placa"][0] + meio, fase["placa"][1] + meio)
    for gaveta in fase["gavetas"]:
        desenhar_halo(gaveta["x"] + meio, gaveta["y"] + 5)
    for marca in fase["eco"]["marcas"]:
        desenhar_halo(marca[0] + meio, marca[1] + meio)
    for pista in fase["pistas"]:
        if not pista["lida"]:
            desenhar_halo(pista["x"] + meio, pista["y"] + meio)
    for tranca in fase["trancas"]:
        desenhar_halo(tranca["x"] + meio, tranca["y"] + meio)
    if fase["diamante"] is not None:
        pulso = 0.75 + 0.25 * math.sin(efeitos.relogio["tempo"] * 2.2)
        desenhar_halo(fase["diamante"][0] + meio, fase["diamante"][1] + 14,
                      cfg.raio_halo_diamante, int(cfg.alfa_halo_diamante * pulso) // 4 * 4)


def desenhar_poeira_no_ar(fase):
    # grãos frios, quase parados, que derivam com o tempo: o ar do prédio
    # vazio. a céu aberto não há
    if fase["aberto"]:
        return
    tempo = efeitos.relogio["tempo"]
    ox, oy = enquadramento.deslocamento()
    largura, altura = enquadramento.largura_visao(), enquadramento.altura_visao()
    for i in range(cfg.graos_no_ar):
        x = (i * 173 + tempo * (2 + i % 4)) % fase["largura"]
        y = 24 + (i * 89) % (cfg.altura_mundo - 80) + 5 * math.sin(tempo * 0.4 + i)
        if ox <= x < ox + largura + 1 and oy <= y < oy + altura + 1:
            grao = graficos.translucido(1, 1, cfg.cor_grao, 50 + 40 * (i % 3))
            graficos.desenhar_superficie(grao, int(x) - ox, int(y) - oy)


def desenhar_sombra_da_iris():
    if jogador.no_chao:
        superficie_no_mundo(graficos.sombra_no_chao(20), jogador.x - 2, jogador.y + cfg.altura_jogador - 2)


def desenhar_esteiras(fase):
    # a faixa por cima da peça do andar, e as setas pintadas correndo no
    # sentido em que ela leva
    faixa = graficos.imagem("esteira.png")
    seta = graficos.imagem("seta.png")
    if faixa is None or seta is None:
        return
    corrida = int(efeitos.relogio["tempo"] * 40) % 16
    for celula in fase["esteiras"]:
        no_mundo(faixa, celula[0], celula[1])
        direita = mecanismos.sentido_da_esteira(fase, celula) == "direita"
        arte = seta if direita else graficos.espelhada("seta.png")
        for n in range(2):
            x = (corrida + 16 * n) % 32 if direita else (31 - corrida + 16 * n) % 32
            if x <= 25:
                no_mundo(arte, celula[0] + x, celula[1] + 1)


def desenhar_gavetas(fase):
    for gaveta in fase["gavetas"]:
        arte = graficos.imagem("gaveta-aberta.png" if gaveta["aberta"] else "gaveta-fechada.png")
        if arte is not None:
            no_mundo(arte, gaveta["x"], gaveta["y"])
        marcas = mecanismos.marcas_da_gaveta(gaveta)
        marca = graficos.translucido(cfg.lado_marca, cfg.lado_marca, cfg.cor_marca, 255)
        for i in range(marcas):
            superficie_no_mundo(marca, gaveta["x"] + 9 + i * 5, gaveta["y"] - 6)


def trecho_de_viga(nome, x, largura):
    # a arte do trecho que começa em x: a ponta no começo, a ponta virada no
    # fim e o miolo no resto; viga de um trecho só é toda miolo
    ponta = None
    if largura > cfg.tile and x == 0:
        ponta = graficos.imagem(nome + "-ponta.png")
    elif largura > cfg.tile and x == largura - cfg.tile:
        ponta = graficos.espelhada(nome + "-ponta.png")
    return ponta or graficos.imagem(nome + ".png")


def desenhar_vigas(fase):
    # trecho por trecho, com as marcas das alavancas que a movem no meio. na
    # parede, tracejados, os dois lugares de cada viga: aonde ela vai se vê
    for viga in fase["vigas"]:
        for canto in (viga["repouso"], viga["outro"]):
            for x in range(0, viga["largura"], cfg.tile):
                lugar = trecho_de_viga("viga-lugar", x, viga["largura"])
                if lugar is not None:
                    no_mundo(lugar, canto[0] + x, canto[1])
    for viga in fase["vigas"]:
        for x in range(0, viga["largura"], cfg.tile):
            arte = trecho_de_viga("viga", x, viga["largura"])
            if arte is not None:
                no_mundo(arte, viga["x"] + x, viga["y"])
        meio = viga["x"] + viga["largura"] / 2 - 4.5 * len(viga["canais"])
        for n, canal in enumerate(viga["canais"]):
            desenhar_marca_de_canal(fase, canal, meio + 9 * n, viga["y"] + 4)


def desenhar_eco(fase):
    # a marca no chão; o eco, quando está tocando, com a pose que ela tinha
    eco = fase["eco"]
    # o porta-retratos fica virado para a parede; gravando ou repetindo, o
    # da vez se vira e mostra quem está nele
    marca = graficos.imagem("eco-marca.png")
    virada = graficos.imagem("eco-marca-ativa.png")
    for canto in eco["marcas"]:
        em_uso = (eco["gravando"] or eco["tocando"]) and canto is eco["marca"]
        arte = virada if em_uso and virada is not None else marca
        if arte is not None:
            no_mundo(arte, canto[0], canto[1])
    if eco["atual"] is None:
        return
    x, y, direcao, estado, quadro = eco["atual"]
    nome, quadros, _, _ = cfg.animacoes[estado]
    par = graficos.tira_do_eco(nome, quadros)
    if par is not None:
        quadro_no_mundo(par[direcao], quadros - 1 - quadro if direcao == "oeste" else quadro,
                        x - cfg.recuo_iris_x, y - cfg.recuo_iris_y)


def desenhar_pistas(fase):
    # o objeto da pista, quando ela tem um; sobre a que falta ler, um brilho
    # que pisca de tempo em tempo
    tempo = efeitos.relogio["tempo"]
    for n, pista in enumerate(fase["pistas"]):
        arte = graficos.imagem(pista["arte"]) if pista["arte"] else None
        if arte is not None:
            no_mundo(arte, pista["x"], pista["y"])
        momento = (tempo + 0.37 * n) % cfg.ciclo_do_brilho
        if not pista["lida"] and momento < cfg.efeitos["brilho_pista"][2]:
            canto = (19, 2) if arte is not None else (12, 10)
            desenhar_tira("brilho_pista", efeitos.quadro_do_efeito("brilho_pista", momento),
                          pista["x"] + canto[0], pista["y"] + canto[1])


def desenhar_trancas(fase):
    for tranca in fase["trancas"]:
        desenhar_arte("tranca_aberta" if tranca["ligada"] else "tranca", tranca["x"], tranca["y"])


def desenhar_tintas(fase):
    # o algarismo que só existe dentro do cone de uma câmera ligada
    for tinta in fase["tintas"]:
        if mecanismos.camera_que_acende(fase, tinta) is not None:
            numero_no_mundo(tinta["texto"], cfg.cor_tinta, tinta["x"], tinta["y"] - 16, 32)


def desenhar_placa(fase):
    # a placa de latão do autor do andar, na parede ao lado da entrada
    if fase["placa"] is not None:
        desenhar_arte("placa", fase["placa"][0], fase["placa"][1])


def desenhar_dica_de_acionar(fase, tipos):
    # a tecla sobre aquilo em que a íris pode mexer agora: ensina sem texto.
    # tipos: os que ainda pedem a dica ("alavanca", "gaveta", "eco")
    if "alavanca" in tipos:
        for alavanca in fase["alavancas"]:
            if jogador.encostou(alavanca["x"], alavanca["y"], cfg.largura_alavanca, cfg.altura_alavanca):
                desenhar_arte("tecla_acionar", alavanca["x"], alavanca["y"])
    if "gaveta" in tipos:
        for gaveta in fase["gavetas"]:
            if not gaveta["aberta"] and mecanismos.ao_alcance(gaveta):
                desenhar_arte("tecla_acionar", gaveta["x"] + 8, gaveta["y"] + 20)
    if "monitores" in tipos and fase["olhar"] is None and mecanismos.diante_dos_monitores(fase):
        desenhar_arte("tecla_acionar", fase["mirante"][0] + 26, fase["mirante"][1] - 100)
    if "eco" in tipos and not fase["eco"]["gravando"]:
        marca = mecanismos.perto_da_marca(fase)
        if marca is not None:
            desenhar_arte("tecla_acionar", marca[0] + 8, marca[1])
    # pista e tranca pedem a tecla sempre: é o jeito de saber que se pode ler
    if fase["olhar"] is None and not fase["eco"]["gravando"] and investigacao.aberto["tipo"] is None:
        coisa = investigacao.pista_ao_alcance(fase) or investigacao.tranca_ao_alcance(fase)
        if coisa is not None:
            # acima da cabeça da íris, que fica diante da coisa
            desenhar_arte("tecla_acionar", coisa["x"] + 8, coisa["y"] - 6)


def desenhar_mecanismos(fase):
    if fase["saida"] is not None:
        # trancada, a placa de luz da saída fica vermelha
        chave = "saida" if mecanismos.saida_aberta(fase) else "saida_trancada"
        desenhar_arte(chave, fase["saida"][0], fase["saida"][1])
    desenhar_diamante(fase)
    desenhar_portas(fase)
    for i, botao in enumerate(fase["botoes"]):
        chave = "botao_pressionado" if botao["pressionado"] else "botao_solto"
        if efeitos.no_meio("botoes", i):
            chave = "botao_meio"
        desenhar_arte(chave, botao["x"], botao["y"])
        desenhar_marca_de_canal(fase, botao["canal"], botao["x"] + 12, botao["y"] - 12)
    for i, alavanca in enumerate(fase["alavancas"]):
        chave = "alavanca_ligada" if alavanca["ligada"] else "alavanca_desligada"
        if efeitos.no_meio("alavancas", i):
            chave = "alavanca_meio"
        desenhar_arte(chave, alavanca["x"], alavanca["y"])
        desenhar_marca_de_canal(fase, alavanca["canal"], alavanca["x"] + 4, alavanca["y"] - 12)
    for caixa in fase["caixas"]:
        desenhar_caixa(fase, caixa)


def desenhar_cameras(fase):
    # a arte olha para a direita; para a esquerda, a cópia espelhada
    for camera in fase["cameras"]:
        nome = cfg.arte_camera[camera["estado"]]
        sprite = graficos.imagem(nome) if camera["direcao"] == "direita" else graficos.espelhada(nome)
        if sprite is not None:
            no_mundo(sprite, camera["x"], camera["y"])


def raios_das_cameras(fase):
    # o cone só muda de forma quando uma porta abre ou fecha: guardado até lá
    portas = tuple(porta["aberta"] for porta in fase["portas"])
    if cache_cones["fase"] is not fase or cache_cones["portas"] != portas:
        cache_cones["fase"] = fase
        cache_cones["portas"] = portas
        cache_cones["raios"] = [tuple(mecanismos.leque(fase, camera)) for camera in fase["cameras"]]
    return cache_cones["raios"]


def desenhar_cones(fase):
    # translúcido por cima da cena, da lente até a parede ou a porta fechada
    # que o corta: desligada, a câmera não tem cone
    for camera, raios in zip(fase["cameras"], raios_das_cameras(fase)):
        if camera["estado"] == "desligada":
            continue
        lx, ly = mecanismos.lente(camera)
        alcance = camera["alcance"] * cfg.tile
        cor, alfa = cfg.cor_cone[camera["estado"]]
        superficie, ox, oy = graficos.leque(raios, alcance, cor, alfa)
        superficie_no_mundo(superficie, lx - ox, ly - oy)
        # a contagem enche o cone de magenta, da câmera para fora (gdd, seção 4.2)
        degrau = int(cfg.degraus_do_alerta * min(1.0, camera["contador"] / cfg.tempo_deteccao))
        if degrau > 0:
            cor, alfa = cfg.cor_alerta
            cheio = alcance * degrau / cfg.degraus_do_alerta
            superficie, ox, oy = graficos.leque(raios, alcance, cor, alfa, cheio)
            superficie_no_mundo(superficie, lx - ox, ly - oy)


def desenhar_decoracoes(fase):
    for x, y, nome in fase["decoracoes"]:
        sprite = graficos.imagem(nome)
        if sprite is not None:
            no_mundo(sprite, x, y)


def preparar(fase):
    # tudo o que o andar desenha, pronto antes do laço
    for camera in fase["cameras"]:
        raios = tuple(mecanismos.leque(fase, camera))
        for cor, alfa in cfg.cor_cone.values():
            graficos.leque(raios, camera["alcance"] * cfg.tile, cor, alfa)
        for nome in cfg.arte_camera.values():
            graficos.imagem(nome)
            graficos.espelhada(nome)
    graficos.translucido(cfg.lado_marca, cfg.lado_marca, cfg.cor_marca, 255)
    graficos.translucido(cfg.lado_pino + 2, cfg.lado_pino + 2, cfg.contorno_pino, 255)
    for cor in (cfg.cor_pino_aceso, cfg.cor_pino_apagado):
        graficos.translucido(cfg.lado_pino, cfg.lado_pino, cor, 255)
    for forma in fase["marcas"].values():
        graficos.marca_de_canal(forma)
    graficos.carregar([nome for _, _, nome in fase["decoracoes"]])
    graficos.imagem(cfg.arte["tecla_acionar"][0])
    atlas_do_tema(fase)
    for alfa in cfg.sombra_da_peca:
        graficos.translucido(cfg.tile, 2, cfg.cor_sombra_da_peca, alfa)
    if fase["arte_caixa"]:
        graficos.imagem(fase["arte_caixa"])
    graficos.halo(cfg.raio_halo, cfg.cor_halo, cfg.alfa_halo)
    graficos.carregar(["gaveta-aberta.png", "gaveta-fechada.png", "viga.png", "viga-lugar.png", "esteira.png",
                       "seta.png", "eco-marca.png", "eco-marca-ativa.png", "viga-ponta.png", "viga-lugar-ponta.png"])
    for nome in ("viga-ponta.png", "viga-lugar-ponta.png"):
        graficos.espelhada(nome)
    graficos.risco_de_invertida()
    graficos.carregar([pista["arte"] for pista in fase["pistas"] if pista["arte"]])
    cenario.preparar(fase)
    graficos.espelhada("seta.png")
    if fase["eco"]["marcas"]:
        for nome, quadros, _, _ in cfg.animacoes.values():
            graficos.tira_do_eco(nome, quadros)
    graficos.carregar_escurecidas(arquivos_da_coluna(fase), cfg.escurecer_coluna)
    graficos.sombra_no_chao(20)
    for nivel in range(3):
        graficos.translucido(1, 1, cfg.cor_grao, 50 + 40 * nivel)
    if fase["aberto"]:
        graficos.escurecida_espelhada(fase["fundo"], cfg.escurecer_fundo)


def desenhar_poeiras():
    # na frente da íris e das caixas: a poeira sobe dos pés
    for chave, x, y, tempo, direcao in efeitos.poeiras:
        desenhar_tira(chave, efeitos.quadro_do_efeito(chave, tempo), x, y, direcao)


def desenhar_cena(janela, fase, dica_de_acionar=False):
    tem_fundo = desenhar_fundo(janela, fase)
    cenario.desenhar(fase)
    desenhar_paredes(fase, tem_fundo)
    desenhar_decoracoes(fase)
    desenhar_esteiras(fase)
    desenhar_halos(fase)
    desenhar_placa(fase)
    desenhar_pistas(fase)
    desenhar_trancas(fase)
    desenhar_tintas(fase)
    desenhar_vigas(fase)
    desenhar_gavetas(fase)
    desenhar_eco(fase)
    desenhar_mecanismos(fase)
    desenhar_cameras(fase)
    desenhar_sombra_da_iris()
    desenhar_jogador()
    desenhar_cones(fase)
    desenhar_poeiras()
    desenhar_poeira_no_ar(fase)
    if dica_de_acionar is not False:
        # True vale por todos os tipos; uma coleção, só pelos que ela traz
        tipos = ("alavanca", "gaveta", "eco", "monitores") if dica_de_acionar is True else dica_de_acionar
        desenhar_dica_de_acionar(fase, tipos)
    # o tremor do flagrante entra como fração da câmera: só a imagem balança
    fx, fy = enquadramento.fracao()
    tx, ty = efeitos.deslocamento_do_tremor()
    graficos.ampliar_visao((max(0.0, min(1.0, fx + tx)), max(0.0, min(1.0, fy + ty))))
    graficos.desenhar_superficie(graficos.vinheta(), 0, 0)
