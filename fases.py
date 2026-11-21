import configuracoes as cfg
import documentos

# cada andar: 12 linhas de texto, um caractere por célula (docs/andares.md, seção 1)
#   .  vazio          #  parede         c  caixa          b  botão
#   B  porta de botão a  alavanca       A  porta de alavanca
#   r  porta de relógio                 v  câmera de segurança
#   i  início         s  saída          d  diamante       p  lugar da placa
# porta, saída e diamante ocupam duas células empilhadas, com a mesma letra.
# detalhes, por (linha, coluna), guardam o que a letra não carrega; para as
# duplas, vale a célula de cima. regras: canal -> "todos". opcionais:
# memorias: canal "todos" -> segundos que o botão solto ainda vale (0 sem)
# porta: "aberta" começa aberta; "caixa" põe uma caixa parada no vão
# marcas: canal -> forma da marca desenhada nos controles e nas portas
# porta de alavanca com "canais" (lista): abre com número ímpar deles ligado,
# a correção que desfaz a correção (andares 3 e 5)
# g  gaveta de arquivo: aberta com E, vira tábua e fecha sozinha
# V  viga de ferro (canto esquerdo, no lugar de repouso): "largura" em
#    células, "para" (linhas, colunas) até o outro lugar, "canais" que a
#    mandam para lá quando em número ímpar
# m  marca do eco: E começa a gravar; E de novo, ou o tempo, solta o eco
# e  esteira: chão que leva; "sentido" na célula, senão o do andar em
#    "esteira": {"sentido", "canais"}; número ímpar de canais ligados
#    repinta todas ao contrário
# relógio com "passos" no lugar de "duracao": fecha contando passos da íris
# tema: nome do jogo de peças do andar (o atlas assets/tema-<nome>.png)
# caixa: png da coisa que se empurra neste andar
# aberto: andar a céu aberto, sem coluna na emenda dos fundos (a cobertura)
# cenario: os objetos do autor (docs/historia.md), postos onde o quebra-cabeça
#    acontece. cada um: {"arte", "coluna", "linha"}, de pé no chão da célula
#    ou, com "parede": True, pendurado a partir do alto dela; "dx" e "dy"
#    ajustam em px. "vivo" faz o objeto mostrar o estado do andar:
#    "relogio" (a hora de verdade), "monitores" (o que cada câmera vê) e
#    "lousa" (com "canal": quais controles do canal já valem)
# lugares: True marca no chão o lugar de onde cada caixa saiu
# k  pista (docs/andares.md, versão 7): "pista" é o nome em documentos.pistas;
#    "arte", o png do objeto (sem ela, a pista é um ponto do cenário);
#    "auto": True anota a pista sozinha quando a íris passa pela coluna dela
# t  tranca de segredo: "enigma" é o nome em documentos.enigmas; aberta, liga
#    o "canal" e não desliga mais
# K  porta de segredo: abre com o canal da tranca
# a saída com "canal" só deixa passar com o canal ligado
# "tinta" numa célula vazia: algarismo que só aparece no cone de uma câmera
# licoes: só o treino. [(coluna em que a sala começa, nome da lição)]; o
#    texto mora em roteiro.licoes, e o recomeço volta ao começo da sala

altura_mapa = 12
tipos_de_porta = {"B": "botao", "A": "alavanca", "r": "relogio", "K": "codigo"}
duplas = "BArKsd"

# campos de detalhes aceitos por letra
campos = {
    "b": {"canal"}, "a": {"canal"},
    "B": {"canal", "invertida", "aberta", "caixa"},
    "A": {"canal", "canais", "invertida", "aberta", "caixa"},
    "r": {"canal", "duracao", "passos"},
    "V": {"largura", "para", "canais", "invertida"},
    "e": {"sentido"},
    "v": {"canal", "direcao", "alcance", "inclinacao", "abertura"},
    ".": {"decoracao", "tinta"},
    "k": {"pista", "arte", "auto"}, "t": {"enigma", "canal"}, "K": {"canal"}, "s": {"canal"},
}

# os dez andares aprovados em docs/andares.md; o texto vem de lá, sem retoque

ANDAR_1 = {
    "nome": "Recepção", "ano": None, "fundo": "pano-01.png", "tema": "recepcao",
    "cenario": [{"arte": "mobilia-balcao-recepcao.png", "coluna": 31, "linha": 10, "dx": 16},
                {"arte": "mobilia-catraca.png", "coluna": 36, "linha": 10}],
    "mapa": [
        "########################################",
        "#............#............#............#",
        "#............#............#............#",
        "#............#.........................#",
        "#............#.........................#",
        "#............#........########.........#",
        "#............#............#............#",
        "#..................##.....#............#",
        "#.........................#............#",
        "#............#..##........#....k...t.s.#",
        "#.i.....#....#..##........#..........s.#",
        "########################################",
    ],
    "detalhes": {
        (8, 2): {"decoracao": "tecla-esquerda.png"},
        (8, 3): {"decoracao": "tecla-direita.png"},
        (8, 7): {"decoracao": "tecla-espaco.png"},
        (9, 31): {"pista": "cracha", "arte": "pista-prancheta.png"},
        (9, 35): {"enigma": "cracha", "canal": "catraca"},
        (9, 37): {"canal": "catraca"},
    },
    "regras": {},
}

ANDAR_2 = {
    "nome": 'Benedito Prado',
    "ano": 2009,
    "fundo": "pano-02.png",
    "tema": 'prado',
    "cenario": [{"arte": "mobilia-mesa-prado.png", "coluna": 4, "linha": 10}],
    "mapa": [
        "##################################################",
        "#................................................#",
        "#................................................#",
        "#.............................................s..#",
        "#.......................................k..t..s..#",
        "#.......................######gggg...#############",
        "#.......................######.......#############",
        "#......................g######g......#############",
        "#..p........####........######.......#############",
        "#..........g####......g.######.g.....#############",
        "#.i.........####........######....k..#############",
        "##################################################",
    ],
    "detalhes": {
        (4, 40): {"pista": "calendario", "arte": "pista-calendario.png"},
        (10, 34): {"pista": "copo", "arte": "pista-copo.png"},
        (4, 43): {"enigma": "prado", "canal": "prado"},
        (3, 46): {"canal": "prado"},
    },
    'regras': {},
}

ANDAR_3 = {
    "nome": 'Adélia Ferraz',
    "ano": 2011,
    "fundo": "pano-03.png",
    "tema": 'ferraz',
    "cenario": [{"arte": "mobilia-mesa-ferraz.png", "coluna": 16, "linha": 10}],
    "mapa": [
        "######################################################",
        "#..........V........................V..V..........s..#",
        "#..............................................t..s..#",
        "#............................................#########",
        "#....................................................#",
        "#.........................................V..........#",
        "#.......................ak.a.........................#",
        "#.............##........####.........................#",
        "#..p..........##.....................................#",
        "#.............##.k...................................#",
        "#.i.....a.....##....a............k..............k....#",
        "######################################################",
    ],
    "detalhes": {
        (9, 17): {"pista": "manual", "arte": "pista-livro.png"},
        (6, 25): {"pista": "amarelo", "arte": "pista-lembrete-amarelo.png"},
        (10, 48): {"pista": "rosa", "arte": "pista-lembrete-rosa.png"},
        (10, 33): {"pista": "azul", "arte": "pista-lembrete-azul.png"},
        (2, 47): {"enigma": "ferraz", "canal": "ferraz"},
        (1, 50): {"canal": "ferraz"},
        (10, 8): {'canal': 'treino'},
        (1, 11): {'largura': 3, 'para': (8, 0), 'canais': ['treino']},
        (10, 20): {'canal': 'chao'},
        (6, 24): {'canal': 'degrau'},
        (6, 27): {'canal': 'alto'},
        (1, 36): {'largura': 3, 'para': (8, 0), 'canais': ['chao', 'degrau']},
        (1, 39): {'largura': 3, 'para': (6, 0), 'canais': ['degrau', 'alto']},
        (5, 42): {'largura': 3, 'para': (4, -14), 'canais': ['chao', 'alto']},
    },
    'regras': {},
    'marcas': {'treino': 'triangulo', 'chao': 'circulo', 'degrau': 'quadrado', 'alto': 'losango'},
}

ANDAR_4 = {
    "nome": 'Solano Vieira',
    "ano": 2012,
    "fundo": "pano-04.png",
    "tema": 'vieira',
    "cenario": [{"arte": "mobilia-mesas-vieira.png", "coluna": 47, "linha": 10}],
    "mapa": [
        "################################################################",
        "#................#......................#.....#................#",
        "#................#......................#.....#................#",
        "#................#......................#.....#................#",
        "#................#......................#.....#................#",
        "#................#......................#.....#................#",
        "#................#......................#.....#................#",
        "#................#......................#.....#................#",
        "#.p..............#......................#.....#................#",
        "#................B......................B.....B.......k..t.s...#",
        "#.i.b...m.....b..B...b..m..b............B..b..B.k..k.......s...#",
        "################################################################",
    ],
    "detalhes": {
        (10, 48): {"pista": "mesa-com"},
        (10, 51): {"pista": "mesa-sem"},
        (9, 54): {"pista": "foto", "arte": "pista-foto.png"},
        (9, 57): {"enigma": "vieira", "canal": "vieira"},
        (9, 59): {"canal": "vieira"},
        (10, 4): {'canal': 'par'},
        (10, 14): {'canal': 'par'},
        (9, 17): {'canal': 'par'},
        (10, 21): {'canal': 'longe'},
        (9, 40): {'canal': 'longe'},
        (10, 27): {'canal': 'dois'},
        (10, 43): {'canal': 'dois'},
        (9, 46): {'canal': 'dois'},
    },
    'regras': {'par': 'todos', 'dois': 'todos'},
    'marcas': {'par': 'circulo', 'longe': 'triangulo', 'dois': 'quadrado'},
}

ANDAR_5 = {
    "nome": 'Noemi Contreiras',
    "ano": 2014,
    "fundo": "pano-05.png",
    "tema": 'contreiras',
    "cenario": [{"arte": "mobilia-porta-emparedada.png", "coluna": 48, "linha": 7, "dx": 8}],
    "mapa": [
        "########################################################",
        "#......................................................#",
        "#......................................................#",
        "#......................................................#",
        "#.s..........k......k........k........k................#",
        "#.st...................................................#",
        "#####..................................................#",
        "#................................................k.a...#",
        "#......p..eeeeeeee......eeeeeeeeeeee......eeeeee########",
        "#.........########......############......##############",
        "#.....i..##########.....#############.....##############",
        "########################################################",
    ],
    "detalhes": {
        (7, 49): {"pista": "emparedada", "auto": True},
        (4, 13): {"pista": "seta-1", "arte": "seta-pintada-direita.png", "auto": True},
        (4, 20): {"pista": "seta-2", "arte": "seta-pintada-cima.png", "auto": True},
        (4, 29): {"pista": "seta-3", "arte": "seta-pintada-direita.png", "auto": True},
        (4, 38): {"pista": "seta-4", "arte": "seta-pintada-baixo.png", "auto": True},
        (7, 51): {'canal': 'contra'},
        (5, 3): {"enigma": "contreiras", "canal": "contreiras"},
        (4, 2): {"canal": "contreiras"},
    },
    'regras': {},
    'marcas': {'contra': 'losango'},
    'esteira': {'sentido': 'direita', 'canais': ['contra']},
}

ANDAR_6 = {
    "nome": "Selene Amparo", "ano": 2016, "fundo": "pano-06.png", "tema": "amparo",
    "cenario": [{"arte": "mobilia-estante-amparo.png", "coluna": 65, "linha": 10},
                {"arte": "mobilia-copa-amparo.png", "coluna": 69, "linha": 10}],
    "lugares": True,
    "mapa": [
        "##############################################################################",
        "#..................#..........................#...............#..............#",
        "#..................#..........................#...............#..............#",
        "#..................#..........................#...............#..............#",
        "#..................#..........................#...............#..............#",
        "#..................############...............#....c..........#..............#",
        "#.............................................#...###......#..#..............#",
        "#......................c......................B............#..B..............#",
        "#..p....#########..############...............B..c.........#..B..............#",
        "#..................############...............#######.#########..........t.s.#",
        "#.i......c.........############b..............#################c..k...k....s.#",
        "##############################################################################",
    ],
    "detalhes": {
        (10, 66): {"pista": "estante"},
        (10, 70): {"pista": "xicara"},
        (9, 73): {"enigma": "amparo", "canal": "arquivo"},
        (9, 75): {"canal": "arquivo"},
        (8, 5): {'decoracao': 'tecla-r.png'},

        (10, 31): {'canal': 'amparo-1'},
        (7, 46): {'canal': 'amparo-1'},
        (7, 62): {'canal': 'amparo-2', 'aberta': True, 'caixa': True},
    },
    "regras": {},
}

ANDAR_7 = {
    "nome": "Aníbal Sobral", "ano": 2018, "fundo": "pano-07.png", "tema": "sobral", "caixa": "caixa-sobral.png",
    "cenario": [{"arte": "mobilia-esquema-sobral.png", "coluna": 54, "linha": 2, "parede": True},
                {"arte": "mobilia-mesa-sobral.png", "coluna": 61, "linha": 10},
                {"arte": "lousa.png", "coluna": 10, "linha": 5, "parede": True, "vivo": "lousa", "canal": "par"},
                {"arte": "lousa.png", "coluna": 21, "linha": 5, "parede": True, "vivo": "lousa", "canal": "sobral"},
                {"arte": "lousa.png", "coluna": 37, "linha": 5, "parede": True, "vivo": "lousa", "canal": "sobral"}],
    "mapa": [
        "#######################################################################",
        "#............#..........................#.............................#",
        "#............#..........................#.............................#",
        "#............#..........................#.............................#",
        "#............#..........................#.............................#",
        "#............#..........................#.............................#",
        "#............#..........................#.............................#",
        "#............#..........................#....c......#.................#",
        "#..p.........#..........................#...###.....#.................#",
        "#............B..........................B...........#....k....k..t.s..#",
        "#.i.cb...b...B....b......c..b...........B..c........#..............s..#",
        "#######################################################################",
    ],
    "detalhes": {
        (9, 57): {"pista": "esquema"},
        (9, 62): {"pista": "carta", "arte": "pista-carta.png"},
        (9, 65): {"enigma": "sobral", "canal": "predio"},
        (9, 67): {"canal": "predio"},
        (10, 5): {'canal': 'par'},
        (10, 9): {'canal': 'par'},
        (9, 13): {'canal': 'par'},
        (10, 18): {'canal': 'sobral'},
        (10, 28): {'canal': 'sobral'},
        (9, 40): {'canal': 'sobral'},
    },
    "regras": {'par': 'todos', 'sobral': 'todos'},
    "marcas": {'par': 'circulo', 'sobral': 'triangulo'},
}

ANDAR_8 = {
    "nome": "Cássia Mirante", "ano": 2020, "fundo": "pano-08.png", "tema": "mirante", "caixa": "caixa-mirante.png",
    "cenario": [{"arte": "mobilia-monitores-mirante.png", "coluna": 4, "linha": 10, "dx": 16, "vivo": "monitores"}],
    "mapa": [
        "############################################################################",
        "#......#.........................#.............#...#............#..........#",
        "#......#.........................#.............#...#............#..........#",
        "#......#.........................#.............#...#............A........s.#",
        "#......#.........................#.............#v.cA............A........s.#",
        "#......#.........................#.............#..#A.....###################",
        "#......#.........................#.............#...#............############",
        "#......K.......####.###.###.###..#.............#...#...##.......############",
        "#..p...K........................v####..#......v#...#............############",
        "#tk....#....##.........................#.............#..........############",
        "#.i....#....##.....................c..b#.........a..a#..........############",
        "############################################################################",
    ],
    "detalhes": {
        (9, 1): {"enigma": "mirante", "canal": "monitores"},
        (9, 2): {"pista": "ocorrencias", "arte": "pista-prancheta.png"},
        (7, 7): {"canal": "monitores"},
        # um algarismo no cone de cada câmera, na ordem dos monitores
        (9, 26): {"tinta": "3"}, (9, 42): {"tinta": "8"}, (4, 57): {"tinta": "1"},
        (8, 32): {'direcao': 'esquerda', 'alcance': 12},
        (8, 46): {'direcao': 'esquerda', 'alcance': 12, 'canal': 'cassia'},
        (10, 38): {'canal': 'cassia'},
        # a da janela olha reto pelo corredor de cima, na altura da íris
        (4, 48): {'direcao': 'direita', 'alcance': 14, 'canal': 'mirante', 'inclinacao': 0, 'abertura': 30},
        (4, 51): {'canal': 'espelho', 'invertida': True},
        (3, 64): {'canal': 'mirante', 'invertida': True},
        (10, 49): {'canal': 'mirante'},
        (10, 52): {'canal': 'espelho'},
    },
    "regras": {},
    "marcas": {'mirante': 'losango', 'espelho': 'quadrado'},
}

ANDAR_9 = {
    "nome": "Otávio Quaresma", "ano": 2022, "fundo": "pano-09.png", "tema": "quaresma", "caixa": "caixa-quaresma.png",
    "cenario": [{"arte": "mobilia-relogio-quaresma.png", "coluna": 4, "linha": 3, "parede": True, "vivo": "relogio"}],
    "mapa": [
        "###############################################################################",
        "#......#..........................#............#........#.................#...#",
        "#......#..........................#............#........#.................#...#",
        "#......#..........................#............#........#.................#...#",
        "#......#..........................#............#........#.................#...#",
        "#......#..........................#............#........#.................#...#",
        "#......#......b...................#.a..........#........#...bc............#..s#",
        "#............################.....#####........#........#...###...........#..s#",
        "#..p..............................#............#........#.................#..##",
        "#......#......................##..r.....##.....r........r.#.....k.k.t.k...r..##",
        "#.i....#......................##..r.....##.....r........r.#...............r..##",
        "###############################################################################",
    ],
    "detalhes": {
        (9, 64): {"pista": "riscos", "arte": "pista-riscos.png"},
        (9, 68): {"enigma": "quaresma", "canal": "quaresma-saida"},
        (9, 66): {"pista": "bilhete-da-porta", "arte": "pista-bilhete.png"},
        (9, 70): {"pista": "projeto", "arte": "pista-prancheta.png"},
        (6, 77): {"canal": "quaresma-saida"},
        (6, 14): {'canal': 'quaresma-1'},
        (9, 34): {'canal': 'quaresma-1', 'passos': 14},
        (6, 36): {'canal': 'quaresma-2'},
        (9, 47): {'canal': 'quaresma-2', 'passos': 17},
        (9, 56): {'canal': 'quaresma-2', 'passos': 17},
        (6, 60): {'canal': 'quaresma-3'},
        (9, 74): {'canal': 'quaresma-3', 'passos': 11},
    },
    "regras": {},
    "marcas": {'quaresma-1': 'triangulo', 'quaresma-2': 'quadrado', 'quaresma-3': 'circulo'},
}

ANDAR_10 = {
    "nome": "Cobertura", "ano": None, "fundo": "pano-10.png", "tema": "cobertura",
    "mapa": [
        "##############################",
        "#............................#",
        "#............................#",
        "#............................#",
        "#............................#",
        "#............................#",
        "#............................#",
        "#............................#",
        "#..p.........................#",
        "#.............###..........d.#",
        "#.i......#....####.........d.#",
        "##############################",
    ],
    "detalhes": {},
    "regras": {},
    "aberto": True,
}

ANDARES = [ANDAR_1, ANDAR_2, ANDAR_3, ANDAR_4, ANDAR_5,
           ANDAR_6, ANDAR_7, ANDAR_8, ANDAR_9, ANDAR_10]

# o treino (docs/andares.md, versão 6): uma sala por mecanismo, na ordem em
# que o prédio os apresenta, cada uma com a sua lição escrita na tela e sem
# como errar. fica fora dos dez: abre pelo menu, não tem número, não grava nada
TREINO = {
    "nome": "Treino", "ano": None, "fundo": "pano-treino.png", "tema": "recepcao",
    "mapa": [
        "###################################################################################################################################",
        "#................#.......#...............V...................#..............................................#......#.......#......#",
        "#................#.......#...................................#..............................................#......#.......#......#",
        "#................#.......#...................................#..............................................#......#.......#......#",
        "#................#.......#...................................#..............................................#......#.......#......#",
        "#................#.......#...................................#..............................................#......#.......#......#",
        "#................#.......#...................................#..............................................#......#.......#......#",
        "#................#.......#..................##...............#..............................................#......#.......#......#",
        "#................#.......#.....##...........##...............#...eeeee......########....##..##.............v#......#.......#......#",
        "#.....##.........B.......A....g##...........##...............B...#####......########........##.....................A.......rk.ts..#",
        "#.i...##....b....B...a...A.....##.....a.....##..b...m.....b..B..#######.....########....c...##....a............a...A..b....r...s..#",
        "###################################################################################################################################",
    ],
    "detalhes": {
        (10, 12): {'canal': 'pisar'}, (9, 17): {'canal': 'pisar'},
        (10, 21): {'canal': 'chave'}, (9, 25): {'canal': 'chave'},
        (10, 38): {'canal': 'ferro'}, (1, 41): {'largura': 3, 'para': (8, 0), 'canais': ['ferro']},
        (10, 48): {'canal': 'dois'}, (10, 58): {'canal': 'dois'}, (9, 61): {'canal': 'dois'},
        (10, 98): {'canal': 'vigia'}, (8, 107): {'canal': 'vigia', 'direcao': 'esquerda', 'alcance': 6},
        (10, 111): {'canal': 'avesso'}, (9, 115): {'canal': 'avesso', 'invertida': True},
        (10, 118): {'canal': 'conta'}, (9, 123): {'canal': 'conta', 'passos': 6},
        (9, 124): {"pista": "bilhete-de-treino", "arte": "pista-bilhete.png"},
        (9, 126): {"enigma": "treino", "canal": "segredo"}, (9, 127): {"canal": "segredo"},
    },
    "regras": {'dois': 'todos'},
    "marcas": {'pisar': 'circulo', 'chave': 'triangulo', 'ferro': 'quadrado', 'dois': 'losango',
               'vigia': 'cruz', 'avesso': 'circulo', 'conta': 'triangulo'},
    "esteira": {"sentido": "direita", "canais": []},
    "licoes": [(1, "mover"), (9, "botao"), (18, "alavanca"), (26, "gaveta"), (36, "viga"), (47, "eco"),
               (62, "esteira"), (85, "caixa"), (96, "camera"), (109, "invertida"), (116, "passos"), (124, "segredo")],
}
# o índice do treino é um nome, não um número
treino = "treino"


def andar_de(indice):
    return TREINO if indice == treino else ANDARES[indice]


def falhar(andar, texto):
    raise ValueError("andar %s: %s" % (andar["nome"], texto))


def validar_forma(andar):
    mapa = andar["mapa"]
    if len(mapa) != altura_mapa:
        falhar(andar, "%d linhas, esperado %d" % (len(mapa), altura_mapa))
    if len({len(linha) for linha in mapa}) != 1:
        falhar(andar, "linhas de comprimentos diferentes")
    if set(mapa[0] + mapa[-1] + "".join(l[0] + l[-1] for l in mapa)) != {"#"}:
        falhar(andar, "a borda precisa ser toda de parede")
    texto = "".join(mapa)
    if texto.count("i") != 1:
        falhar(andar, "precisa de exatamente um início")
    if "s" not in texto and "d" not in texto:
        falhar(andar, "precisa de saída ou diamante")


def validar_duplas(andar):
    # cada dupla ocupa exatamente duas células empilhadas
    mapa = andar["mapa"]
    for coluna in range(len(mapa[0])):
        linha = 0
        while linha < altura_mapa:
            letra = mapa[linha][coluna]
            fim = linha
            while fim + 1 < altura_mapa and mapa[fim + 1][coluna] == letra:
                fim = fim + 1
            if letra in duplas and (fim - linha + 1) % 2:
                falhar(andar, "%s em (%d, %d) sem par vertical" % (letra, linha, coluna))
            linha = fim + 1


def validar_detalhes(andar):
    mapa = andar["mapa"]
    for (linha, coluna), dados in andar["detalhes"].items():
        if not (0 <= linha < altura_mapa and 0 <= coluna < len(mapa[0])):
            falhar(andar, "detalhe fora do mapa em (%d, %d)" % (linha, coluna))
        letra = mapa[linha][coluna]
        estranhos = set(dados) - campos.get(letra, set())
        if estranhos:
            falhar(andar, "%s não combina com %r em (%d, %d)" % (sorted(estranhos), letra, linha, coluna))
    for linha, texto in enumerate(mapa):
        for coluna, letra in enumerate(texto):
            dados = andar["detalhes"].get((linha, coluna), {})
            if letra == "r" and topo(mapa, linha, coluna) and not {"duracao", "passos"} & set(dados):
                falhar(andar, "relógio sem duracao em (%d, %d)" % (linha, coluna))
            if letra == "V" and not {"largura", "para", "canais"} <= set(dados):
                falhar(andar, "viga sem largura, para ou canais em (%d, %d)" % (linha, coluna))
            if letra == "v" and not {"direcao", "alcance"} <= set(dados):
                falhar(andar, "câmera sem direcao ou alcance em (%d, %d)" % (linha, coluna))
            if letra == "k" and dados.get("pista") not in documentos.pistas:
                falhar(andar, "pista desconhecida em (%d, %d): %r" % (linha, coluna, dados.get("pista")))
            if letra == "t" and (dados.get("enigma") not in documentos.enigmas or "canal" not in dados):
                falhar(andar, "tranca sem enigma conhecido ou sem canal em (%d, %d)" % (linha, coluna))


vivos = ("relogio", "monitores", "lousa")
campos_do_cenario = {"arte", "coluna", "linha", "parede", "dx", "dy", "vivo", "canal"}


def validar_cenario(andar):
    mapa = andar["mapa"]
    for objeto in andar.get("cenario", []):
        estranhos = set(objeto) - campos_do_cenario
        if estranhos or not {"arte", "coluna", "linha"} <= set(objeto):
            falhar(andar, "objeto de cenário mal formado: %r" % objeto)
        if not (0 <= objeto["linha"] < altura_mapa and 0 <= objeto["coluna"] < len(mapa[0])):
            falhar(andar, "objeto de cenário fora do mapa: %r" % objeto["arte"])
        if objeto.get("vivo") not in (None,) + vivos:
            falhar(andar, "cenário vivo desconhecido: %r" % objeto["vivo"])
        if objeto.get("vivo") == "lousa" and objeto.get("canal") not in canais_do_mapa(andar):
            falhar(andar, "lousa de canal que não existe no mapa: %r" % objeto.get("canal"))
    for coluna, nome in andar.get("licoes", []):
        if not (0 <= coluna < len(mapa[0])) or mapa[altura_mapa - 2][coluna] not in ".i":
            falhar(andar, "lição %r começa numa coluna sem chão livre" % nome)


def canais_do_mapa(andar):
    # canais de controles, portas e câmeras; sem "canal", controle e porta
    # ficam no canal "padrao"
    canais = set()
    for (linha, coluna), dados in andar["detalhes"].items():
        if "canal" in dados:
            canais.add(dados["canal"])
        canais.update(dados.get("canais", []))
    for linha, texto in enumerate(andar["mapa"]):
        for coluna, letra in enumerate(texto):
            sem_canal = "canal" not in andar["detalhes"].get((linha, coluna), {})
            if letra in "baBArK" and sem_canal and "canais" not in andar["detalhes"].get((linha, coluna), {}):
                canais.add("padrao")
    return canais


def validar_canais(andar):
    canais = canais_do_mapa(andar)
    canais.update(andar.get("esteira", {}).get("canais", []))
    for canal, segundos in andar.get("memorias", {}).items():
        if andar["regras"].get(canal) != "todos":
            falhar(andar, "memória no canal %r, que não é \"todos\"" % canal)
        if segundos < 0:
            falhar(andar, "memória negativa no canal %r" % canal)
    for canal, forma in andar.get("marcas", {}).items():
        if canal not in canais:
            falhar(andar, "marca do canal %r, que não existe no mapa" % canal)
        if forma not in cfg.formas_de_marca:
            falhar(andar, "forma de marca desconhecida: %r" % forma)


def topo(mapa, linha, coluna):
    # célula de cima de uma dupla: número par de letras iguais logo acima
    letra = mapa[linha][coluna]
    acima = 0
    while linha - acima - 1 >= 0 and mapa[linha - acima - 1][coluna] == letra:
        acima = acima + 1
    return letra in duplas and acima % 2 == 0


def fase_vazia(andar):
    mapa = andar["mapa"]
    return {
        "nome": andar["nome"], "fundo": andar["fundo"], "regras": andar["regras"],
        "memorias": andar.get("memorias", {}), "marcas": andar.get("marcas", {}),
        "aberto": andar.get("aberto", False), "tema": andar.get("tema"), "arte_caixa": andar.get("caixa"),
        "cenario": [dict(objeto) for objeto in andar.get("cenario", [])],
        "lugares": [], "marcar_lugares": andar.get("lugares", False), "licoes": andar.get("licoes", []),
        # mirante: o lugar diante dos monitores; olhar: a vez e o tempo da câmera que a visão mostra
        "mirante": None, "olhar": None,
        "largura": len(mapa[0]) * cfg.tile, "paredes": [], "caixas": [], "botoes": [],
        "alavancas": [], "portas": [], "cameras": [], "decoracoes": [], "canais": {},
        "gavetas": [], "vigas": [], "esteiras": {}, "eventos": [],
        # a investigação: pistas, trancas, tinta que só a câmera acende e o
        # canal que destranca a saída (None: saída livre)
        "pistas": [], "trancas": [], "tintas": [], "canal_da_saida": None,
        "eco": {"marcas": [], "gravando": False, "fita": [], "tempo": 0.0, "origem": None,
                "tocando": False, "indice": 0, "atual": None, "marca": None},
        "esteira": dict(andar.get("esteira", {"sentido": "direita", "canais": []})),
        "celulas_parede": set(), "inicio": None, "saida": None, "diamante": None, "placa": None,
    }


def ler_celula(fase, mapa, linha, coluna, dados):
    letra = mapa[linha][coluna]
    x, y = coluna * cfg.tile, linha * cfg.tile
    canal = dados.get("canal", "padrao")
    if letra in "#e":
        borda = linha in (0, altura_mapa - 1) or coluna in (0, len(mapa[0]) - 1)
        fase["paredes"].append([x, y, borda])
        fase["celulas_parede"].add((x, y))
        if letra == "e":
            fase["esteiras"][(x, y)] = dados.get("sentido")
    elif letra == "g":
        fase["gavetas"].append({"x": x, "y": y, "aberta": False, "resta": 0.0})
    elif letra == "V":
        dl, dc = dados["para"]
        fase["vigas"].append({"x": float(x), "y": float(y), "largura": dados["largura"] * cfg.tile,
                              "repouso": (x, y), "outro": (x + dc * cfg.tile, y + dl * cfg.tile),
                              "canais": dados["canais"], "invertida": dados.get("invertida", False),
                              "andando": False})
    elif letra == "m":
        fase["eco"]["marcas"].append([x, y])
    elif letra == "c":
        fase["caixas"].append({"x": x, "y": y, "vy": 0.0, "alvo": None})
    elif letra == "b":
        fase["botoes"].append({"x": x, "y": y + cfg.tile - cfg.altura_botao,
                               "pressionado": False, "canal": canal, "memoria": 0.0})
    elif letra == "a":
        fase["alavancas"].append({"x": x, "y": y + cfg.tile - cfg.altura_alavanca,
                                  "ligada": False, "canal": canal})
    elif letra in tipos_de_porta and topo(mapa, linha, coluna):
        invertida = dados.get("invertida", False)
        canais = dados.get("canais", [])
        if canais:
            canal = canais[0]
        fase["portas"].append({"x": x, "y": y, "tipo": tipos_de_porta[letra], "canal": canal, "canais": canais,
                               "invertida": invertida, "duracao": dados.get("duracao", 0.0),
                               "passos": dados.get("passos", 0),
                               "aberta": dados.get("aberta", invertida), "folga": 0.0, "contando": False,
                               "restante": 0.0, "ativo_antes": False})
        if dados.get("caixa"):
            # caixa parada no vão, na célula de baixo da porta
            fase["caixas"].append({"x": x, "y": y + cfg.tile, "vy": 0.0, "alvo": None})
    elif letra == "v":
        fase["cameras"].append({"x": x, "y": y, "direcao": dados["direcao"], "alcance": dados["alcance"],
                                "inclinacao": dados.get("inclinacao", cfg.inclinacao_camera),
                                "abertura": dados.get("abertura", cfg.abertura_camera),
                                "canal": dados.get("canal"), "contador": 0.0, "estado": "vigiando"})
    elif letra == "i":
        # colisor mais estreito que a célula: a íris nasce no meio dela
        fase["inicio"] = [x + (cfg.tile - cfg.largura_jogador) // 2, y + cfg.tile - cfg.altura_jogador]
    elif letra == "s" and topo(mapa, linha, coluna):
        fase["saida"] = [x, y]
        fase["canal_da_saida"] = dados.get("canal")
    elif letra == "k":
        fase["pistas"].append({"x": x, "y": y, "nome": dados["pista"], "arte": dados.get("arte"),
                               "auto": dados.get("auto", False), "lida": False})
    elif letra == "t":
        rodas = len(documentos.enigmas[dados["enigma"]]["segredo"])
        fase["trancas"].append({"x": x, "y": y, "enigma": dados["enigma"], "canal": dados["canal"],
                                "ligada": False, "posicoes": [0] * rodas, "erros": 0})
    elif letra == "d" and topo(mapa, linha, coluna):
        fase["diamante"] = [x, y]
    elif letra == "p":
        fase["placa"] = [x, y]
    if "decoracao" in dados:
        fase["decoracoes"].append([x, y, dados["decoracao"]])
    if "tinta" in dados:
        fase["tintas"].append({"x": x + cfg.tile // 2, "y": y + cfg.tile // 2, "texto": dados["tinta"]})


def carregar(indice):
    andar = andar_de(indice)
    validar_forma(andar)
    validar_duplas(andar)
    validar_detalhes(andar)
    validar_canais(andar)
    validar_cenario(andar)
    fase = fase_vazia(andar)
    mapa = andar["mapa"]
    for linha in range(altura_mapa):
        for coluna in range(len(mapa[0])):
            ler_celula(fase, mapa, linha, coluna, andar["detalhes"].get((linha, coluna), {}))
    # onde cada caixa começa: o lugar dela
    fase["lugares"] = [(caixa["x"], caixa["y"]) for caixa in fase["caixas"]]
    for objeto in fase["cenario"]:
        if objeto.get("vivo") == "monitores":
            x = objeto["coluna"] * cfg.tile + objeto.get("dx", 0)
            fase["mirante"] = (x - 8, (objeto["linha"] - 1) * cfg.tile, 67, 2 * cfg.tile)
    return fase


def licao_em(fase, x):
    # a lição da sala em que está o ponto x: (coluna em que começa, nome), ou None
    atual = None
    for coluna, nome in fase["licoes"]:
        if coluna * cfg.tile <= x:
            atual = (coluna, nome)
    return atual
