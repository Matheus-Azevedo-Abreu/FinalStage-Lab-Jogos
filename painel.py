import configuracoes as cfg
import graficos

# o que fica por cima do jogo em resolução de tela: hud (andar e cronômetro,
# gdd seção 4.2) e o cartão de passagem entre andares

cor = (255, 224, 138)
cor_sombra = (14, 11, 22)


def u(valor):
    return valor * cfg.escala_interface


def relogio(segundos):
    minutos, resto = divmod(int(segundos), 60)
    return "%02d:%02d" % (minutos, resto)


def rotulo(conteudo, tamanho, papel, x, y, alinhar="esquerda", alfa=255, tinta=None):
    # texto com sombra de um pixel da interface; devolve a altura. dourado,
    # a não ser que venha outra tinta
    frente = graficos.texto(conteudo, tamanho, tinta or cor, papel)
    sombra = graficos.texto(conteudo, tamanho, cor_sombra, papel)
    if alinhar == "direita":
        x = x - frente.get_width()
    elif alinhar == "centro":
        x = x - frente.get_width() // 2
    for superficie in (sombra, frente):
        superficie.set_alpha(alfa)
    graficos.desenhar_superficie(sombra, x + u(1), y + u(1))
    graficos.desenhar_superficie(frente, x, y)
    return frente.get_height()


def nome_do_andar(indice):
    # o treino não tem número
    return "ANDAR %02d" % (indice + 1) if isinstance(indice, int) else "TREINO"


def milhar(pontos):
    # 10450 -> "10.450": o número grande se lê melhor separado
    return ("%d.%03d" % divmod(pontos, 1000)) if pontos >= 1000 else str(pontos)


def desenhar_hud(indice, segundos, pontos=None, bonus=0.0, aviso=None):
    # interface mínima: a tela pertence ao puzzle. no alto, o andar, o
    # cronômetro e, na noite, os pontos já ganhos; bonus (de 1 a 0) acende o
    # aviso do que somou pontos: a placa lida ou, com aviso, o texto dado
    margem = u(10)
    rotulo(nome_do_andar(indice), u(16), "titulo", margem, margem)
    rotulo(relogio(segundos), u(24), "numero", cfg.largura_tela - margem, margem - u(4), "direita")
    if pontos is None:
        return
    rotulo(milhar(pontos) + " PTS", u(8), "titulo", cfg.largura_tela - margem, margem + u(24), "direita", 220)
    if bonus > 0:
        rotulo(aviso or "PLACA LIDA  +%d" % cfg.bonus_mostrado, u(8), "titulo", cfg.largura_tela - margem,
               margem + u(38), "direita", int(255 * min(1.0, 2 * bonus)))


def desenhar_caderno_na_hud(pistas, do_andar=None):
    # no canto de baixo, discreto: a tecla do caderno e quantas pistas ele
    # tem; com do_andar, (lidas, total) do andar em curso
    if do_andar is not None and do_andar[1]:
        rotulo("C  CADERNO     PISTAS DO ANDAR  %d DE %d" % do_andar, u(8), "titulo", u(10), cfg.altura_tela - u(20),
               "esquerda", 170)
    elif pistas:
        rotulo("C  CADERNO  %d" % pistas, u(8), "titulo", u(10), cfg.altura_tela - u(20), "esquerda", 170)


def desenhar_passagem(escuridao, opacidade_cartao, indice, resultado=None):
    # o cartão do andar que vem; acima dele, em letra pequena, o que o andar
    # que acabou rendeu: (índice, segundos, pontos, letra)
    if escuridao > 0:
        graficos.desenhar_superficie(graficos.veu(int(255 * escuridao)), 0, 0)
    if opacidade_cartao > 0:
        alfa = int(255 * opacidade_cartao)
        meio = cfg.altura_tela // 2
        rotulo(nome_do_andar(indice), u(32), "titulo", cfg.largura_tela // 2, meio - u(24), "centro", alfa)
        if resultado is not None:
            anterior, segundos, pontos, letra = resultado
            linha = "%s   %s   %s PTS   %s" % (nome_do_andar(anterior), relogio(segundos), milhar(pontos), letra)
            rotulo(linha, u(8), "titulo", cfg.largura_tela // 2, meio + u(22), "centro", alfa)


def desenhar_olhar(vez, total):
    # a íris olha os monitores: qual câmera a visão mostra, no alto da tela
    rotulo("CÂMERA %d DE %d" % (vez, total), u(16), "titulo", cfg.largura_tela // 2, u(10), "centro")
    rotulo("QUALQUER TECLA VOLTA", u(8), "titulo", cfg.largura_tela // 2, u(30), "centro", 170)


def desenhar_licao(titulo, texto, opacidade):
    # treino: a lição da sala, no alto da tela, enquanto a íris está nela
    if opacidade <= 0:
        return
    alfa = int(255 * opacidade)
    largura = min(cfg.largura_tela - u(24), u(480))
    linhas = graficos.quebrar(texto, u(16), "numero", largura - u(20))
    altura = u(26) + u(17) * len(linhas)
    x = (cfg.largura_tela - largura) // 2
    y = u(30)
    caixa = graficos.moldura(largura, altura, u(1), cor_caixa, 222, cor_fio)
    graficos.desenhar_superficie(graficos.com_alfa(caixa, alfa), x, y)
    rotulo(titulo, u(8), "titulo", x + u(10), y + u(7), "esquerda", alfa)
    desenhar_linhas(texto, len(texto), largura - u(20), x + u(10), y + u(20), alfa)


# falas: a caixa da conversa, a linha do rádio e a placa lida. cores do gdd:
# o texto é claro e frio, o nome e o fio da caixa são dourados
cor_fala = (217, 222, 234)
cor_caixa = (14, 11, 22)
cor_fio = (232, 176, 74)
# gravação no latão: sulco escuro com a borda de baixo iluminada
cor_sulco = (74, 42, 14)
cor_brilho = (255, 232, 150)

nomes_das_vozes = {"selene": "SELENE", "iris": "ÍRIS"}

arquivos_de_retrato = ["retrato-neutra.png", "retrato-atenta.png", "retrato-cansada.png",
                       "retrato-desconfiada.png", "retrato-indecifravel.png",
                       "radio-falando.png", "radio-silencio.png", "placa-leitura.png"]


def arquivo_do_retrato(quem, retrato, falando):
    if quem == "selene":
        return "radio-falando.png" if falando else "radio-silencio.png"
    return "retrato-%s.png" % retrato


def desenhar_linhas(texto, letras, largura, x, y, alfa=255, tamanho=16):
    # o texto até a letra de agora, quebrado sempre do mesmo jeito: a
    # palavra não pula de linha no meio da escrita
    contadas = 0
    for linha in graficos.quebrar(texto, u(tamanho), "numero", largura):
        visivel = linha[:max(0, letras - contadas)]
        contadas = contadas + len(linha) + 1
        if visivel:
            superficie = graficos.texto(visivel, u(tamanho), cor_fala, "numero")
            graficos.desenhar_superficie(graficos.com_alfa(superficie, alfa), x, y)
        y = y + u(tamanho + 1)


def desenhar_conversa(fala, letras, escrita, relogio_da_tela, no_alto=False):
    # caixa embaixo, retrato à esquerda (dupla representação, gdd 6.5); no
    # alto quando a cena que importa está no chão, como no final
    quem, retrato, texto = fala
    largura = min(cfg.largura_tela - u(32), u(560))
    altura = u(104)
    x = (cfg.largura_tela - largura) // 2
    y = u(36) if no_alto else cfg.altura_tela - altura - u(16)
    graficos.desenhar_superficie(graficos.moldura(largura, altura, u(1), cor_caixa, 232, cor_fio), x, y)
    margem = u(12)
    if quem is not None:
        figura = graficos.ajustada(arquivo_do_retrato(quem, retrato, not escrita), u(96), u(96))
        if figura is not None:
            graficos.desenhar_superficie(figura, x + u(4), y + u(4))
        margem = u(108)
        rotulo(nomes_das_vozes[quem], u(8), "titulo", x + margem, y + u(10))
    topo = y + (u(24) if quem is not None else u(28))
    desenhar_linhas(texto, letras, largura - margem - u(12), x + margem, topo, 255, 24)
    # a seta pisca quando a linha terminou de ser escrita
    if escrita and int(relogio_da_tela * 2.5) % 2 == 0:
        rotulo("ESPAÇO", u(8), "titulo", x + largura - u(10), y + altura - u(18), "direita")


def desenhar_aviso(fala, letras, opacidade):
    # a linha do rádio por cima do jogo: pequena, embaixo, sem travar nada
    if fala is None or opacidade <= 0:
        return
    quem, retrato, texto = fala
    alfa = int(255 * opacidade)
    largura = min(cfg.largura_tela - u(32), u(420))
    altura = u(46)
    x = (cfg.largura_tela - largura) // 2
    y = cfg.altura_tela - altura - u(12)
    caixa = graficos.moldura(largura, altura, u(1), cor_caixa, 215, cor_fio)
    graficos.desenhar_superficie(graficos.com_alfa(caixa, alfa), x, y)
    falando = letras < len(texto)
    # 32 divide os 192 do retrato: redução inteira, pixel nítido e sem franja
    figura = graficos.ajustada(arquivo_do_retrato(quem, retrato, falando), u(32), u(32))
    if figura is not None:
        graficos.desenhar_superficie(graficos.com_alfa(figura, alfa), x + u(8), y + u(7))
    desenhar_linhas(texto, letras, largura - u(58), x + u(48), y + u(6), alfa)


def gravado(conteudo, tamanho, papel, x, y, alinhar="esquerda", alfa=255):
    # letra gravada no latão: o brilho fica um pixel abaixo do sulco
    frente = graficos.texto(conteudo, tamanho, cor_sulco, papel)
    brilho = graficos.texto(conteudo, tamanho, cor_brilho, papel)
    if alinhar == "direita":
        x = x - frente.get_width()
    elif alinhar == "centro":
        x = x - frente.get_width() // 2
    graficos.desenhar_superficie(graficos.com_alfa(brilho, alfa), x + u(1), y + u(1))
    graficos.desenhar_superficie(graficos.com_alfa(frente, alfa), x, y)
    return frente.get_height()


def largura_gravada(conteudo, tamanho, papel, x, y):
    # grava e devolve a largura, para o que vem depois na mesma linha
    gravado(conteudo, tamanho, papel, x, y)
    return graficos.texto(conteudo, tamanho, cor_sulco, papel).get_width()


def desenhar_placa_lida(nome, ano, opacidade):
    # a placa do autor, grande, no alto da tela, enquanto a íris está diante
    # dela; a da cobertura está em branco
    if opacidade <= 0:
        return
    alfa = int(255 * opacidade)
    largura, altura = u(192), u(64)
    x = (cfg.largura_tela - largura) // 2
    y = u(10)
    chapa = graficos.ajustada("placa-leitura.png", largura, altura)
    if chapa is None:
        chapa = graficos.moldura(largura, altura, u(1), cor_fio, 255, cor_sulco)
    graficos.desenhar_superficie(graficos.com_alfa(chapa, alfa), x, y)
    if ano is None:
        return
    meio = cfg.largura_tela // 2
    partes = nome.upper().split(" ", 1)
    topo = y + u(9)
    for parte in partes:
        gravado(parte, u(16), "titulo", meio, topo, "centro", alfa)
        topo = topo + u(15)
    gravado(str(ano), u(16), "numero", meio, topo + u(2), "centro", alfa)


def desenhar_gravacao(fracao, titulo="GRAVANDO"):
    # o eco sendo gravado, ou repetindo: a fita que resta, no alto da tela
    largura = u(120)
    x = (cfg.largura_tela - largura) // 2
    rotulo(titulo, u(8), "titulo", cfg.largura_tela // 2, u(10), "centro")
    graficos.desenhar_superficie(graficos.moldura(largura, u(6), u(1), cor_caixa, 200, cor_fio), x, u(24))
    cheio = max(1, int((largura - u(4)) * (1 - fracao)))
    graficos.desenhar_superficie(graficos.translucido(cheio, u(2), cor_fio, 255), x + u(2), y_da_fita())


def y_da_fita():
    return u(26)


def desenhar_aviso_de_som(mudo, opacidade):
    # a resposta à tecla m, no alto da tela, por um instante
    texto = "SOM DESLIGADO" if mudo else "SOM LIGADO"
    rotulo(texto, u(8), "titulo", cfg.largura_tela // 2, u(12), "centro", int(255 * opacidade))


def preparar_falas():
    for nome in arquivos_de_retrato:
        graficos.imagem(nome)

