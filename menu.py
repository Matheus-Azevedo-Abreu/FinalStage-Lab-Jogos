import math
import configuracoes as cfg
import graficos
import painel
import fases

# telas de menu: diz qual botão foi clicado e desenha; quem troca de tela é o
# main. tudo na escala inteira da interface, posicionado pelo tamanho da tela

largura_botao = 192
altura_botao = 40
espaco_botao = 12
# o letreiro do jogo, no alto do menu, e o vão dele até o primeiro botão
altura_do_letreiro = 62
# ranking: a chapa de cada lugar e quantos lugares há (pontuacao.lugares)
altura_da_chapa = 56
largura_da_chapa = 384
lugares_do_ranking = 5

# botões de cada tela: nome e texto de reserva
botoes = {
    "menu": [("continuar", "CONTINUAR"), ("jogar", "JOGAR"), ("treino", "TREINO"), ("ranking", "RANKING"),
             ("controles", "CONTROLES"), ("sair", "SAIR")],
    "controles": [("voltar", "VOLTAR")],
    "ranking": [("voltar", "VOLTAR")],
    "pausa": [("continuar", "CONTINUAR"), ("reiniciar", "REINICIAR"), ("menu_inicial", "MENU INICIAL")],
}

# o que o menu mostra a mais: continuar só com uma corrida em curso, e o
# melhor tempo só depois de uma corrida inteira; quem preenche é o main
situacao = {"continuar": False, "melhor_total": None, "melhores": {}, "lugar": None}

# relógio do menu, para o que se mexe nele: chuva, brilho do título, botões
vida = {"tempo": 0.0}

# linhas da tela de controles: teclas e o que fazem
controles = [
    (["tecla-esquerda.png", "tecla-direita.png", "tecla-a.png", "tecla-d.png"], "mover"),
    (["tecla-espaco.png"], "pular"),
    (["tecla-e.png"], "mexer e examinar"),
    (["tecla-c.png"], "abrir o caderno"),
    (["tecla-esc.png"], "pausar"),
    (["tecla-r.png"], "reiniciar o andar"),
    (["tecla-m.png"], "ligar e desligar o som"),
]
altura_linha = 38

cor_texto = (255, 224, 138)
cor_reserva = (42, 40, 72)
cor_reserva_ativa = (58, 63, 99)


def u(valor):
    return valor * cfg.escala_interface


def arquivo_do_botao(nome, ativo):
    return "botao-" + nome.replace("_", "-") + ("-ativo" if ativo else "") + ".png"


def arquivos():
    # tudo o que as telas carregam, para o main pré-carregar
    nomes = ["menu-fundo.png", "titulo-final-stage.png", "titulo-controles.png", "titulo-pausa.png",
             "titulo-concluido.png", "titulo-detectada.png", "titulo-ranking.png", "placa-ranking.png",
             "cena-abertura.png", "buril.png"]
    nomes += [arquivo for arquivo, _, _ in cfg.cursores.values()]
    for lista in botoes.values():
        for nome, _ in lista:
            nomes += [arquivo_do_botao(nome, False), arquivo_do_botao(nome, True)]
    for teclas, _ in controles:
        nomes += teclas
    return nomes


def topo_dos_controles():
    # título, linhas e o botão voltar, centrados juntos na vertical
    bloco = u(27 + 30 + altura_linha * len(controles) + espaco_botao + altura_botao)
    return (cfg.altura_tela - bloco) // 2


def botoes_da_tela(tela):
    # no menu, continuar só existe com uma corrida em curso
    if tela == "menu" and not situacao["continuar"]:
        return botoes["menu"][1:]
    return botoes[tela]


def topo_do_menu():
    # o letreiro e a coluna de botões, centrados juntos na vertical, com a
    # linha da melhor noite embaixo: cabe numa tela de 384 de altura
    bloco = altura_do_letreiro + 10 + (altura_botao + 4) * len(botoes_da_tela("menu")) + 18
    return max(u(6), (cfg.altura_tela - u(bloco)) // 2)


def geometria_do_ranking():
    # o topo do título e o vão entre as chapas, em unidades de interface:
    # título, cinco chapas e o botão voltar cabem numa tela de 384 de altura
    altura = cfg.altura_tela // cfg.escala_interface
    fixo = 27 + altura_da_chapa * lugares_do_ranking + altura_botao
    vao = max(1, min(10, (altura - fixo - 8) // (lugares_do_ranking + 1)))
    topo = max(4, (altura - fixo - vao * (lugares_do_ranking + 1)) // 2)
    return topo, vao


def posicoes(tela):
    # canto de cada botão: no menu, uma coluna à esquerda; nas outras, no centro
    passo = u(altura_botao + espaco_botao)
    x = (cfg.largura_tela - u(largura_botao)) // 2
    lista = botoes_da_tela(tela)
    if tela == "menu":
        x, y, passo = u(40), topo_do_menu() + u(altura_do_letreiro + 10), u(altura_botao + 4)
    elif tela == "controles":
        y = topo_dos_controles() + u(27 + 30 + altura_linha * len(controles) + espaco_botao)
    elif tela == "ranking":
        topo, vao = geometria_do_ranking()
        y = u(topo + 27 + (altura_da_chapa + vao) * lugares_do_ranking + vao)
    else:
        y = cfg.altura_tela // 2 - u(40)
    return [(nome, texto, x, y + i * passo) for i, (nome, texto) in enumerate(lista)]


def botao_sob_mouse(tela, mouse):
    mx, my = mouse.get_position()
    for nome, _, x, y in posicoes(tela):
        if x <= mx < x + u(largura_botao) and y <= my < y + u(altura_botao):
            return nome
    return None


def clicado(tela, mouse):
    # botão clicado neste quadro, ou None
    if mouse.button_down(mouse.LEFT):
        return botao_sob_mouse(tela, mouse)
    return None


def desenhar_texto_centrado(conteudo, tamanho, centro_x, y):
    superficie = graficos.texto(conteudo, tamanho, cor_texto)
    graficos.desenhar_superficie(superficie, centro_x - superficie.get_width() // 2, y)


def desenhar_arte(nome, x, y):
    # arte da interface na escala inteira; devolve False sem o png
    arte = graficos.interface(nome)
    if arte is not None:
        graficos.desenhar_superficie(arte, x, y)
    return arte is not None


def desenhar_titulo(arquivo, reserva, y):
    # letreiro em png, centrado; sem ele, o texto
    arte = graficos.interface(arquivo)
    if arte is None:
        desenhar_texto_centrado(reserva, u(24), cfg.largura_tela // 2, y)
        return u(27)
    graficos.desenhar_superficie(arte, (cfg.largura_tela - arte.get_width()) // 2, y)
    return arte.get_height()


def letra_da_tecla(tecla):
    return tecla.replace("tecla-", "").replace(".png", "").upper()


def preparar_textos():
    # fontes, textos e arte ampliada prontos antes do laço
    for teclas, acao in controles:
        graficos.texto(acao, u(16), cor_texto)
        for tecla in teclas:
            graficos.interface(tecla)
            if graficos.imagem(tecla) is None:
                graficos.texto(letra_da_tecla(tecla), u(16), cor_texto)
                graficos.bloco(u(cfg.tile), u(cfg.tile), cor_reserva)
    for nome in arquivos():
        graficos.interface(nome)
    graficos.cobrindo_nitida("menu-fundo.png", 0.6)
    graficos.cobrindo("fundo-10.png")
    graficos.cobrindo_nitida("cena-abertura.png")
    painel.preparar_falas()


def preparar_cursor():
    # sem o png da seta, fica o cursor do sistema
    if graficos.imagem(cfg.cursores["seta"][0]) is not None:
        graficos.esconder_cursor()


def desenhar_cursor(tela, mouse):
    # mão sobre botão, seta no resto; a ponta do desenho fica no ponteiro
    arquivo, ponta_x, ponta_y = cfg.cursores["mao" if botao_sob_mouse(tela, mouse) else "seta"]
    mx, my = mouse.get_position()
    desenhar_arte(arquivo, mx - u(ponta_x), my - u(ponta_y))


def desenhar_botao(nome, texto, x, y, ativo):
    # sem png, um bloco com o texto
    if desenhar_arte(arquivo_do_botao(nome, ativo), x, y):
        return
    cor = cor_reserva_ativa if ativo else cor_reserva
    graficos.desenhar(graficos.bloco(u(largura_botao), u(altura_botao), cor), x, y)
    desenhar_texto_centrado(texto, u(16), x + u(largura_botao) // 2, y + u(10))


def desenhar_botoes(tela, mouse):
    # o botão sob o mouse acende e avança um pouco, com uma seta ao lado
    sob = botao_sob_mouse(tela, mouse)
    for nome, texto, x, y in posicoes(tela):
        avanco = u(4) if nome == sob else 0
        desenhar_botao(nome, texto, x + avanco, y, nome == sob)
        if nome == sob:
            vai = u(2) if int(vida["tempo"] * 4) % 2 else 0
            painel.rotulo(">", u(16), "titulo", x - u(14) + vai, y + u(10))


def desenhar_chuva(alfa=46):
    # garoa fina na frente da pintura: a noite da abertura já começa no menu
    gota = graficos.translucido(u(1), u(7), (163, 174, 200), alfa)
    for i in range(70):
        x = (i * 137 + vida["tempo"] * 60) % (cfg.largura_tela + 40) - 20
        y = (i * 71 + vida["tempo"] * (420 + 40 * (i % 5))) % (cfg.altura_tela + 20) - 20
        graficos.desenhar_superficie(gota, int(x), int(y))


def linhas_do_predio():
    # o prédio em dez linhas, a cobertura em cima: x, y, largura, altura de cada
    largura, altura = u(176), u(13)
    x = cfg.largura_tela - largura - u(36)
    y = cfg.altura_tela - u(40) - altura * len(fases.ANDARES)
    return [(len(fases.ANDARES) - 1 - i, x, y + i * altura, largura, altura) for i in range(len(fases.ANDARES))]


def andar_liberado(indice):
    # dá para rejogar o que já foi vencido e o seguinte
    return indice == 0 or indice in situacao["melhores"] or (indice - 1) in situacao["melhores"]


def andar_sob_mouse(mouse):
    # o andar da lista em que o mouse está, se ele pode ser jogado
    if not situacao["melhores"]:
        return None
    mx, my = mouse.get_position()
    for indice, x, y, largura, altura in linhas_do_predio():
        if x <= mx < x + largura and y <= my < y + altura and andar_liberado(indice):
            return indice
    return None


def desenhar_predio(mouse):
    # o tempo é a pontuação: a melhor marca de cada andar fica à vista, e um
    # clique leva de volta a ele. só aparece depois do primeiro andar vencido
    if not situacao["melhores"]:
        return
    linhas = linhas_do_predio()
    _, x, y, largura, altura = linhas[0]
    fundo = graficos.moldura(largura + u(16), altura * len(linhas) + u(30), u(1), painel.cor_caixa, 205, painel.cor_fio)
    graficos.desenhar_superficie(fundo, x - u(8), y - u(22))
    painel.rotulo("MELHORES TEMPOS", u(8), "titulo", x, y - u(16))
    sob = andar_sob_mouse(mouse)
    for indice, x, y, largura, altura in linhas:
        feito = indice in situacao["melhores"]
        alfa = 255 if feito else (150 if andar_liberado(indice) else 70)
        if indice == sob:
            graficos.desenhar_superficie(graficos.translucido(largura + u(8), altura, painel.cor_fio, 60), x - u(4), y)
        nome = fases.ANDARES[indice]["nome"].split(" ")[-1].upper()
        painel.rotulo("%02d" % (indice + 1), u(8), "titulo", x, y + u(2), "esquerda", alfa)
        painel.rotulo(nome, u(8), "titulo", x + u(24), y + u(2), "esquerda", alfa)
        tempo = painel.relogio(situacao["melhores"][indice]) if feito else "--:--"
        painel.rotulo(tempo, u(16), "numero", x + largura, y - u(2), "direita", alfa)
    painel.rotulo("CLIQUE NUM ANDAR PARA JOGAR DE NOVO", u(8), "titulo", x + largura, y + altura + u(6), "direita", 140)


def desenhar_principal(mouse):
    graficos.desenhar_nitida("menu-fundo.png", 0.6)
    desenhar_chuva()
    desenhar_arte("titulo-final-stage.png", u(24), topo_do_menu())
    desenhar_botoes("menu", mouse)
    desenhar_predio(mouse)
    if situacao["melhor_total"] is not None:
        # a melhor noite inteira, do andar 1 à cobertura
        base = cfg.altura_tela - u(26)
        painel.rotulo("MELHOR NOITE", u(8), "titulo", u(40), base + u(5))
        painel.rotulo(painel.relogio(situacao["melhor_total"]), u(16), "numero", u(128), base)
    painel.rotulo("UFF  ·  LABORATÓRIO DE JOGOS  ·  2026", u(8), "titulo", cfg.largura_tela // 2,
                  cfg.altura_tela - u(18), "centro", 110)
    desenhar_cursor("menu", mouse)


def desenhar_tecla(tecla, x, y):
    # sem png, um bloco com a letra; devolve a largura ocupada
    arte = graficos.interface(tecla)
    if arte is not None:
        graficos.desenhar_superficie(arte, x, y)
        return arte.get_width()
    graficos.desenhar(graficos.bloco(u(cfg.tile), u(cfg.tile), cor_reserva), x, y)
    desenhar_texto_centrado(letra_da_tecla(tecla), u(16), x + u(cfg.tile) // 2, y + u(8))
    return u(cfg.tile)


def desenhar_linha_de_controle(teclas, acao, y):
    meio = cfg.largura_tela // 2
    x = meio - u(160)
    for tecla in teclas:
        x = x + desenhar_tecla(tecla, x, y) + u(8)
    superficie = graficos.texto(acao, u(16), cor_texto)
    graficos.desenhar_superficie(superficie, meio + u(60), y + u(16) - superficie.get_height() // 2)


def desenhar_controles(mouse):
    graficos.desenhar_nitida("menu-fundo.png", 0.6)
    desenhar_chuva()
    graficos.desenhar_superficie(graficos.veu(170), 0, 0)
    topo = topo_dos_controles()
    desenhar_titulo("titulo-controles.png", "CONTROLES", topo)
    y = topo + u(27 + 30)
    for teclas, acao in controles:
        desenhar_linha_de_controle(teclas, acao, y)
        y = y + u(altura_linha)
    desenhar_botoes("controles", mouse)
    desenhar_cursor("controles", mouse)


def desenhar_pausa(mouse):
    # por cima da cena do jogo, que o main desenha antes
    graficos.desenhar_superficie(graficos.veu(160), 0, 0)
    desenhar_titulo("titulo-pausa.png", "PAUSA", cfg.altura_tela // 2 - u(96))
    desenhar_botoes("pausa", mouse)
    desenhar_cursor("pausa", mouse)


def placa_de_assinar():
    # a placa em branco da cobertura, grande, no meio da tela: x, y, largura, altura
    fator = max(1, min(int(cfg.largura_tela * 0.82) // 384, int(cfg.altura_tela * 0.6) // 128))
    largura, altura = 384 * fator, 128 * fator
    return (cfg.largura_tela - largura) // 2, (cfg.altura_tela - altura) // 2, largura, altura


def area_de_assinar():
    # a parte da placa em que se grava: dentro dos parafusos
    x, y, largura, altura = placa_de_assinar()
    return x + largura // 10, y + altura // 6, largura * 8 // 10, altura * 4 // 6


def desenhar_tracos(tracos, x, y, largura, altura, espessura):
    # o sulco escuro com o brilho um pouco abaixo, como o resto do latão
    for traco in tracos:
        pontos = [(x + px * largura, y + py * altura) for px, py in traco]
        graficos.tracar(pontos, painel.cor_brilho, espessura, espessura // 2 + 1, espessura // 2 + 1)
    for traco in tracos:
        pontos = [(x + px * largura, y + py * altura) for px, py in traco]
        graficos.tracar(pontos, painel.cor_sulco, espessura)


def desenhar_assinatura(tracos, mouse, riscando, relogio_da_tela):
    # a última tela de jogo: a placa em branco, a ponta que segue o mouse e o
    # nome que a jogadora grava segurando o botão
    graficos.desenhar_cobrindo("fundo-10.png")
    graficos.desenhar_superficie(graficos.veu(150), 0, 0)
    x, y, largura, altura = placa_de_assinar()
    chapa = graficos.ajustada("placa-leitura.png", largura, altura)
    if chapa is not None:
        graficos.desenhar_superficie(graficos.com_alfa(chapa, 255), x, y)
    ax, ay, al, aa = area_de_assinar()
    espessura = max(2, largura // 280)
    # a linha de assinar, gravada de leve
    graficos.tracar([(ax + al * 0.08, ay + aa * 0.86), (ax + al * 0.92, ay + aa * 0.86)], painel.cor_sulco, 1)
    desenhar_tracos(tracos, ax, ay, al, aa, espessura)
    painel.rotulo("COMO VOCÊ QUER SER GRAVADA?", u(16), "titulo", cfg.largura_tela // 2, y - u(40), "centro")
    painel.rotulo("SEGURE O BOTÃO DO MOUSE PARA GRAVAR   ·   R APAGA   ·   ENTER CONCLUI", u(8), "titulo",
                  cfg.largura_tela // 2, y + altura + u(20), "centro", 200)
    mx, my = mouse.get_position()
    if riscando:
        # limalha de latão saltando da ponta
        for n in range(5):
            dx = (int(relogio_da_tela * 60) * (7 + 3 * n)) % 15 - 7
            dy = (int(relogio_da_tela * 60) * (5 + 2 * n)) % 11 - 9
            graficos.desenhar_superficie(graficos.translucido(u(1), u(1), painel.cor_brilho, 255), mx + u(dx), my + u(dy))
    ponta = graficos.ajustada("buril.png", u(40), u(40))
    if ponta is not None:
        graficos.desenhar_superficie(ponta, mx - u(2), my - u(38))


def desenhar_abertura(fala, letras, escrita, relogio_da_tela):
    # a calçada, à noite: o rádio liga e a selene explica a etapa
    graficos.desenhar_nitida("cena-abertura.png")
    desenhar_chuva(60)
    painel.desenhar_conversa(fala, letras, escrita, relogio_da_tela)
    painel.rotulo("ESC PULA", u(8), "titulo", cfg.largura_tela - u(10), u(10), "direita", 150)


def desenhar_detectada():
    # por cima da cena, enquanto a íris é levada de volta à entrada do andar
    graficos.desenhar_superficie(graficos.veu(120), 0, 0)
    desenhar_titulo("titulo-detectada.png", "DETECTADA", cfg.altura_tela // 2 - u(60))
