# as falas do jogo (docs/historia.md). só texto: quem fala, o retrato e a
# linha. quem: "selene" (a voz no rádio), "iris" ou None (legenda, sem
# retrato). retratos da íris: neutra, atenta, cansada, desconfiada,
# indecifravel. a selene nunca dá a solução, nunca mente e só diz o nome
# da íris na última fala

# abertura: a calçada, o rádio liga, as regras em quatro linhas
abertura = [
    (None, None, "Vértice. Sétima etapa. A última não é entrevista."),
    ("selene", None, "Boa noite. Aqui é Selene Amparo, coordenadora do seu processo. Você me ouve bem?"),
    ("iris", "atenta", "Ouço."),
    ("selene", None, "A etapa final é prática. No topo do prédio há um diamante. Suba até a cobertura e pegue."),
    ("selene", None, "A segurança fica ligada. Não consigo desligar sem deixar registro."),
    ("selene", None, "Se uma câmera vir você por um segundo inteiro, o andar recomeça. Ninguém é eliminado."),
    ("selene", None, "O tempo é anotado. Não elimina. É só anotado."),
    ("iris", "desconfiada", "E quem montou os andares?"),
    ("selene", None, "Pode entrar quando quiser."),
]

# rádio ao entrar no andar, um sim e outro não; índice do andar -> linha
radio_do_andar = {
    0: "A recepção é só a recepção. Vá no seu ritmo.",
    2: "A Adélia achava que uma alavanca só não ia bastar. Pôs várias, e corrigiu cada uma.",
    4: "A Noemi dizia que o prédio não é sobre chegar. É sobre refazer.",
    6: "O Aníbal desenhou o prédio inteiro numa parede. Inclusive os andares que ainda não existem.",
    8: "As portas do Otávio não contam segundos. Contam você.",
}

# nos outros andares a íris conta os passos em voz baixa; na cobertura, para
andares_de_contagem = (1, 3, 5, 7)

# flagrante da câmera: uma por vez, em rodízio
deteccao = [
    "A segurança está subindo. Eles acompanham você até a entrada do andar.",
    "Um segundo inteiro. É o que a câmera precisa.",
    "Sem problema. A noite só fica mais longa.",
    "Anotado. Pode recomeçar.",
]

# a íris diante da placa, na primeira leitura; índice do andar -> fala
placas = {
    1: ("iris", "neutra", "Benedito Prado, dois mil e nove. Alguém assinou o andar."),
    3: ("iris", "desconfiada", "Prado. Ferraz. Vieira. Os sobrenomes são todos coisas."),
    5: ("iris", "atenta", "Selene Amparo."),
    8: ("iris", "cansada", "Cada um deixou um andar. É essa a vaga."),
    9: ("iris", "indecifravel", "Em branco."),
}

# andar 4: a primeira vez que o eco aparece
primeiro_eco = ("iris", "desconfiada", "Essa sou eu.")

# andar 6: parada diante da placa da selene, ela muda de assunto
mudanca_de_assunto = ("selene", None, "O tempo continua sendo anotado.")
andar_da_selene = 5

# treino: a lição de cada sala, título e texto, na ordem em que o prédio
# apresenta os mecanismos. curta: cabe em três linhas no alto da tela
licoes = {
    "mover": ("ANDAR E PULAR", "A e D, ou as setas, andam. ESPAÇO pula: a Íris sobe até dois blocos e cruza um vão "
              "de até quatro. R recomeça o andar sem castigo: o tempo só continua correndo."),
    "botao": ("BOTÃO", "Qualquer peso em cima abre a porta da mesma marca dourada. Saiu de cima, ela fecha 3 "
              "segundos depois: cada quadrado rosa sobre a porta é um segundo que resta."),
    "alavanca": ("ALAVANCA", "Encoste nela e aperte E. A porta da mesma marca abre e fica aberta até a alavanca "
                 "voltar. Luz vermelha é desligada; verde, ligada."),
    "gaveta": ("GAVETA", "E ao lado puxa a gaveta, que vira degrau. A mola a fecha sozinha em 3 segundos, mesmo "
               "com você em cima. Puxar de novo dá corda outra vez."),
    "viga": ("VIGA DE FERRO", "A alavanca manda a viga para o lugar tracejado na parede; puxada de novo, a viga "
             "volta. Ela espera se você estiver em cima ou no caminho. Com duas marcas, obedece a duas "
             "alavancas, e uma desfaz a outra."),
    "eco": ("ECO", "No porta-retratos, E grava 6 segundos do que você fizer. Depois você volta ao começo e o eco "
            "repete tudo uma vez: ele pesa em botão e segura porta. Esta porta pede os dois botões juntos; "
            "cada pino verde é um que já vale."),
    "esteira": ("ESTEIRA", "O chão leva no sentido das setas. Pular a favor soma o embalo e cruza um vão de seis; "
                "contra as setas, você não sai do lugar. Caiu no vão? O degrau devolve à esteira."),
    "caixa": ("CAIXA", "Ande contra ela para empurrar: desliza um bloco por vez. É degrau para muro de três, pesa "
              "em botão, cai da borda e empilha. A câmera vê através dela."),
    "camera": ("CÂMERA", "O cone é o que ela vê. Um segundo inteiro dentro dele e o andar recomeça. Parede e porta "
               "fechada cortam o cone; logo abaixo da câmera há um ponto cego. A alavanca da mesma marca a "
               "desliga."),
    "invertida": ("PORTA INVERTIDA", "Marca riscada funciona ao contrário: a porta fica aberta com a alavanca "
                  "desligada e fecha quando ela liga. Puxe para ver, e puxe de novo para passar."),
    "passos": ("PORTA DE PASSOS", "O botão abre, e a porta fecha depois de tantos passos seus: o número sobre "
               "ela é quantos restam. Parada, você não gasta passo; um pulo vale três."),
    "segredo": ("PISTA E SEGREDO", "O brilho marca uma pista: E lê, e ela fica no caderno (C). Saída de luz vermelha "
                "está trancada. Na tranca, A e D escolhem a roda, W e S giram e ENTER confere. No prédio, o "
                "segredo se deduz do que o autor de cada andar deixou."),
}

# final: o diamante na mão, sem rádio até ele ser tocado
final = [
    (None, None, "O diamante é pequeno. Ela esperava que fosse pesado."),
    ("selene", None, "Processo concluído. Parabéns. Digo isso com sinceridade."),
    ("selene", None, "A documentação fica disponível na segunda-feira."),
    ("selene", None, "O primeiro entregável já tem prazo: o décimo primeiro andar, até o fim do ano."),
    ("iris", "indecifravel", "..."),
    ("selene", None, "Íris, você já pensou em como quer ser gravada?"),
]


def contagem(passos):
    # a linha em que a íris conta: os dois últimos passos dados
    return ("iris", "neutra", "...%d, %d." % (passos - 1, passos))
