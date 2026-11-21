import json
import time
import configuracoes as cfg
import progresso

# pontos e letra de cada andar e da noite inteira, a partir do tempo do
# cronômetro, dos flagrantes da câmera e das placas lidas, e o ranking
# guardado em arquivo, com a assinatura de quem fez cada noite. as pistas
# lidas somam e os segredos errados descontam: a investigação também é anotada.
# não importa pygame. tempo é pontuação, nunca derrota: a pior letra é d

# tempo do roteiro de solução de cada andar, em segundos: o piso de quem já
# sabe a resposta. testes/testar_andares.py confere esta lista com o medido
referencia = [9.1, 14.6, 27.4, 23.7, 10.3, 21.9, 21.4, 24.6, 37.3, 5.0]

# até tantas vezes o tempo do roteiro o andar vale os pontos cheios; daí em
# diante, caem na proporção do tempo. cada flagrante custa a multa
pontos_cheios = 1000
folga = 1.5
multa = 150
# ler a placa do autor do andar soma isto: a história também pontua
bonus_da_placa = 50
# cada pista lida soma isto; cada segredo errado confirmado na tranca custa a multa
bonus_da_pista = 25
multa_do_erro = 30
# letra e o mínimo de pontos: s só sem flagrante (1,67 vez o roteiro), a até
# 2,5 vezes, b até 4, c até 6
faixas = (("S", 900), ("A", 600), ("B", 375), ("C", 250))
# o ranking guarda as cinco melhores noites
lugares = 5


def pontos_do_andar(indice, segundos, flagrantes=0, placa=False, pistas=0, erros=0):
    # o treino (índice de texto) e andar fora da lista não pontuam
    if not isinstance(indice, int) or indice >= len(referencia) or segundos <= 0:
        return 0
    cheios = pontos_cheios * min(1.0, folga * referencia[indice] / segundos)
    pelo_tempo = max(0, round(cheios) - multa * flagrantes - multa_do_erro * erros)
    return pelo_tempo + (bonus_da_placa if placa else 0) + bonus_da_pista * pistas


def letra(pontos):
    for nome, minimo in faixas:
        if pontos >= minimo:
            return nome
    return "D"


def pontos_da_corrida(corrida):
    # pontos de cada andar jogado, pelo índice
    flagrantes = corrida.get("deteccoes", {})
    placas = corrida.get("placas", ())
    erros = corrida.get("erros", {})
    lidas = [andar for andar, _ in corrida.get("caderno", ())]
    return {indice: pontos_do_andar(indice, segundos, flagrantes.get(indice, 0), indice in placas,
                                    lidas.count(indice), erros.get(indice, 0))
            for indice, segundos in corrida["andares"].items()}


def resumo(corrida):
    # soma dos pontos e a letra da noite, que é a da média dos andares jogados
    pontos = pontos_da_corrida(corrida)
    soma = sum(pontos.values())
    return soma, letra(soma / max(1, len(pontos)))


def ler_placar():
    # arquivo estragado ou ausente vale como placar vazio
    try:
        with open(cfg.arquivo_placar, encoding="utf-8") as arquivo:
            lido = json.load(arquivo)
    except (OSError, ValueError):
        return []
    if not isinstance(lido, list):
        return []
    bons = [linha for linha in lido if isinstance(linha, dict) and isinstance(linha.get("pontos"), int)]
    for linha in bons:
        if not progresso.tempo_valido(linha.get("tempo")):
            linha["tempo"] = 0.0
        # ranking de antes das assinaturas, ou assinatura estragada: em branco
        if not tracos_validos(linha.get("assinatura")):
            linha["assinatura"] = []
    return bons[:lugares]


def tracos_validos(tracos):
    # lista de traços, cada um uma lista de pares de números
    if not isinstance(tracos, list):
        return False
    for traco in tracos:
        if not isinstance(traco, list):
            return False
        for ponto in traco:
            if not (isinstance(ponto, list) and len(ponto) == 2 and
                    all(isinstance(v, (int, float)) for v in ponto)):
                return False
    return True


def registrar(corrida, assinatura=()):
    # só a noite inteira entra no ranking, com a assinatura de quem a fez
    # (traços em frações da placa); devolve o lugar dela (1 é o primeiro),
    # ou None quando ficou fora dos que o arquivo guarda
    soma, rank = resumo(corrida)
    nova = {"pontos": soma, "rank": rank, "tempo": round(corrida["total"], 1),
            "flagrantes": sum(corrida.get("deteccoes", {}).values()),
            "placas": len(corrida.get("placas", ())),
            "pistas": len(corrida.get("caderno", ())),
            "data": time.strftime("%Y-%m-%d %H:%M"),
            "assinatura": [[[round(x, 3), round(y, 3)] for x, y in traco] for traco in assinatura]}
    placar = ler_placar() + [nova]
    placar.sort(key=lambda linha: (-linha["pontos"], linha.get("tempo", 0)))
    lugar = [linha is nova for linha in placar].index(True) + 1
    progresso.gravar_inteiro(cfg.arquivo_placar, placar[:lugares])
    return lugar if lugar <= lugares else None
