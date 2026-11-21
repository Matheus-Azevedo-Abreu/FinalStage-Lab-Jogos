import json
import math
import os
import configuracoes as cfg
import documentos

# o que fica guardado entre uma noite e outra: o andar em curso, o melhor
# tempo de cada andar e da corrida inteira, e se o som está mudo. não
# importa pygame. arquivo estragado ou ausente vale como começo do zero

# caderno: as pistas lidas na noite em curso, [andar, pista], para quem continua depois
dados = {"andar": 0, "melhores": {}, "melhor_total": None, "mudo": False, "caderno": []}


def carregar():
    try:
        with open(cfg.arquivo_progresso, encoding="utf-8") as arquivo:
            lido = json.load(arquivo)
    except (OSError, ValueError):
        return
    if not isinstance(lido, dict):
        return
    if isinstance(lido.get("andar"), int):
        dados["andar"] = max(0, lido["andar"])
    if isinstance(lido.get("melhores"), dict):
        # o json só guarda chave de texto: o índice do andar volta a ser número
        dados["melhores"] = {int(k): float(v) for k, v in lido["melhores"].items()
                             if str(k).isascii() and str(k).isdigit() and tempo_valido(v)}
    if tempo_valido(lido.get("melhor_total")):
        dados["melhor_total"] = float(lido["melhor_total"])
    dados["mudo"] = lido.get("mudo") is True
    if isinstance(lido.get("caderno"), list):
        dados["caderno"] = [[e[0], e[1]] for e in lido["caderno"] if entrada_valida(e)]


def entrada_valida(entrada):
    # [andar, nome de uma pista que existe]
    return (isinstance(entrada, list) and len(entrada) == 2 and isinstance(entrada[0], int)
            and not isinstance(entrada[0], bool) and isinstance(entrada[1], str) and entrada[1] in documentos.pistas)


def guardar_caderno(entradas):
    dados["caderno"] = [[andar, nome] for andar, nome in entradas if isinstance(andar, int)]
    salvar()


def caderno_ate(indice):
    # o que a noite em curso já tinha lido antes do andar dado
    return [(andar, nome) for andar, nome in dados["caderno"] if andar < indice]


def tempo_valido(valor):
    # número de verdade: nan e infinito, que o json do python aceita, não
    return isinstance(valor, (int, float)) and not isinstance(valor, bool) and math.isfinite(valor) and valor >= 0


def gravar_inteiro(caminho, conteudo):
    # escreve ao lado e troca no fim: uma queda no meio não zera o arquivo.
    # disco cheio ou pasta sem permissão não derruba o jogo
    try:
        with open(caminho + ".tmp", "w", encoding="utf-8") as arquivo:
            json.dump(conteudo, arquivo, indent=1)
        os.replace(caminho + ".tmp", caminho)
    except OSError:
        pass


def salvar():
    gravar_inteiro(cfg.arquivo_progresso, dados)


def chegar(indice):
    # o andar em que a corrida está; o menu oferece continuar a partir dele
    dados["andar"] = indice
    salvar()


def anotar_andar(indice, segundos):
    # devolve True quando o tempo é o melhor já feito no andar
    melhor = dados["melhores"].get(indice)
    if melhor is not None and segundos >= melhor:
        return False
    dados["melhores"][indice] = segundos
    salvar()
    return True


def anotar_corrida(segundos):
    # só a corrida que saiu do andar 1; devolve True quando é o melhor total
    dados["andar"] = 0
    recorde = dados["melhor_total"] is None or segundos < dados["melhor_total"]
    if recorde:
        dados["melhor_total"] = segundos
    salvar()
    return recorde


def guardar_mudo(mudo):
    dados["mudo"] = mudo
    salvar()
