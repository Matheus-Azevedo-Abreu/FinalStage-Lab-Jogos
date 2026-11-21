import configuracoes as cfg
import jogador
import dialogo
import roteiro
import documentos

# quando a história fala: decide, pelo estado do jogo, que linha entra no
# rádio e se a íris está lendo a placa do andar. nunca altera o jogo e não
# importa pygame. a regra é falar na entrada do andar e calar no puzzle

# o que já foi dito nesta corrida, para nada se repetir quando o andar recomeça
dito = {"andares": set(), "placas": set(), "selene_mudou": False, "deteccoes": 0, "eco": False}

# a placa diante da íris: há quanto tempo ela lê, se acabou de chegar e
# quanto da placa grande aparece (entra e sai em 0,15 s)
leitura = {"lendo": False, "tempo": 0.0, "chegou": False, "opacidade": 0.0}


def reiniciar():
    # corrida nova
    dito["andares"] = set()
    dito["placas"] = set()
    dito["selene_mudou"] = False
    dito["deteccoes"] = 0
    dito["eco"] = False
    leitura["lendo"] = False
    leitura["tempo"] = 0.0
    leitura["opacidade"] = 0.0
    dialogo.calar()


def entrar(indice, passos):
    # uma linha só, na primeira vez em cada andar: rádio ou contagem
    if indice in dito["andares"]:
        return
    if indice in roteiro.andares_de_contagem and passos < 2:
        # a noite que começa neste andar: a íris conta quando houver o que contar
        return
    dito["andares"].add(indice)
    if indice in roteiro.radio_do_andar:
        dialogo.avisar(("selene", None, roteiro.radio_do_andar[indice]))
    elif indice in roteiro.andares_de_contagem:
        dialogo.avisar(roteiro.contagem(passos))


def detectar():
    dialogo.calar()
    linha = roteiro.deteccao[dito["deteccoes"] % len(roteiro.deteccao)]
    dito["deteccoes"] = dito["deteccoes"] + 1
    dialogo.avisar(("selene", None, linha))


def abrir_tranca(enigma):
    # a tranca cedeu: a íris diz em voz baixa o que entendeu do autor do andar
    fala = documentos.enigmas[enigma]["fala"]
    if fala is not None:
        dialogo.avisar(fala)


def dar_dica(enigma):
    # depois de alguns erros, a íris pensa alto: o que juntar, não a resposta
    dica = documentos.enigmas[enigma]["dica"]
    if dica is not None:
        dialogo.avisar(("iris", "atenta", dica))


def diante_da_placa(fase):
    # parada no chão, com o meio do corpo perto do meio da placa: passar
    # andando não é ler
    placa = fase["placa"]
    if placa is None or not jogador.no_chao or jogador.vx != 0:
        return False
    meio = jogador.x + cfg.largura_jogador / 2
    perto = abs(meio - (placa[0] + cfg.tile / 2)) <= cfg.alcance_placa
    return perto and abs(jogador.y + cfg.altura_jogador - (placa[1] + 3 * cfg.tile)) < 1


def ler_placa(indice, passo):
    # a primeira leitura rende uma fala; diante da placa da selene, se a
    # íris fica, a selene muda de assunto
    leitura["tempo"] = leitura["tempo"] + passo
    if indice not in dito["placas"]:
        dito["placas"].add(indice)
        if indice in roteiro.placas:
            dialogo.avisar(roteiro.placas[indice])
    demorou = leitura["tempo"] >= cfg.espera_na_placa
    if indice == roteiro.andar_da_selene and demorou and not dito["selene_mudou"]:
        dito["selene_mudou"] = True
        dialogo.avisar(roteiro.mudanca_de_assunto)


def atualizar(passo, fase, indice, passos, sinais):
    # um quadro de jogo correndo
    entrar(indice, passos)
    if "detectada" in sinais:
        detectar()
    if "eco_toca" in fase["eventos"] and not dito["eco"]:
        # a íris se vê repetindo o que fez
        dito["eco"] = True
        dialogo.avisar(roteiro.primeiro_eco)
    lendo = diante_da_placa(fase)
    leitura["chegou"] = lendo and not leitura["lendo"]
    leitura["lendo"] = lendo
    if lendo:
        ler_placa(indice, passo)
    else:
        leitura["tempo"] = 0.0
    sentido = 1 if lendo else -1
    leitura["opacidade"] = max(0.0, min(1.0, leitura["opacidade"] + sentido * passo / 0.15))
    dialogo.atualizar_aviso(passo)


def opacidade_da_placa():
    return leitura["opacidade"]
