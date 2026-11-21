# o que a íris investiga (docs/andares.md, versão 7): as pistas que os autores
# deixaram em cada andar e os segredos das trancas. só texto, como roteiro.py.
# nenhum segredo está escrito pronto (fora o crachá e o treino, que ensinam):
# sai de juntar as pistas com o que se vê no andar

# pista: título, papel (a folha em que o texto aparece), parágrafos e, se
# houver, a figura desenhada acima do texto (assets/figura-<nome>.png).
# papéis: "folha", "bilhete", "ficha", "amarelo", "rosa", "azul", "parede"
pistas = {
    "cracha": {
        "titulo": "PORTARIA — TURNO DA NOITE", "papel": "ficha",
        "texto": ["Etapa 7. Avaliação prática.",
                  "Candidata: PORTELA, Í.",
                  "Processos anteriores: 31. Meses de espera: 7.",
                  "Crachá provisório nº 0731.",
                  "Digite o número do crachá na catraca."]},
    "calendario": {
        "titulo": "CALENDÁRIO DE PAREDE", "papel": "parede", "figura": "figura-calendario.png",
        "texto": ["Agosto de 2009. Dia 3, a lápis: \"começo\". Dia 14, circulado: \"pronto\". "
                  "Dia 21: \"chega a placa\".",
                  "Ninguém virou a folha depois."]},
    "copo": {
        "titulo": "BILHETE SOB UM COPO DE CAFÉ", "papel": "bilhete",
        "texto": ["O café virou pedra dentro do copo.",
                  "\"Senha da saída: o dia em que dei o andar por pronto, e o mês. Quatro algarismos.\"",
                  "\"Funciona. Não mexo mais. — Benedito\""]},
    "manual": {
        "titulo": "MANUAL DO ANDAR 3 — A. FERRAZ", "papel": "folha",
        "texto": ["1. A senha da saída: nos lembretes.",
                  "2. Amarelo é rascunho. Rosa corrige o amarelo. Azul corrige o rosa.",
                  "3. Siga a ordem: correção fora de hora estraga a outra.",
                  "4. Se uma alavanca não bastar, há outras.",
                  "Lombada sem vinco: ninguém leu."]},
    "amarelo": {
        "titulo": "LEMBRETE AMARELO", "papel": "amarelo",
        "texto": ["SENHA DA SAÍDA", "4  7  1", "(conferir depois)"]},
    "rosa": {
        "titulo": "LEMBRETE ROSA", "papel": "rosa",
        "texto": ["Errei.", "O primeiro algarismo: some 2."]},
    "azul": {
        "titulo": "LEMBRETE AZUL", "papel": "azul",
        "texto": ["Errei de novo.", "Troque o primeiro com o último.", "Agora basta. Acho."]},
    "mesa-com": {
        "titulo": "GAVETA DA MESA COM CADEIRA", "papel": "bilhete",
        "texto": ["\"Senha em duas metades, uma em cada mesa.\"",
                  "\"A minha: 27.\"",
                  "\"A outra fica com quem senta à minha frente. — Solano\""]},
    "mesa-sem": {
        "titulo": "GAVETA DA MESA SEM CADEIRA", "papel": "bilhete",
        "texto": ["A mesma letra.",
                  "\"Ninguém nunca sentou aqui. De noite, quem senta à minha frente sou eu, no vidro da janela.\"",
                  "\"Ele guarda a outra metade. Escreve tudo ao contrário.\""]},
    "foto": {
        "titulo": "FOTO NA PAREDE", "papel": "folha",
        "texto": ["Dois homens à mesma mesa, um de frente para o outro.",
                  "É a mesma pessoa duas vezes. A montagem foi feita com cuidado.",
                  "No verso: \"Equipe do 4º andar, 2012\"."]},
    "emparedada": {
        "titulo": "PORTA EMPAREDADA", "papel": "parede",
        "texto": ["Pintado nos tijolos:",
                  "\"A saída que você espera era aqui. A minha fica onde você começou.\"",
                  "\"Repintei cada seta da parede ao contrário. A senha é o caminho antigo, lido por quem "
                  "volta. — Noemi\""]},
    # as quatro setas da noemi, na ordem de quem vai: anotam-se sozinhas
    "seta-1": {"titulo": "SETA NA PAREDE — 1ª DE QUEM VAI", "papel": "parede", "figura": "figura-seta-direita.png",
               "texto": ["Tinta nova, apontando para a direita.",
                         "Por baixo, raspada, a seta antiga apontava para a esquerda."]},
    "seta-2": {"titulo": "SETA NA PAREDE — 2ª DE QUEM VAI", "papel": "parede", "figura": "figura-seta-cima.png",
               "texto": ["Tinta nova, apontando para cima.",
                         "Por baixo, raspada, a seta antiga apontava para baixo."]},
    "seta-3": {"titulo": "SETA NA PAREDE — 3ª DE QUEM VAI", "papel": "parede", "figura": "figura-seta-direita.png",
               "texto": ["Tinta nova, apontando para a direita.",
                         "Por baixo, raspada, a seta antiga apontava para a esquerda."]},
    "seta-4": {"titulo": "SETA NA PAREDE — 4ª DE QUEM VAI", "papel": "parede", "figura": "figura-seta-baixo.png",
               "texto": ["Tinta nova, apontando para baixo.",
                         "Por baixo, raspada, a seta antiga apontava para cima."]},
    "xicara": {
        "titulo": "XÍCARA NA COPA", "papel": "ficha",
        "texto": ["Lavada e virada para secar. Seca há anos.",
                  "Etiqueta de patrimônio no fundo: \"COPA 6º — S. AMPARO\".",
                  "É a única coisa neste andar com o nome de alguém."]},
    "estante": {
        "titulo": "ESTANTE DO ARQUIVO", "papel": "parede", "figura": "figura-estante.png",
        "texto": ["Uma pasta por contratado, por ano.",
                  "Entre CONTREIRAS e SOBRAL, um vão sem poeira: alguém tira e põe essa pasta até hoje."]},
    "esquema": {
        "titulo": "ESQUEMA NA PAREDE", "papel": "parede", "figura": "figura-esquema.png",
        "texto": ["Na margem: \"Senha: o último algarismo do ano de cada andar pronto abaixo do meu. "
                  "Quem fica por cima vem primeiro.\""]},
    "carta": {
        "titulo": "CARTA NÃO ENVIADA", "papel": "folha",
        "texto": ["\"Entendi a vaga. Não é subir o prédio: é fazer o andar seguinte para quem vier depois.\"",
                  "\"Desenhei também os de cima. Queria saber o que ainda vão pedir de alguém.\"",
                  "\"Assino com o nome novo. O antigo ficou na recepção. — Aníbal Sobral\""]},
    "ocorrencias": {
        "titulo": "LIVRO DE OCORRÊNCIAS — C. MIRANTE", "papel": "folha",
        "texto": ["\"Cada câmera acende um algarismo no que ela vê. Só se lê por estes monitores.\"",
                  "\"A porta quer o que cada monitor mostra, de cima para baixo.\"",
                  "\"O quarto não mostra nada desde 2020. Nada também é um algarismo.\""]},
    "riscos": {
        "titulo": "RISCOS NA PAREDE", "papel": "parede", "figura": "figura-riscos.png",
        "texto": ["Um risco por dia sem janela.",
                  "Depois do último, a lápis: \"parei de contar quando deixou de ser estranho\"."]},
    "bilhete-da-porta": {
        "titulo": "BILHETE NA PAREDE", "papel": "bilhete",
        "texto": ["\"Senha da saída: primeiro, os dias que risquei nesta parede.\"",
                  "\"Depois, os passos que a última porta dá a quem passa.\"",
                  "\"Nem um a mais. — O. Quaresma\""]},
    "projeto": {
        "titulo": "PRANCHETA — PROJETO DO 11º ANDAR", "papel": "ficha",
        "texto": ["Folha em branco, com o carimbo da Vértice.",
                  "Responsável: \"a próxima contratada\".",
                  "Prazo: \"fim do ano\"."]},
    "bilhete-de-treino": {
        "titulo": "BILHETE DE TREINO", "papel": "bilhete",
        "texto": ["\"O segredo desta porta é 2 4.\"",
                  "\"No prédio ninguém deixa o segredo escrito assim: ele se deduz do que o autor do "
                  "andar deixou para trás.\""]},
}

# o que cada roda da tranca pode mostrar
rodas = {
    "digitos": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "setas": ["cima", "direita", "baixo", "esquerda"],
}

# enigma: o rótulo gravado na tranca, o tipo das rodas, o segredo (uma
# posição por roda), a dica (o que a íris pensa alto depois de errar
# algumas vezes: diz o que juntar, nunca a resposta) e a fala dela quando
# a tranca abre
enigmas = {
    "cracha": {"rotulo": "CATRACA — NÚMERO DO CRACHÁ", "rodas": "digitos", "segredo": list("0731"),
               "dica": "O número está na lista da portaria.",
               "fala": ("iris", "desconfiada", "Sete meses, trinta e um processos. Alguém aqui sabe contar.")},
    "prado": {"rotulo": "SAÍDA — DIA E MÊS", "rodas": "digitos", "segredo": list("1408"),
              "dica": "O bilhete diz o que é a senha. O calendário diz quando.",
              "fala": ("iris", "neutra", "Ele terminou e nunca mais mexeu. Dá para invejar.")},
    "ferraz": {"rotulo": "SAÍDA — A SENHA, CORRIGIDA", "rodas": "digitos", "segredo": list("176"),
               "dica": "O manual dá a ordem das cores. Uma correção de cada vez.",
               "fala": ("iris", "atenta", "Ela corrigiu a própria correção. Tinha medo de não bastar.")},
    "vieira": {"rotulo": "SAÍDA — AS DUAS METADES", "rodas": "digitos", "segredo": list("2772"),
               "dica": "Vidro de janela, à noite. O que ele devolve de um número?",
               "fala": ("iris", "cansada", "A outra metade era ele mesmo.")},
    "contreiras": {"rotulo": "SAÍDA — O CAMINHO ANTIGO", "rodas": "setas",
                   "segredo": ["cima", "esquerda", "baixo", "esquerda"],
                   "dica": "Caminho antigo é a seta de baixo. E quem volta lê do fim para o começo.",
                   "fala": ("iris", "atenta", "A saída dela fica onde eu comecei.")},
    "amparo": {"rotulo": "ARQUIVO — ANO DA PASTA RETIRADA", "rodas": "digitos", "segredo": list("2016"),
               "dica": "Que ano falta na estante?",
               "fala": ("iris", "desconfiada", "A pasta que falta é a dela.")},
    "sobral": {"rotulo": "SAÍDA — O PRÉDIO, DE CIMA PARA BAIXO", "rodas": "digitos", "segredo": list("64219"),
               "dica": "Cinco andares prontos abaixo do dele. O ano do sexto eu já vi.",
               "fala": ("iris", "cansada", "Ele desenhou os andares que não existem. O próximo é de quem chegar.")},
    "mirante": {"rotulo": "PORTA — O QUE CADA MONITOR MOSTRA", "rodas": "digitos", "segredo": list("3810"),
                "dica": "Quatro monitores. Três mostram um algarismo. O quarto mostra nada.",
                "fala": ("iris", "desconfiada", "Para ler a senha, tive que olhar por onde ela olhava.")},
    "quaresma": {"rotulo": "SAÍDA — DIAS E PASSOS", "rodas": "digitos", "segredo": list("4011"),
                 "dica": "Os dias estão riscados na parede. Os passos, em cima da última porta.",
                 "fala": ("iris", "indecifravel", "Quarenta dias. Depois ele parou de achar estranho.")},
    "treino": {"rotulo": "PORTA DE TREINO", "rodas": "digitos", "segredo": list("24"), "dica": None, "fala": None},
}

# a folha da leitura, em unidades da interface: largura do texto em letras
# (a vt323 tem largura fixa) e quantas linhas cabem, com e sem figura
letras_por_linha = 36
linhas_da_folha = 10
linhas_com_figura = 4


def quebrar(paragrafo, largura=letras_por_linha):
    # quebra por palavra, na largura fixa da letra: a mesma conta em toda tela
    linhas, atual = [], ""
    for palavra in paragrafo.split(" "):
        tentativa = palavra if not atual else atual + " " + palavra
        if len(tentativa) <= largura or not atual:
            atual = tentativa
        else:
            linhas.append(atual)
            atual = palavra
    return linhas + [atual]


def linhas_da_pista(nome):
    # o texto da pista como vai para a folha, parágrafo por parágrafo
    linhas = []
    for paragrafo in pistas[nome]["texto"]:
        linhas.extend(quebrar(paragrafo))
    return linhas
