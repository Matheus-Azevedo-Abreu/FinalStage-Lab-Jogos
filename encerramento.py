import configuracoes as cfg

# o fim do jogo, depois que a jogadora assina a placa: a placa pronta, o
# resultado da noite gravado linha a linha e os créditos subindo. aqui ficam
# só o tempo e os dados; quem desenha é o epilogo.py. não importa pygame

# etapas, na ordem; a duração de "resultado" e de "creditos" depende do que
# há para mostrar e é calculada em iniciar
ordem = ("placa", "resultado", "creditos")
duracoes = {"placa": 2.6, "resultado": 0.0, "creditos": 0.0}
estado = {"etapa": "placa", "tempo": 0.0, "acabou": True, "linhas": 0, "total": 0.0}

# o que aconteceu neste quadro, para o som: "linha" (mais uma linha do
# resultado gravada), "letra" (a letra da noite) e "creditos"
eventos = []

# cada linha do resultado entra depois deste tempo; a letra da noite, um
# pouco depois da última; e o resultado fica na tela mais este tanto
tempo_por_linha = 0.28
espera_da_letra = 0.6
pausa_do_resultado = 4.5
# os créditos sobem a tantas unidades de interface por segundo
velocidade = 26
# antes disto a tecla não pula a etapa: ninguém perde a placa sem querer
guarda = 0.7

# os créditos: (tipo, texto). tipos: "titulo" (o letreiro do jogo), "papel"
# (cabeçalho), "nome" (linha), "assinatura" (a que a jogadora gravou) e
# "vazio". altura de cada tipo, em unidades de interface
alturas = {"titulo": 78, "papel": 30, "nome": 20, "assinatura": 56, "vazio": 22}
creditos = [
    ("titulo", ""),
    ("papel", "UM JOGO DE"),
    ("nome", "Matheus Azevedo Abreu"),
    ("nome", "Gabriel Ribeiro Ota Yida"),
    ("nome", "Enzo Lemos Von Paumgartten Klautau"),
    ("vazio", ""),
    ("papel", "COM"),
    ("nome", "Íris Portela, candidata"),
    ("nome", "Selene Amparo, coordenadora de processo"),
    ("vazio", ""),
    ("papel", "OS ANDARES E QUEM OS PROJETOU"),
    ("nome", "2  ·  Benedito Prado, 2009  ·  a gaveta"),
    ("nome", "3  ·  Adélia Ferraz, 2011  ·  a viga"),
    ("nome", "4  ·  Solano Vieira, 2012  ·  o eco"),
    ("nome", "5  ·  Noemi Contreiras, 2014  ·  a esteira"),
    ("nome", "6  ·  Selene Amparo, 2016  ·  a caixa"),
    ("nome", "7  ·  Aníbal Sobral, 2018  ·  a pilha"),
    ("nome", "8  ·  Cássia Mirante, 2020  ·  a câmera"),
    ("nome", "9  ·  Otávio Quaresma, 2022  ·  os passos"),
    ("nome", "11  ·  até o fim do ano"),
    ("assinatura", ""),
    ("vazio", ""),
    ("papel", "ARTE"),
    ("nome", "gerada por inteligência artificial (ChatGPT, OpenAI)"),
    ("nome", "sob direção do time"),
    ("nome", "arte e resolução de bugs: Enzo Lemos Von Paumgartten Klautau"),
    ("nome", "peças dos andares, interface e cenário desenhados por código"),
    ("vazio", ""),
    ("papel", "SOM"),
    ("nome", "efeitos e faixa ambiente sintetizados por código"),
    ("vazio", ""),
    ("papel", "FONTES"),
    ("nome", "Silkscreen  ·  VT323"),
    ("nome", "SIL Open Font License"),
    ("vazio", ""),
    ("papel", "FEITO COM"),
    ("nome", "Python  ·  pygame  ·  Power PPlay 2.0"),
    ("nome", "PPlay: Prof. Esteban Clua, Prof. Anselmo Montenegro,"),
    ("nome", "Gabriel Saldanha, Adônis Gasiglia, Yuri Nogueira, Sergio Herman"),
    ("nome", "Power PPlay 2.0: Kauã Neves Jesus de Paula"),
    ("vazio", ""),
    ("papel", "LABORATÓRIO DE INTRODUÇÃO À PROGRAMAÇÃO"),
    ("nome", "Universidade Federal Fluminense  ·  2026"),
    ("nome", "Prof. Esteban Walter Gonzalez Clua"),
    ("vazio", ""),
    ("vazio", ""),
    ("papel", "O TEMPO FOI ANOTADO."),
    ("nome", "Obrigado por jogar."),
]


def altura_do_rolo():
    return sum(alturas[tipo] for tipo, _ in creditos)


def iniciar(linhas):
    # linhas: quantos andares o resultado tem para gravar
    estado["etapa"] = "placa"
    estado["tempo"] = 0.0
    estado["total"] = 0.0
    estado["acabou"] = False
    estado["linhas"] = linhas
    duracoes["resultado"] = linhas * tempo_por_linha + espera_da_letra + pausa_do_resultado
    tela = cfg.altura_tela / cfg.escala_interface
    duracoes["creditos"] = (altura_do_rolo() + tela + 30) / velocidade
    eventos[:] = []


def ativo():
    return not estado["acabou"]


def etapa():
    return estado["etapa"]


def tempo():
    return estado["tempo"]


def fracao():
    # de 0 a 1 dentro da etapa em curso
    return min(1.0, estado["tempo"] / duracoes[estado["etapa"]])


def proxima_etapa():
    posicao = ordem.index(estado["etapa"])
    if posicao + 1 >= len(ordem):
        estado["acabou"] = True
        return
    estado["etapa"] = ordem[posicao + 1]
    estado["tempo"] = 0.0
    if estado["etapa"] == "creditos":
        eventos.append("creditos")


def avancar():
    # a tecla de quem tem pressa: pula para a etapa seguinte
    if estado["tempo"] >= guarda:
        proxima_etapa()


def encerrar():
    estado["acabou"] = True


def linhas_gravadas():
    # quantas linhas do resultado já estão na placa
    if estado["etapa"] == "placa":
        return 0
    if estado["etapa"] == "creditos":
        return estado["linhas"]
    return min(estado["linhas"], int(estado["tempo"] / tempo_por_linha))


def letra_gravada():
    # a letra da noite entra depois da última linha
    if estado["etapa"] == "placa":
        return False
    return estado["etapa"] == "creditos" or estado["tempo"] >= estado["linhas"] * tempo_por_linha + espera_da_letra


def rolagem():
    # quanto os créditos já subiram, em unidades de interface
    return estado["tempo"] * velocidade if estado["etapa"] == "creditos" else 0.0


def atualizar(passo):
    eventos[:] = []
    if estado["acabou"]:
        return
    linhas, letra = linhas_gravadas(), letra_gravada()
    estado["tempo"] = estado["tempo"] + passo
    estado["total"] = estado["total"] + passo
    if linhas_gravadas() > linhas:
        eventos.append("linha")
    if letra_gravada() and not letra:
        eventos.append("letra")
    if estado["tempo"] >= duracoes[estado["etapa"]]:
        proxima_etapa()
