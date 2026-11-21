import os

# caminhos a partir do próprio arquivo, nunca do diretório de execução
base = os.path.dirname(os.path.abspath(__file__))
pasta_assets = os.path.join(base, "assets")

# blocos de cor de reserva: gerados em execução, fora do repositório
pasta_temporaria = os.path.join(base, "temporario")

# tela: 800 x 384 sem janela (testes e prévias); o main a ajusta à tela real
largura_tela = 800
altura_tela = 384
tela_cheia = True
tile = 32
titulo = "final stage"
quadros_por_segundo = 60

# mundo: todo andar tem 12 linhas de 32; os fundos têm 800 x 384
altura_mundo = 384
largura_fundo = 800

# pixels de tela por pixel de mundo e da interface. inteiros de propósito:
# escala fracionária deixa os pixels desiguais
escala_mundo = 2
escala_interface = 1
# a visão mostra cerca de tantos px de mundo na vertical: numa tela de 956
# de altura, escala 3 (490 x 319 px de mundo; um tile ocupa 96 px de tela)
altura_visao_alvo = 300

# fontes do gdd (seção 6.6), desenhadas sem suavização
pasta_fontes = os.path.join(pasta_assets, "fontes")
fontes = {"titulo": "silkscreen.ttf", "numero": "vt323.ttf"}

# som (gdd, seção 5): tudo em assets/sons, gravado pelo preparar-som.py.
# volumes de 0 a 100; a faixa ambiente fica atrás dos efeitos
pasta_sons = os.path.join(pasta_assets, "sons")
sons = ["passo-1", "passo-2", "pulo", "pouso", "botao-pressionado", "botao-solto", "alavanca",
        "porta-abrindo", "porta-fechando", "caixa", "caixa-caiu", "tique", "alerta", "detectada",
        "reinicio", "saida", "diamante", "foco", "clique", "radio-abre", "radio-fecha",
        "voz-selene", "voz-iris", "placa", "gravando", "gaveta-abrindo", "gaveta-fechando", "viga",
        "eco-grava", "eco-toca", "esteira", "lancada", "pista", "roda", "tranca-abre", "tranca-erro"]
musica = "ambiente.wav"
volume_efeitos = 85
volume_musica = 55

# progresso e recordes, fora do git: andar em curso, melhor tempo de cada
# andar e da corrida inteira
arquivo_progresso = os.path.join(base, "progresso.json")
# placar das noites inteiras, também fora do git (pontuacao.py)
arquivo_placar = os.path.join(base, "placar.json")

# falas: letras por segundo, e quanto a linha do rádio fica na tela depois
# de escrita (um tempo fixo mais um tanto por letra)
letras_por_segundo = 42
tempo_aviso = 2.2
tempo_aviso_por_letra = 0.035
# a voz toca a cada tantas letras
letras_por_voz = 3
# diante da placa do andar 6, depois disto a selene muda de assunto
espera_na_placa = 4.0
# largura de leitura da placa: a íris a menos disto do meio dela
alcance_placa = 28
# a cortina entre telas: clareia do escuro neste tempo
tempo_cortina = 0.5
# tremor da visão no flagrante da câmera: duração e força em px de mundo;
# a visão só tem um px de sobra, então a força não passa de 1
tempo_tremor = 0.3
forca_tremor = 1.0

# transição entre andares: escurece, mostra o andar (e o que o anterior
# rendeu), clareia
tempo_escurecer = 0.35
tempo_cartao = 1.5
tempo_clarear = 0.45
# quanto a placa lida soma, como aparece na hud (o valor é de pontuacao.py),
# por quanto tempo o aviso fica e em quanto a lição do treino troca
bonus_mostrado = 50
tempo_do_bonus = 2.0
tempo_da_licao = 0.25
# investigação (docs/andares.md, versão 7): a pista se lê com o meio do corpo
# a menos disto, em px, dos lados da célula dela; aberta, a tela só aceita
# tecla depois de um instante; a tranca certa fica um tempo na tela antes de
# fechar, e a errada treme por outro
folga_da_pista = 4
espera_do_modal = 0.05
tempo_do_acerto = 0.7
tempo_do_erro = 0.4
# no terceiro segredo errado da mesma tranca, a íris pensa alto uma dica
erros_para_a_dica = 3
# o que a hud avisa quando a pista entra no caderno
bonus_da_pista_mostrado = 25
# tinta que só a câmera acende: a cor fria do cone
cor_tinta = (217, 222, 234)
# o brilho da pista por ler pisca uma vez a cada tanto; a porta de passos
# fechada mostra, apagado, quantos passos ela dá
ciclo_do_brilho = 1.6
cor_passos_apagados = (116, 130, 166)
# vinheta nas bordas da tela, em alfa máximo
vinheta = 90

# teclas 1 a 9 (pular de andar) e P (salvar a tela) só funcionam com isto ligado
depuracao = False

# jogador
vel_jogador = 180
vel_pulo = 380
gravidade = 1000
# quadro mais longo que isto vale só isto: abaixo de 30 quadros por segundo
# o jogo desacelera, em vez de o pulo deixar de vencer dois tiles (a 20
# quadros por segundo ele subia 63 px)
dt_maximo = 1 / 30
# o pedido de pulo vale por este tempo: apertado um instante antes do pouso,
# o pulo sai ao pousar
memoria_do_pulo = 0.1
largura_jogador = 16
altura_jogador = 48

# mecanismos
folga_porta = 3.0
altura_porta = 64
altura_botao = 16
altura_botao_pressionado = 10
largura_alavanca = 16
altura_alavanca = 32
# 1 s contínuo no cone da câmera detecta; a cena da detecção dura 2 s
tempo_deteccao = 1.0
duracao_deteccao = 2.0
# depois disto, R encerra a cena da detecção e o andar recomeça já
espera_da_deteccao = 0.5
# a caixa tem peso: desliza mais devagar que a caminhada
vel_empurrao = 120

# gaveta de arquivo (andar 2): fica aberta este tempo e fecha sozinha,
# com quem estiver em cima; a tábua tem esta altura
tempo_gaveta = 3.0
altura_gaveta = 10
# viga de ferro (andar 3): velocidade com que corre de um lugar ao outro
vel_viga = 160
altura_viga = 16
# eco (andar 4): quanto tempo a íris grava, e depois o eco repete
tempo_eco = 6.0
# esteira (andar 5): velocidade da faixa; quem pula dela leva o embalo
vel_esteira = 240
# um passo da íris, em px andados no chão: as portas do andar 9 contam passos
passo_px = 54
# um pulo cobre 137 px: vale três passos ao pousar
passos_do_pulo = 3

# fundos escurecidos no carregamento, para os objetos se destacarem
escurecer_fundo = 0.82

# enquadramento: a visão mostra a tela dividida por escala_mundo
# zona morta pequena: parada, a íris fica a no máximo 8 px do centro
zona_morta_x = 16
zona_morta_y = 48
# a visão se adianta na direção da caminhada e volta ao centro com a íris parada;
# 32 compensa o atraso da suavização (180 / 8 = 22,5) e a meia zona morta (8)
antecipacao = 32
suavizacao_antecipacao = 3
# a visão segue como mola amortecida: tempo para alcançar o alvo, em
# segundos. na vertical é mais lenta, para o degrau não dar tranco
tempo_visao_x = 0.22
tempo_visao_y = 0.38
# caindo, a visão acompanha depressa: a íris não chega à borda de baixo
tempo_visao_queda = 0.14
# a íris nunca fica mais perto que isto da borda da visão, nem em queda longa
margem_visao = 16

# coluna decorativa na junta de dois fundos repetidos, bem atrás de tudo
escurecer_coluna = 0.5

# cores: só aparecem quando o png correspondente está faltando
cor_fundo = (30, 30, 30)
cores = {
    "parede": (80, 80, 80),
    "jogador": (140, 60, 200),
    "botao_solto": (220, 100, 30),
    "botao_pressionado": (50, 200, 80),
    "porta_fechada": (180, 40, 40),
    "porta_aberta": (100, 213, 147),
    "alavanca_desligada": (180, 50, 50),
    "alavanca_ligada": (50, 180, 50),
    "caixa": (160, 110, 60),
    "saida": (240, 220, 120),
}

# arte: arquivo e deslocamento de desenho (x, y) em relação ao objeto.
# y = altura da célula - base da figura, medido png por png
arte = {
    "caixa":              ("caixa.png", 0, 0),
    "porta_fechada":      ("porta-trancada.png", 0, 0),
    "porta_aberta":       ("porta-aberta.png", 0, 0),
    "saida":              ("saida.png", 0, 0),
    "botao_solto":        ("botao-solto.png", 0, 0),
    "botao_pressionado":  ("botao-pressionado.png", 0, 0),
    # alavanca desenhada em 32 de largura sobre o colisor de 16
    "alavanca_desligada": ("alavanca-desligada.png", -8, 0),
    "alavanca_ligada":    ("alavanca-ligada.png", -8, 1),
    # quadro do meio, mostrado por um instante na troca de estado
    "alavanca_meio":      ("alavanca-meio.png", -8, 0),
    "botao_meio":         ("botao-meio.png", 0, 0),
    # ícone centrado acima da porta, 2 px acima do batente
    "icone_botao":        ("icone-botao.png", 8, -14),
    "icone_alavanca":     ("icone-alavanca.png", 8, -14),
    "icone_relogio":      ("icone-relogio.png", 8, -14),
    "icone_codigo":       ("icone-codigo.png", 8, -14),
    # tranca de segredo, a luz da saída trancada e o brilho da pista por ler
    "tranca":             ("tranca.png", 0, 0),
    "tranca_aberta":      ("tranca-aberta.png", 0, 0),
    "saida_trancada":     ("saida-trancada.png", 0, 0),
    "parede_interna":     ("parede-interna.png", 0, 0),
    "laje":               ("laje.png", 0, 0),
    "divisoria":          ("divisoria.png", 0, 0),
    "laje_esquerda":      ("laje-esquerda.png", 0, 0),
    "laje_direita":       ("laje-direita.png", 0, 0),
    "divisoria_pe":       ("divisoria-pe.png", 0, 0),
    # câmera, diamante e a placa do autor do andar, na célula "p"
    "camera":             ("camera.png", 0, 0),
    "camera_alerta":      ("camera-alerta.png", 0, 0),
    "camera_desligada":   ("camera-desligada.png", 0, 0),
    "diamante":           ("diamante.png", 0, 0),
    "placa":              ("placa.png", 0, 8),
    # a tecla aparece sobre a alavanca até a primeira vez que a íris aciona uma
    "tecla_acionar":      ("tecla-e.png", -8, -52),
}

# câmera de segurança: png por estado; a arte olha para a direita
arte_camera = {
    "vigiando": "camera.png",
    "alerta": "camera-alerta.png",
    "desligada": "camera-desligada.png",
}
# o cone sai da lente (posição no png, que olha para a direita) e desce para
# o chão: inclinação do eixo e abertura, em graus; o andar pode trocar as
# duas por câmera. raios é em quantas fatias o cone é traçado
lente_camera = (29, 12)
inclinacao_camera = 24
abertura_camera = 36
raios_do_cone = 36
# cone: vigiando, varre em branco frio; no alerta fica vermelho inteiro desde
# o primeiro quadro, e a contagem o enche de magenta a partir da câmera.
# clareia em faixas, da lente (alfa cheio) ao fim do alcance
cor_cone = {"vigiando": ((217, 222, 234), 76), "alerta": ((216, 58, 58), 116)}
cor_alerta = ((181, 23, 158), 150)
alfa_fim_do_cone = 0.3
faixas_do_cone = 5
# a contagem enche o cone em tantos degraus (um desenho guardado por degrau)
degraus_do_alerta = 16
# marca de tempo acima das portas: um quadrado magenta por segundo
cor_marca = (181, 23, 158)
lado_marca = 3
# marca de canal: forma 8 x 8 px de mundo acima dos controles e ao lado do
# ícone da porta. dourado, nunca cor de estado (vermelho, verde, magenta)
formas_de_marca = ("circulo", "triangulo", "quadrado", "losango", "cruz")
cor_marca_canal = (232, 176, 74)
contorno_marca_canal = (14, 11, 22)
lado_marca_canal = 8
# risco claro sobre a marca da porta invertida
cor_risco = (217, 222, 234)
# contador da porta de canal "todos": um pino por controle do canal, acima
# do ícone; aceso em verde (cor de estado) quando o controle já vale
lado_pino = 4
cor_pino_aceso = (69, 196, 106)
cor_pino_apagado = (82, 91, 130)
contorno_pino = (14, 11, 22)
# halo quente em volta do que se pode tocar (a cor é a interface): raio em
# px de mundo e alfa no centro; o do diamante pulsa
cor_halo = (255, 224, 138)
raio_halo = 22
alfa_halo = 26
raio_halo_diamante = 40
alfa_halo_diamante = 60
# sombra que o maciço no ar faz na parede logo abaixo dele: faixas de 2 px,
# da mais forte para a mais fraca, em alfa
cor_sombra_da_peca = (14, 11, 22)
sombra_da_peca = (120, 80, 44)
# uma em cada tantas células de um maciço leva o detalhe raro do tema
raridade_do_detalhe = 5
# poeira parada no ar, onde há teto: quantos grãos por andar e a cor fria
graos_no_ar = 26
cor_grao = (163, 174, 200)
# brilho do diamante, em relação ao canto do png
brilho_diamante = (8, 10)

# cenário do autor (preparar-mobilia.py): o móvel de pé pode passar tantos px
# da linha do chão (os da versão 8 pousam nela), e escurece como o fundo
pe_do_cenario = 0
# relógio do quaresma: centro e raio do mostrador dentro do png; os
# ponteiros e as marcas das horas são desenhados pelo jogo, na hora certa
centro_do_relogio = (28, 28)
raio_do_relogio = 19
cor_ponteiro = (27, 24, 48)
cor_segundos = (82, 91, 130)
# monitores da cássia: canto do vidro de cada um dentro do png, de cima para
# baixo, e o tamanho do vidro. o quarto, sem câmera, é o da estática
telas_dos_monitores = ((14, 7), (14, 33), (14, 59), (14, 85), (14, 111), (14, 137))
tamanho_da_tela = (24, 14)
tela_de_estatica = 3
# diante dos monitores, E mostra o que cada câmera do andar vê: a visão fica
# este tempo em cada uma
tempo_de_olhar = 1.8
# lousa do aníbal: o canto e o tamanho da área de giz dentro do png
area_da_lousa = (5, 5, 54, 32)
cor_giz = (217, 222, 234)
cor_giz_apagado = (82, 91, 130)

# reserva: largura, altura, cor e deslocamento do bloco que substitui o png
reserva = {
    "caixa":              (tile, tile, cores["caixa"], 0),
    "porta_fechada":      (tile, altura_porta, cores["porta_fechada"], 0),
    "porta_aberta":       (tile, altura_porta, cores["porta_aberta"], 0),
    "botao_solto":        (tile, altura_botao, cores["botao_solto"], 0),
    "botao_pressionado":  (tile, altura_botao_pressionado,
                           cores["botao_pressionado"],
                           altura_botao - altura_botao_pressionado),
    "alavanca_desligada": (largura_alavanca, altura_alavanca,
                           cores["alavanca_desligada"], 0),
    "alavanca_ligada":    (largura_alavanca, altura_alavanca,
                           cores["alavanca_ligada"], 0),
    "saida":              (tile, altura_porta, cores["saida"], 0),
    "botao_meio":         (tile, altura_botao, cores["botao_solto"], 0),
    "alavanca_meio":      (largura_alavanca, altura_alavanca,
                           cores["alavanca_desligada"], 0),
    "parede_interna":     (tile, tile, cores["parede"], 0),
    "laje":               (tile, tile, cores["parede"], 0),
    "divisoria":          (tile, tile, cores["parede"], 0),
    "laje_esquerda":      (tile, tile, cores["parede"], 0),
    "laje_direita":       (tile, tile, cores["parede"], 0),
    "divisoria_pe":       (tile, tile, cores["parede"], 0),
    "jogador":            (largura_jogador, altura_jogador, cores["jogador"], 0),
}

# íris: quadro de 64 com o colisor centrado e os pés na última linha
quadro_iris = 64
recuo_iris_x = (quadro_iris - largura_jogador) // 2   # 24
recuo_iris_y = quadro_iris - altura_jogador           # 16

# animações: arquivo, quadros, duração do ciclo em segundos e se repete
animacoes = {
    "parada":     ("iris-parada.png", 4, 0.8, True),
    "andando":    ("iris-andando.png", 6, 0.6, True),
    "empurrando": ("iris-empurrando.png", 6, 0.9, True),
    "pulando":    ("iris-pulando.png", 1, 1.0, False),
    "caindo":     ("iris-caindo.png", 1, 1.0, False),
    "acionando":  ("iris-acionando.png", 3, 0.3, False),
    # a preparação aparece no começo da subida: o pulo não espera por ela
    "preparando":   ("iris-preparando.png", 1, 0.05, False),
    "aterrissando": ("iris-aterrissando.png", 2, 0.16, False),
    # tocada uma vez no flagrante da câmera
    "detectada":    ("iris-detectada.png", 3, 0.9, False),
}

# efeitos em tira: arquivo, quadros e duração em segundos, tocados uma vez
efeitos = {
    "porta_abrindo": ("porta-abrindo.png", 3, 0.24),
    "poeira_passo":  ("poeira-passo.png", 4, 0.32),
    "poeira_caixa":  ("poeira-caixa.png", 4, 0.32),
    # caixa arrastada por cima de outra: atrito na junta, sem nuvem de chão
    "raspao_caixa":  ("raspao-caixa.png", 4, 0.32),
    # entra com o diamante do andar 10
    "brilho":        ("brilho-diamante.png", 4, 0.8),
    # pisca sobre a pista que a íris ainda não leu
    "brilho_pista":  ("brilho-pista.png", 4, 0.6),
}

# alavanca e botão mostram o quadro do meio por este tempo ao trocar de estado
tempo_meio = 0.08

# quadros da caminhada em que o pé toca o chão: levantam poeira
passos_andando = (0, 3)

# cursor do mouse: arquivo e ponta (x, y) dentro do png de 16
cursores = {
    "seta": ("cursor-seta.png", 0, 0),
    "mao":  ("cursor-mao.png", 3, 0),
}

# o empurrão move a caixa um tile de uma vez: a pose segura esse tempo
# para não piscar entre andando e empurrando
folga_empurrao = 0.2


def ajustar_tela(largura, altura):
    # tela real: a escala do mundo mostra cerca de altura_visao_alvo px de
    # mundo; a da interface mantém os menus do tamanho pensado para 384
    global largura_tela, altura_tela, escala_mundo, escala_interface
    largura_tela, altura_tela = largura, altura
    escala_mundo = max(2, round(altura / altura_visao_alvo))
    escala_interface = max(1, altura // altura_mundo)


def colidiu(ax, ay, al, aa, bx, by, bl, ba):
    if ax >= bx + bl or ax + al <= bx:
        return False
    if ay >= by + ba or ay + aa <= by:
        return False
    return True
