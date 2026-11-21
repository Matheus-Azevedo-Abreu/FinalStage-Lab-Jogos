# a assinatura da tela final: os traços que a jogadora grava na placa com o
# mouse. só guarda os pontos, em frações do tamanho da placa, para valerem em
# qualquer tela; não desenha e não importa pygame

# cada traço é uma lista de pontos (x, y), de 0 a 1 dentro da placa
tracos = []

# se o botão estava apertado no quadro anterior, e o último ponto guardado
pena = {"apertada": False}

# distância mínima entre dois pontos de um traço, em fração da largura
passo_minimo = 0.004


def limpar():
    tracos[:] = []
    pena["apertada"] = False


def vazia():
    return not any(len(traco) > 1 for traco in tracos)


def gravar(x, y, apertada):
    # um quadro: x e y em frações da placa. devolve True se a ponta riscou
    dentro = 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0
    riscou = False
    if apertada and dentro:
        if not pena["apertada"]:
            tracos.append([(x, y)])
        else:
            ultimo = tracos[-1][-1]
            if abs(x - ultimo[0]) + abs(y - ultimo[1]) >= passo_minimo:
                tracos[-1].append((x, y))
                riscou = True
    pena["apertada"] = apertada and dentro
    return riscou


def para_guardar(limite=500):
    # os traços enxutos para o ranking: no máximo tantos pontos ao todo,
    # tirados por igual de cada traço, sempre com o primeiro e o último
    bons = [traco for traco in tracos if len(traco) > 1]
    total = sum(len(traco) for traco in bons)
    salto = max(1, -(-total // limite))
    return [traco[:-1:salto] + [traco[-1]] for traco in bons]
