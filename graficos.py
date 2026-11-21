import math
import os
import pygame
from PPlay.sprite import Sprite
from PPlay.window import Window
import configuracoes as cfg
import enquadramento

# um bloco por tamanho e cor, só criado quando falta o png; vai para
# temporario/, nunca para assets/
cache = {}

# sprites vindos de png; None quando o arquivo não existe
cache_arte = {}

# tiras de animação: leste e oeste, espelhadas uma vez só
cache_tiras = {}

# fundos escurecidos, por nome e fator
cache_escurecidas = {}

# pngs virados para a esquerda e retângulos translúcidos prontos
cache_espelhadas = {}
cache_translucidos = {}

# arte da interface na escala inteira, fontes, vinheta e a tela ampliada
cache_interface = {}
cache_fontes = {}
cache_tela = {}

# textos e véus prontos: fonte e superfície não se refazem a cada quadro
cache_textos = {}
cache_veus = {}


def bloco(largura, altura, cor):
    chave = (largura, altura, cor)
    if chave in cache:
        return cache[chave]

    if not os.path.isdir(cfg.pasta_temporaria):
        os.makedirs(cfg.pasta_temporaria)

    caminho = os.path.join(cfg.pasta_temporaria, "bloco-%d-%d-%d-%d-%d.bmp" % (
        largura, altura, cor[0], cor[1], cor[2]))

    if not os.path.exists(caminho):
        if not pygame.display.get_init():
            pygame.display.init()
        superficie = pygame.Surface((largura, altura))
        superficie.fill(cor)
        pygame.image.save(superficie, caminho)

    cache[chave] = Sprite(caminho)
    return cache[chave]


def imagem(nome):
    # só depois da janela: convert_alpha precisa de modo de vídeo ativo
    if nome in cache_arte:
        return cache_arte[nome]

    caminho = os.path.join(cfg.pasta_assets, nome)
    if os.path.exists(caminho):
        cache_arte[nome] = Sprite(caminho)
    else:
        cache_arte[nome] = None
    return cache_arte[nome]


def atlas(nome, lado):
    # folha de peças cortada uma vez em quadrados de lado x lado: uma lista
    # por linha da folha. None quando o png não existe
    chave = ("atlas", nome, lado)
    if chave not in cache_arte:
        folha = imagem(nome)
        if folha is None:
            cache_arte[chave] = None
        else:
            colunas, linhas = folha.image.get_width() // lado, folha.image.get_height() // lado
            cache_arte[chave] = [[folha.image.subsurface((c * lado, l * lado, lado, lado)) for c in range(colunas)]
                                 for l in range(linhas)]
    return cache_arte[chave]


def escurecida(nome, fator):
    # cópia escurecida de um png, feita uma vez; None quando o arquivo não existe
    chave = (nome, fator)
    if chave in cache_escurecidas:
        return cache_escurecidas[chave]

    caminho = os.path.join(cfg.pasta_assets, nome)
    if not os.path.exists(caminho):
        cache_escurecidas[chave] = None
        return None
    sprite = Sprite(caminho)
    # cópia, como na tira: a pplay guarda a superfície original num cache
    sprite.image = sprite.image.copy()
    nivel = round(255 * fator)
    sprite.image.fill((nivel, nivel, nivel), special_flags=pygame.BLEND_RGB_MULT)
    cache_escurecidas[chave] = sprite
    return sprite


def escurecida_espelhada(nome, fator):
    # o fundo escurecido, virado: lado a lado com o original, a emenda some
    chave = (nome, fator, "espelhada")
    if chave not in cache_escurecidas:
        original = escurecida(nome, fator)
        if original is None:
            cache_escurecidas[chave] = None
        else:
            copia = Sprite(os.path.join(cfg.pasta_assets, nome))
            copia.image = pygame.transform.flip(original.image, True, False)
            cache_escurecidas[chave] = copia
    return cache_escurecidas[chave]


def espelhada(nome):
    # cópia virada na horizontal, feita uma vez; None quando o arquivo não existe
    if nome in cache_espelhadas:
        return cache_espelhadas[nome]
    caminho = os.path.join(cfg.pasta_assets, nome)
    if not os.path.exists(caminho):
        cache_espelhadas[nome] = None
        return None
    sprite = Sprite(caminho)
    sprite.image = pygame.transform.flip(sprite.image, True, False)
    cache_espelhadas[nome] = sprite
    return sprite


def leque(raios, alcance, cor, alfa, cheio=None):
    # o cone da câmera: polígono que sai da lente e vai até onde cada raio
    # chega (dx, dy, distância), em faixas que clareiam para longe, com borda
    # de luz. com cheio, só até essa distância e de uma cor só: a contagem.
    # devolve a superfície e o ponto dela em que fica a lente
    chave = ("leque", raios, alcance, cor, alfa, cheio)
    if chave not in cache_translucidos:
        def ate(corte):
            return [(dx * min(d, corte), dy * min(d, corte)) for dx, dy, d in raios]
        borda = ate(alcance)
        ox = 1 - math.floor(min([x for x, _ in borda] + [0]))
        oy = 1 - math.floor(min([y for _, y in borda] + [0]))
        largura = math.ceil(max([x for x, _ in borda] + [0])) + ox + 2
        altura = math.ceil(max([y for _, y in borda] + [0])) + oy + 2
        superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)

        def pintar(pontos, tinta):
            pygame.draw.polygon(superficie, tinta, [(ox, oy)] + [(ox + x, oy + y) for x, y in pontos])
        if cheio is not None:
            pintar(ate(cheio), cor + (alfa,))
        else:
            faixas = cfg.faixas_do_cone
            for n in range(faixas):
                forca = cfg.alfa_fim_do_cone + (1 - cfg.alfa_fim_do_cone) * n / (faixas - 1)
                pintar(ate(alcance * (faixas - n) / faixas), cor + (int(alfa * forca),))
            contorno = [(ox, oy)] + [(ox + x, oy + y) for x, y in borda]
            pygame.draw.lines(superficie, cor + (min(255, int(alfa * 1.5)),), True, contorno, 1)
        cache_translucidos[chave] = (superficie, ox, oy)
    return cache_translucidos[chave]


def halo(raio, cor, alfa):
    # luz redonda que morre para a borda, em degraus: o brilho quente de tudo
    # o que a íris pode tocar. um por raio, cor e alfa
    chave = ("halo", raio, cor, alfa)
    if chave not in cache_translucidos:
        superficie = pygame.Surface((2 * raio, 2 * raio), pygame.SRCALPHA)
        for y in range(2 * raio):
            for x in range(2 * raio):
                d = math.hypot(x - raio + 0.5, y - raio + 0.5) / raio
                if d < 1:
                    # quatro degraus: degradê liso não combina com pixel art
                    forca = math.ceil((1 - d) ** 1.6 * 4) / 4
                    superficie.set_at((x, y), cor + (int(alfa * forca),))
        cache_translucidos[chave] = superficie
    return cache_translucidos[chave]


def sombra_no_chao(largura):
    # elipse escura sob os pés: prende a figura ao chão
    chave = ("sombra", largura)
    if chave not in cache_translucidos:
        superficie = pygame.Surface((largura, 4), pygame.SRCALPHA)
        pygame.draw.ellipse(superficie, (8, 6, 16, 110), (0, 0, largura, 4))
        cache_translucidos[chave] = superficie
    return cache_translucidos[chave]


def translucido(largura, altura, cor, alfa):
    # retângulo de cor com transparência, um por tamanho, cor e alfa
    chave = (largura, altura, cor, alfa)
    if chave not in cache_translucidos:
        superficie = pygame.Surface((largura, altura))
        superficie.fill(cor)
        superficie.set_alpha(alfa)
        cache_translucidos[chave] = superficie
    return cache_translucidos[chave]


# marcas de canal, pixel a pixel: o contorno, x preenchimento
desenhos_de_marca = {
    "circulo": ["..oooo..", ".oxxxxo.", "oxxxxxxo", "oxxxxxxo",
                "oxxxxxxo", "oxxxxxxo", ".oxxxxo.", "..oooo.."],
    "triangulo": ["...oo...", "..oxxo..", "..oxxo..", ".oxxxxo.",
                  ".oxxxxo.", "oxxxxxxo", "oxxxxxxo", "oooooooo"],
    "quadrado": ["oooooooo", "oxxxxxxo", "oxxxxxxo", "oxxxxxxo",
                 "oxxxxxxo", "oxxxxxxo", "oxxxxxxo", "oooooooo"],
    "losango": ["...oo...", "..oxxo..", ".oxxxxo.", "oxxxxxxo",
                "oxxxxxxo", ".oxxxxo.", "..oxxo..", "...oo..."],
    "cruz": ["..oooo..", "..oxxo..", "ooxxxxoo", "oxxxxxxo",
             "oxxxxxxo", "ooxxxxoo", "..oxxo..", "..oooo.."],
}
cache_marcas = {}


def marca_de_canal(forma):
    # desenhada por código, uma vez por forma
    if forma not in cache_marcas:
        lado = cfg.lado_marca_canal
        superficie = pygame.Surface((lado, lado), pygame.SRCALPHA)
        cores = {"o": cfg.contorno_marca_canal, "x": cfg.cor_marca_canal}
        for y, linha in enumerate(desenhos_de_marca[forma]):
            for x, letra in enumerate(linha):
                if letra in cores:
                    superficie.set_at((x, y), cores[letra])
        cache_marcas[forma] = superficie
    return cache_marcas[forma]


# o risco que cruza a marca da porta invertida: ela funciona ao contrário
desenho_do_risco = ["......oo", ".....oxo", "....oxo.", "...oxo..", "..oxo...", ".oxo....", "oxo.....", "oo......"]


def risco_de_invertida():
    if "risco" not in cache_marcas:
        superficie = pygame.Surface((8, 8), pygame.SRCALPHA)
        cores = {"o": cfg.contorno_marca_canal, "x": cfg.cor_risco}
        for y, linha in enumerate(desenho_do_risco):
            for x, letra in enumerate(linha):
                if letra in cores:
                    superficie.set_at((x, y), cores[letra])
        cache_marcas["risco"] = superficie
    return cache_marcas["risco"]


# figuras das telas dos monitores, ponto a ponto (o vidro tem 24 x 14)
desenho_do_cone = ["oo......", "oooo....", "oooooo..", "oooooooo", ".ooooooo", "..oooooo", "...ooooo"]
desenho_da_pessoa = [".oo.", ".oo.", "oooo", "oooo", ".oo.", ".oo.", "o..o", "o..o"]


def carimbar(superficie, desenho, x, y, cor):
    for dy, linha in enumerate(desenho):
        for dx, letra in enumerate(linha):
            if letra == "o":
                superficie.set_at((x + dx, y + dy), cor)


def tela_de_monitor(estado, numero, quadro):
    # o vidro de um monitor do andar da cássia: o que a câmera daquele número
    # está fazendo. vigiando, o cone frio; em alerta, a pessoa em vermelho,
    # piscando; desligada (ou sem câmera), estática. um por estado e quadro
    chave = ("monitor", estado, numero, quadro)
    if chave not in cache_translucidos:
        largura, altura = cfg.tamanho_da_tela
        superficie = pygame.Surface((largura, altura))
        if estado == "estatica":
            tons = ((82, 91, 130), (116, 130, 166), (163, 174, 200), (217, 222, 234))
            for y in range(altura):
                for x in range(largura):
                    superficie.set_at((x, y), tons[(x * 37 + y * 101 + quadro * 53 + x * y * (quadro + 3)) % 7 % 4])
        elif estado == "alerta":
            superficie.fill((216, 58, 58) if quadro % 2 == 0 else (122, 30, 38))
            carimbar(superficie, desenho_da_pessoa, 10, 3, (244, 241, 234))
        else:
            superficie.fill((31, 36, 64))
            carimbar(superficie, desenho_do_cone, 8, 4, (116, 130, 166))
            # a linha de varredura desce pelo vidro
            pygame.draw.line(superficie, (47, 55, 97), (0, quadro % altura), (largura - 1, quadro % altura))
        # um ponto dourado por número: qual câmera é esta
        for n in range(numero):
            superficie.set_at((2 + 2 * n, 2), cfg.cor_marca_canal)
        cache_translucidos[chave] = superficie
    return cache_translucidos[chave]


def tira(nome, quadros):
    # o espelho sai de uma cópia: a pplay guarda a superfície original
    # num cache por caminho, e a leste não pode virar
    if nome in cache_tiras:
        return cache_tiras[nome]

    caminho = os.path.join(cfg.pasta_assets, nome)
    if not os.path.exists(caminho):
        cache_tiras[nome] = None
        return None
    leste = Sprite(caminho, quadros)
    oeste = Sprite(caminho, quadros)
    oeste.image = pygame.transform.flip(leste.image, True, False)
    cache_tiras[nome] = {"leste": leste, "oeste": oeste}
    return cache_tiras[nome]


cache_fantasmas = {}


def tira_do_eco(nome, quadros):
    # a tira da íris em azul translúcido: o eco é ela, mas não está ali
    if nome not in cache_fantasmas:
        par = tira(nome, quadros)
        if par is None:
            cache_fantasmas[nome] = None
        else:
            copias = {}
            for lado_dela in ("leste", "oeste"):
                copia = Sprite(os.path.join(cfg.pasta_assets, nome), quadros)
                copia.image = par[lado_dela].image.copy()
                copia.image.fill((150, 200, 255, 130), special_flags=pygame.BLEND_RGBA_MULT)
                copias[lado_dela] = copia
            cache_fantasmas[nome] = copias
    return cache_fantasmas[nome]


def carregar(nomes):
    # tudo de uma vez, logo depois da janela, para não engasgar no laço
    for nome in nomes:
        imagem(nome)


def carregar_escurecidas(nomes, fator):
    for nome in nomes:
        escurecida(nome, fator)


def carregar_tiras(animacoes):
    # serve às animações da íris e aos efeitos: arquivo e quadros vêm primeiro
    for valores in animacoes.values():
        tira(valores[0], valores[1])


def esconder_cursor():
    # o jogo desenha o próprio cursor
    pygame.mouse.set_visible(False)


def faltando():
    # o que ainda está sendo desenhado como bloco de cor
    ausentes = [nome for nome, sprite in cache_arte.items() if sprite is None]
    return ausentes + [nome for nome, par in cache_tiras.items() if par is None]


def desenhar(sprite, x, y):
    sprite.x = x
    sprite.y = y
    sprite.draw()


def desenhar_quadro(sprite, quadro, x, y):
    sprite.set_curr_frame(quadro)
    desenhar(sprite, x, y)


def no_mundo(sprite, x, y):
    # posição arredondada como a da câmera: a pplay truncaria, e o objeto
    # tremeria um pixel em relação ao fundo. fora da visão, não desenha
    x, y = round(x), round(y)
    if enquadramento.visivel(x, y, sprite.width, sprite.height):
        ox, oy = enquadramento.deslocamento()
        desenhar(sprite, x - ox, y - oy)


def superficie_no_mundo(superficie, x, y):
    x, y = round(x), round(y)
    if enquadramento.visivel(x, y, superficie.get_width(), superficie.get_height()):
        ox, oy = enquadramento.deslocamento()
        desenhar_superficie(superficie, x - ox, y - oy)


def quadro_no_mundo(sprite, quadro, x, y):
    x, y = round(x), round(y)
    if enquadramento.visivel(x, y, sprite.width, sprite.height):
        ox, oy = enquadramento.deslocamento()
        desenhar_quadro(sprite, quadro, x - ox, y - oy)


def retangulo_no_mundo(cor, x, y, largura, altura):
    # um retângulo cheio, direto na tela, em coordenadas de mundo
    if enquadramento.visivel(x, y, largura, altura):
        ox, oy = enquadramento.deslocamento()
        pygame.draw.rect(Window.get_screen(), cor, (round(x) - ox, round(y) - oy, largura, altura))


def linha_no_mundo(cor, x0, y0, x1, y1):
    ox, oy = enquadramento.deslocamento()
    pygame.draw.line(Window.get_screen(), cor, (round(x0) - ox, round(y0) - oy), (round(x1) - ox, round(y1) - oy))


def fonte(papel, tamanho):
    # "titulo" é a silkscreen, "numero" a vt323; sem o arquivo, a do sistema
    chave = (papel, tamanho)
    if chave not in cache_fontes:
        caminho = os.path.join(cfg.pasta_fontes, cfg.fontes[papel])
        if os.path.exists(caminho):
            cache_fontes[chave] = pygame.font.Font(caminho, tamanho)
        else:
            cache_fontes[chave] = pygame.font.SysFont("Arial", tamanho, bold=True)
    return cache_fontes[chave]


def texto(conteudo, tamanho, cor, papel="titulo"):
    # sem suavização, como pede o gdd: a borda do pixel fica nítida
    chave = (conteudo, tamanho, cor, papel)
    if chave not in cache_textos:
        cache_textos[chave] = fonte(papel, tamanho).render(conteudo, False, cor)
    return cache_textos[chave]


def veu(alfa):
    # retângulo escuro translúcido do tamanho da tela. uma superfície só, com
    # o alfa do momento: uma por alfa enchia a memória (centenas de mb)
    chave = (cfg.largura_tela, cfg.altura_tela)
    if chave not in cache_veus:
        superficie = pygame.Surface((cfg.largura_tela, cfg.altura_tela))
        superficie.fill((14, 11, 22))
        cache_veus[chave] = superficie
    cache_veus[chave].set_alpha(alfa)
    return cache_veus[chave]


def interface(nome):
    # png da interface ampliado pela escala inteira, feito uma vez
    chave = (nome, cfg.escala_interface)
    if chave not in cache_interface:
        sprite = imagem(nome)
        if sprite is None:
            cache_interface[chave] = None
        else:
            largura, altura = sprite.image.get_size()
            cache_interface[chave] = pygame.transform.scale(
                sprite.image, (largura * cfg.escala_interface, altura * cfg.escala_interface))
    return cache_interface[chave]


def ajustada(nome, largura, altura):
    # png em outro tamanho, feito uma vez: ampliação inteira fica nítida;
    # redução é suavizada para não perder linha
    chave = ("ajustada", nome, largura, altura)
    if chave not in cache_interface:
        sprite = imagem(nome)
        if sprite is None:
            cache_interface[chave] = None
        elif largura % sprite.image.get_width() == 0:
            cache_interface[chave] = pygame.transform.scale(sprite.image, (largura, altura))
        else:
            # pixel transparente guarda a cor do fundo de origem (magenta), e a
            # suavização a puxaria para a borda: a cópia limpa essa cor antes
            limpa = pygame.Surface(sprite.image.get_size(), pygame.SRCALPHA)
            limpa.fill((14, 11, 22, 0))
            limpa.blit(sprite.image, (0, 0))
            cache_interface[chave] = pygame.transform.smoothscale(limpa, (largura, altura))
    return cache_interface[chave]


def ajustada_superficie(superficie, escala):
    # uma superfície feita por código, ampliada por inteiro; uma por escala
    chave = ("ampliada", id(superficie), escala)
    if chave not in cache_interface:
        tamanho = (superficie.get_width() * escala, superficie.get_height() * escala)
        cache_interface[chave] = pygame.transform.scale(superficie, tamanho)
    return cache_interface[chave]


def moldura(largura, altura, borda, cor_fundo, alfa, cor_borda):
    # caixa escura translúcida com fio na borda: falas e avisos do rádio
    chave = ("moldura", largura, altura, borda, cor_fundo, alfa, cor_borda)
    if chave not in cache_translucidos:
        superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
        superficie.fill(cor_fundo + (alfa,))
        pygame.draw.rect(superficie, cor_borda + (255,), (0, 0, largura, altura), borda)
        cache_translucidos[chave] = superficie
    return cache_translucidos[chave]


def quebrar(conteudo, tamanho, papel, largura):
    # o texto em linhas que cabem na largura, quebrado nos espaços; guardado
    chave = ("linhas", conteudo, tamanho, papel, largura)
    if chave not in cache_textos:
        letra = fonte(papel, tamanho)
        linhas, atual = [], ""
        for palavra in conteudo.split(" "):
            tentativa = palavra if atual == "" else atual + " " + palavra
            if atual != "" and letra.size(tentativa)[0] > largura:
                linhas.append(atual)
                atual = palavra
            else:
                atual = tentativa
        cache_textos[chave] = linhas + [atual]
    return cache_textos[chave]


def com_alfa(superficie, alfa):
    # a mesma superfície, com a opacidade do momento
    superficie.set_alpha(alfa)
    return superficie


def cobrindo_nitida(nome, ancora=0.5):
    # pintura que cobre a tela em ampliação inteira, sem suavizar: o pixel
    # fica do tamanho certo, como no jogo. a âncora diz que parte da largura
    # fica no meio quando sobra imagem dos lados
    chave = ("nitida", nome, cfg.largura_tela, cfg.altura_tela, ancora)
    if chave not in cache_interface:
        sprite = imagem(nome)
        if sprite is None:
            cache_interface[chave] = None
        else:
            largura, altura = sprite.image.get_size()
            fator = math.ceil(max(cfg.largura_tela / largura, cfg.altura_tela / altura))
            grande = pygame.transform.scale(sprite.image.convert(), (largura * fator, altura * fator))
            x = int((largura * fator - cfg.largura_tela) * ancora)
            y = (altura * fator - cfg.altura_tela) // 2
            cache_interface[chave] = grande.subsurface((x, y, cfg.largura_tela, cfg.altura_tela)).copy()
    return cache_interface[chave]


def desenhar_nitida(nome, ancora=0.5):
    pintura = cobrindo_nitida(nome, ancora)
    if pintura is not None:
        desenhar_superficie(pintura, 0, 0)
    return pintura is not None


def tracar(pontos, cor, espessura, dx=0, dy=0):
    # um traço da assinatura, direto na tela
    if len(pontos) > 1:
        pygame.draw.lines(Window.get_screen(), cor, False, [(x + dx, y + dy) for x, y in pontos], espessura)


def cobrindo(nome):
    # pintura que cobre a tela inteira, centrada; suavizada, porque é pintura
    chave = ("cobrindo", nome, cfg.largura_tela, cfg.altura_tela)
    if chave not in cache_interface:
        sprite = imagem(nome)
        if sprite is None:
            cache_interface[chave] = None
        else:
            largura, altura = sprite.image.get_size()
            fator = max(cfg.largura_tela / largura, cfg.altura_tela / altura)
            tamanho = (math.ceil(largura * fator), math.ceil(altura * fator))
            cache_interface[chave] = pygame.transform.smoothscale(sprite.image.convert(), tamanho)
    return cache_interface[chave]


def desenhar_cobrindo(nome):
    pintura = cobrindo(nome)
    if pintura is not None:
        desenhar_superficie(pintura, (cfg.largura_tela - pintura.get_width()) // 2,
                            (cfg.altura_tela - pintura.get_height()) // 2)
    return pintura is not None


def vinheta():
    # bordas escurecidas, como luz de ambiente; feita pequena e ampliada suave
    chave = ("vinheta", cfg.largura_tela, cfg.altura_tela)
    if chave not in cache_tela:
        pequena = pygame.Surface((64, 40), pygame.SRCALPHA)
        for y in range(40):
            for x in range(64):
                d = math.hypot((x - 31.5) / 32, (y - 19.5) / 20)
                alfa = int(cfg.vinheta * max(0.0, min(1.0, (d - 0.55) / 0.6)) ** 1.6)
                pequena.set_at((x, y), (8, 6, 16, alfa))
        cache_tela[chave] = pygame.transform.smoothscale(pequena, (cfg.largura_tela, cfg.altura_tela))
    return cache_tela[chave]


def desenhar_superficie(superficie, x, y):
    Window.get_screen().blit(superficie, (x, y))


def desenhar_recortado(superficie, x, y, area):
    # só o que cai dentro da área (x, y, largura, altura) da tela
    tela = Window.get_screen()
    tela.set_clip(area)
    tela.blit(superficie, (x, y))
    tela.set_clip(None)


def faixa_de_brilho(largura, altura):
    # o reflexo que corre a placa de latão: faixa clara, inclinada
    chave = ("brilho", largura, altura)
    if chave not in cache_translucidos:
        superficie = pygame.Surface((largura + altura // 2, altura), pygame.SRCALPHA)
        pontos = [(altura // 2, 0), (altura // 2 + largura, 0), (largura, altura), (0, altura)]
        pygame.draw.polygon(superficie, (255, 244, 200, 90), pontos)
        miolo = [(altura // 2 + largura // 3, 0), (altura // 2 + 2 * largura // 3, 0),
                 (2 * largura // 3, altura), (largura // 3, altura)]
        pygame.draw.polygon(superficie, (255, 250, 225, 150), miolo)
        cache_translucidos[chave] = superficie
    return cache_translucidos[chave]


def aurora(nivel):
    # o céu clareando atrás dos créditos: faixa quente que sobe do horizonte,
    # mais forte a cada nível (de 0 a 12). uma superfície por nível
    chave = ("aurora", nivel, cfg.largura_tela, cfg.altura_tela)
    if chave not in cache_tela:
        pequena = pygame.Surface((1, 48), pygame.SRCALPHA)
        for y in range(48):
            forca = (y / 47) ** 1.8
            pequena.set_at((0, y), (232, 150, 86, int(13 * nivel * forca)))
        cache_tela[chave] = pygame.transform.smoothscale(pequena, (cfg.largura_tela, int(cfg.altura_tela * 0.5)))
    return cache_tela[chave]


def ampliar_visao(fracao):
    # o mundo desenhado no canto da tela, um pixel a mais em cada eixo, vira a
    # tela inteira: ampliação inteira sem suavizar, e a fração da câmera vira
    # deslocamento em pixels de tela, para a rolagem andar suave
    tela = Window.get_screen()
    escala = cfg.escala_mundo
    largura = min(math.ceil(cfg.largura_tela / escala) + 1, cfg.largura_tela)
    altura = min(math.ceil(cfg.altura_tela / escala) + 1, cfg.altura_tela)
    chave = ("ampliada", largura, altura, escala)
    if chave not in cache_tela:
        cache_tela[chave] = pygame.Surface((largura * escala, altura * escala))
    ampliada = cache_tela[chave]
    pygame.transform.scale(tela.subsurface((0, 0, largura, altura)), (largura * escala, altura * escala), ampliada)
    tela.blit(ampliada, (-round(fracao[0] * escala), -round(fracao[1] * escala)))


def capturar(caminho):
    # salva a tela como está, para a entrega ao professor
    pygame.image.save(pygame.display.get_surface(), caminho)
