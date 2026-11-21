import configuracoes as cfg
import graficos
import painel
import documentos
import investigacao
import fases

# o que a investigação põe por cima do andar: a folha da pista, as rodas da
# tranca e o caderno. só desenha, em unidades da interface; o que está
# aberto e o que as rodas mostram vêm de investigacao.py

# tinta de quem escreveu, giz do que está na parede, e as cores da tranca
tinta = (27, 24, 48)
tinta_do_titulo = (82, 91, 130)
giz = (217, 222, 234)
cor_certa = (69, 196, 106)
cor_errada = (216, 58, 58)
u = painel.u

# a folha: tamanho, margem do texto, onde começa o texto e a altura da linha
folha = (256, 192)
margem = 16
topo_do_texto = 28
entrelinha = 16
# quantas pistas o caderno mostra de uma vez
linhas_do_caderno = 9


def ampliado(conteudo, cor, papel="numero", tamanho=16):
    # a letra desenhada no tamanho de origem e ampliada por inteiro: a largura
    # é a mesma conta em toda tela, e o pixel fica nítido
    return graficos.ajustada_superficie(graficos.texto(conteudo, tamanho, cor, papel), cfg.escala_interface)


def canto_da_folha():
    return (cfg.largura_tela - u(folha[0])) // 2, (cfg.altura_tela - u(folha[1])) // 2 - u(6)


def escurecer():
    graficos.desenhar_superficie(graficos.veu(165), 0, 0)


def rodape(texto):
    painel.rotulo(texto, u(8), "titulo", cfg.largura_tela // 2, canto_da_folha()[1] + u(folha[1] + 6), "centro", 210)


def desenhar_pista(nome, do_caderno):
    # a folha no meio da tela: título, figura (se houver) e o texto
    pista = documentos.pistas[nome]
    x, y = canto_da_folha()
    papel = graficos.interface("papel-%s.png" % pista["papel"])
    if papel is not None:
        graficos.desenhar_superficie(papel, x, y)
    na_parede = pista["papel"] == "parede"
    cor = giz if na_parede else tinta
    graficos.desenhar_superficie(ampliado(pista["titulo"], cfg.cor_marca_canal if na_parede else tinta_do_titulo,
                                          "titulo", 8), x + u(margem), y + u(11))
    topo = y + u(topo_do_texto)
    figura = graficos.interface(pista["figura"]) if "figura" in pista else None
    if figura is not None:
        graficos.desenhar_superficie(figura, x + (u(folha[0] - 4) - figura.get_width()) // 2, topo)
        topo = topo + figura.get_height() + u(4)
    for linha in documentos.linhas_da_pista(nome):
        graficos.desenhar_superficie(ampliado(linha, cor), x + u(margem), topo)
        topo = topo + u(entrelinha)
    rodape("E  VOLTA AO CADERNO" if do_caderno else "E  FECHA")


def arte_do_simbolo(simbolo, cor):
    # algarismo em letra grande; seta, o png dela
    if len(simbolo) == 1:
        return graficos.ajustada_superficie(graficos.texto(simbolo, 32, cor, "numero"), cfg.escala_interface)
    return graficos.interface("simbolo-%s.png" % simbolo)


def desenhar_tranca(aberto):
    # a chapa da tranca: o rótulo, uma roda por posição do segredo e as teclas
    tranca = aberto["tranca"]
    enigma = documentos.enigmas[tranca["enigma"]]
    rodas = investigacao.mostrado(tranca)
    passo = 34
    largura = u(max(232, passo * len(rodas) + 40))
    altura = u(136)
    x, y = (cfg.largura_tela - largura) // 2, (cfg.altura_tela - altura) // 2
    # a tranca errada treme para os lados enquanto o erro dura
    if aberto["erro"] > 0:
        x = x + u(3) * (1 if int(aberto["erro"] * 30) % 2 else -1)
    certa = aberto["acerto"] > 0
    fio = cor_certa if certa else (cor_errada if aberto["erro"] > 0 else painel.cor_fio)
    graficos.desenhar_superficie(graficos.moldura(largura, altura, u(2), painel.cor_caixa, 242, fio), x, y)
    painel.rotulo(enigma["rotulo"], u(8), "titulo", x + largura // 2, y + u(10), "centro")
    inicio = x + (largura - u(passo * len(rodas) - 6)) // 2
    for n, simbolo in enumerate(rodas):
        da_vez = n == aberto["roda"] and not certa
        rx = inicio + u(passo * n)
        moldura_da_roda = graficos.interface("roda-ativa.png" if da_vez else "roda.png")
        if moldura_da_roda is not None:
            graficos.desenhar_superficie(moldura_da_roda, rx, y + u(26))
        arte = arte_do_simbolo(simbolo, cor_certa if certa else giz)
        if arte is not None:
            graficos.desenhar_superficie(arte, rx + (u(28) - arte.get_width()) // 2,
                                         y + u(54) - arte.get_height() // 2)
    if certa:
        painel.rotulo("ABERTA", u(8), "titulo", x + largura // 2, y + u(92), "centro", 255, cor_certa)
    elif tranca["erros"]:
        painel.rotulo("ERROS ANOTADOS: %d" % tranca["erros"], u(8), "titulo", x + largura // 2, y + u(92), "centro",
                      255, cor_errada)
    painel.rotulo("A D  ESCOLHE A RODA     W S  GIRA", u(8), "titulo", x + largura // 2, y + u(106), "centro", 190)
    painel.rotulo("ENTER  CONFERE     ESC  SAI", u(8), "titulo", x + largura // 2, y + u(118), "centro", 190)


# quantas pistas cada andar tem, contadas uma vez
pistas_por_andar = {}


def pistas_do_andar(indice):
    if indice not in pistas_por_andar:
        pistas_por_andar[indice] = sum(linha.count("k") for linha in fases.andar_de(indice)["mapa"])
    return pistas_por_andar[indice]


def titulo_do_andar(indice, placas, lidas):
    # o nome do autor só aparece para quem leu a placa dele; ao lado, quantas
    # pistas do andar já estão no caderno: dá para saber se ficou alguma
    andar = fases.andar_de(indice)
    nome = painel.nome_do_andar(indice)
    if andar["ano"] is not None and indice in placas:
        nome = "%s — %s, %d" % (nome, andar["nome"].upper(), andar["ano"])
    return "%s   %d DE %d" % (nome, lidas, pistas_do_andar(indice))


def linhas_do_caderno_em_ordem(entradas, placas):
    # o caderno como lista: um cabeçalho por andar e, abaixo, as pistas dele;
    # cada linha: (texto, posição em entradas, ou None para o cabeçalho)
    linhas, andar_da_vez = [], None
    for posicao, (indice, nome) in enumerate(entradas):
        if indice != andar_da_vez:
            andar_da_vez = indice
            lidas = sum(1 for outro, _ in entradas if outro == indice)
            linhas.append((titulo_do_andar(indice, placas, lidas), None))
        linhas.append((documentos.pistas[nome]["titulo"], posicao))
    return linhas


def desenhar_caderno(aberto, entradas, placas):
    # a lista do que a íris já leu na noite, andar por andar
    x, y = canto_da_folha()
    papel = graficos.interface("papel-folha.png")
    if papel is not None:
        graficos.desenhar_superficie(papel, x, y)
    graficos.desenhar_superficie(ampliado("CADERNO", tinta_do_titulo, "titulo", 8), x + u(margem + 14), y + u(11))
    linhas = linhas_do_caderno_em_ordem(entradas, placas)
    if not linhas:
        graficos.desenhar_superficie(ampliado("Nada anotado ainda.", tinta), x + u(margem), y + u(topo_do_texto))
        rodape("ESC  FECHA")
        return
    # a janela de linhas acompanha a escolhida
    escolhida = [n for n, (_, posicao) in enumerate(linhas) if posicao == aberto["linha"]][0]
    primeira = max(0, min(escolhida - linhas_do_caderno // 2, len(linhas) - linhas_do_caderno))
    topo = y + u(topo_do_texto)
    for n in range(primeira, min(len(linhas), primeira + linhas_do_caderno)):
        texto, posicao = linhas[n]
        if posicao is None:
            graficos.desenhar_superficie(ampliado(texto, tinta_do_titulo, "titulo", 8), x + u(margem), topo + u(4))
        else:
            if n == escolhida:
                graficos.desenhar_superficie(graficos.translucido(u(folha[0] - 36), u(entrelinha - 1),
                                                                  cfg.cor_marca_canal, 110), x + u(margem - 2), topo)
            graficos.desenhar_superficie(ampliado(texto, tinta), x + u(margem + 8), topo)
        topo = topo + u(entrelinha)
    rodape("W S  ESCOLHE     E  LÊ     ESC  FECHA")


def desenhar(entradas, placas):
    # por cima da cena do andar, que continua lá, parada e escurecida
    aberto = investigacao.aberto
    if aberto["tipo"] is None:
        return
    escurecer()
    if aberto["tipo"] == "pista":
        desenhar_pista(aberto["pista"], aberto["do_caderno"])
    elif aberto["tipo"] == "tranca":
        desenhar_tranca(aberto)
    else:
        desenhar_caderno(aberto, entradas, placas)


def arquivos():
    # tudo o que a leitura mostra, para o main pré-carregar
    nomes = ["roda.png", "roda-ativa.png"]
    nomes += ["simbolo-%s.png" % simbolo for simbolo in documentos.rodas["setas"]]
    nomes += ["papel-%s.png" % papel for papel in sorted({pista["papel"] for pista in documentos.pistas.values()})]
    nomes += [pista["figura"] for pista in documentos.pistas.values() if "figura" in pista]
    return nomes + ["papel-folha.png"]
