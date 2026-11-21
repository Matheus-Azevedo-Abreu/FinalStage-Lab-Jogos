import configuracoes as cfg
import graficos
import painel
import menu
import fases
import pontuacao
import encerramento

# o que se vê depois da assinatura: a placa pronta, o resultado da noite, os
# créditos subindo e o ranking das cinco melhores noites, cada uma com a
# assinatura de quem a fez. só desenha; o tempo é do encerramento.py

u = menu.u

# quanto dura a troca da placa grande pela pequena e a saída do resultado
tempo_de_troca = 0.45
# quando o reflexo corre a placa, dentro da etapa "placa"
reflexo = (0.25, 1.15)


def nome_curto(indice):
    return fases.ANDARES[indice]["nome"].split(" ")[-1].upper()


def desenhar_placa_grande(tracos, opacidade):
    # a placa do tamanho em que foi assinada, com o reflexo passando por ela
    if opacidade <= 0:
        return
    x, y, largura, altura = menu.placa_de_assinar()
    chapa = graficos.ajustada("placa-leitura.png", largura, altura)
    if chapa is not None:
        graficos.desenhar_superficie(graficos.com_alfa(chapa, int(255 * opacidade)), x, y)
    if opacidade < 1:
        return
    ax, ay, al, aa = menu.area_de_assinar()
    menu.desenhar_tracos(tracos, ax, ay, al, aa, max(2, largura // 280))
    inicio, fim = reflexo
    if encerramento.etapa() == "placa" and inicio <= encerramento.tempo() <= fim:
        faixa = graficos.faixa_de_brilho(largura // 7, altura)
        avanco = (encerramento.tempo() - inicio) / (fim - inicio)
        graficos.desenhar_recortado(faixa, x - faixa.get_width() + int((largura + faixa.get_width()) * avanco), y,
                                    (x, y, largura, altura))


def desenhar_placa_pequena(tracos, opacidade, y):
    # a mesma placa, assinada, no alto da tela
    if opacidade <= 0:
        return
    largura, altura = u(192), u(64)
    x = (cfg.largura_tela - largura) // 2
    chapa = graficos.ajustada("placa-leitura.png", largura, altura)
    if chapa is not None:
        graficos.desenhar_superficie(graficos.com_alfa(chapa, int(255 * opacidade)), x, y)
    if opacidade >= 1:
        menu.desenhar_tracos(tracos, x + largura // 10, y + altura // 6, largura * 8 // 10, altura * 4 // 6, u(1))


def desenhar_linha_do_andar(indice, segundos, pontos, recorde, x, y, alfa):
    painel.rotulo("%02d" % (indice + 1), u(8), "titulo", x, y + u(4), "esquerda", alfa)
    painel.rotulo(nome_curto(indice), u(8), "titulo", x + u(22), y + u(4), "esquerda", alfa)
    painel.rotulo(painel.relogio(segundos), u(16), "numero", x + u(140), y, "direita", alfa, painel.cor_fala)
    painel.rotulo(painel.milhar(pontos), u(16), "numero", x + u(182), y, "direita", alfa)
    painel.rotulo(pontuacao.letra(pontos), u(8), "titulo", x + u(190), y + u(4), "esquerda", alfa)
    if recorde:
        marca = graficos.ajustada_superficie(graficos.marca_de_canal("losango"), cfg.escala_interface)
        graficos.desenhar_superficie(graficos.com_alfa(marca, alfa), x + u(202), y + u(4))


def texto_do_lugar(corrida, lugar):
    if corrida.get("partida", 0) != 0:
        return "NOITE PELA METADE: FORA DO RANKING"
    if lugar is None:
        return "FORA DOS CINCO DO RANKING"
    return "LUGAR %d NO RANKING" % lugar


def desenhar_resultado(corrida, recordes, lugar, opacidade, y):
    # o tempo e os pontos de cada andar, em duas colunas, entrando uma linha
    # por vez; embaixo, o total, a letra da noite e o lugar no ranking
    if opacidade <= 0:
        return
    alfa = int(255 * opacidade)
    andares = sorted(corrida["andares"].items())
    pontos = pontuacao.pontos_da_corrida(corrida)
    metade = (len(andares) + 1) // 2
    largura = min(cfg.largura_tela - u(16), u(470))
    altura = u(18 * metade + 76)
    x = (cfg.largura_tela - largura) // 2
    caixa = graficos.moldura(largura, altura, u(1), painel.cor_caixa, 226, painel.cor_fio)
    graficos.desenhar_superficie(graficos.com_alfa(caixa, alfa), x, y)
    for posicao, (indice, segundos) in enumerate(andares[:encerramento.linhas_gravadas()]):
        coluna, fila = divmod(posicao, metade)
        desenhar_linha_do_andar(indice, segundos, pontos[indice], indice in recordes,
                                x + u(12) + coluna * u(228), y + u(8) + fila * u(18), alfa)
    if not encerramento.letra_gravada():
        return
    soma, rank = pontuacao.resumo(corrida)
    base = y + u(8) + metade * u(18) + u(6)
    painel.rotulo("TEMPO", u(8), "titulo", x + u(12), base + u(9), "esquerda", alfa)
    painel.rotulo(painel.relogio(corrida["total"]), u(24), "numero", x + u(58), base, "esquerda", alfa, painel.cor_fala)
    painel.rotulo("PONTOS", u(8), "titulo", x + u(132), base + u(9), "esquerda", alfa)
    painel.rotulo(painel.milhar(soma), u(24), "numero", x + u(186), base, "esquerda", alfa)
    painel.rotulo("RANK", u(8), "titulo", x + largura - u(96), base + u(9), "esquerda", alfa)
    painel.rotulo(rank, u(48), "numero", x + largura - u(48), base - u(14), "esquerda", alfa)
    flagrantes = sum(corrida.get("deteccoes", {}).values())
    placas = len(corrida.get("placas", ()))
    resumo = "PLACAS LIDAS %d   FLAGRANTES %d   %s" % (placas, flagrantes, texto_do_lugar(corrida, lugar))
    painel.rotulo(resumo, u(8), "titulo", x + u(12), base + u(34), "esquerda", alfa)
    if "total" in recordes:
        painel.rotulo("MELHOR NOITE", u(8), "titulo", x + largura - u(12), base + u(34), "direita", alfa)


def desenhar_creditos(tracos):
    # o rolo sobe de baixo da tela; cada linha conforme o tipo
    meio = cfg.largura_tela // 2
    y = cfg.altura_tela + u(10) - int(encerramento.rolagem() * cfg.escala_interface)
    for tipo, texto in encerramento.creditos:
        altura = u(encerramento.alturas[tipo])
        if -altura < y < cfg.altura_tela:
            if tipo == "titulo":
                menu.desenhar_titulo("titulo-final-stage.png", "FINAL STAGE", y)
            elif tipo == "papel":
                painel.rotulo(texto, u(8), "titulo", meio, y + u(12), "centro")
            elif tipo == "nome":
                painel.rotulo(texto, u(16), "numero", meio, y, "centro", 255, painel.cor_fala)
            elif tipo == "assinatura":
                menu.desenhar_tracos(tracos, meio - u(90), y + u(2), u(180), u(48), u(1))
        y = y + altura


def desenhar_encerramento(corrida, recordes, tracos, lugar, relogio_da_tela):
    # as três etapas sobre a cidade vista da cobertura; nos créditos, o céu
    # começa a clarear
    etapa, tempo = encerramento.etapa(), encerramento.tempo()
    graficos.desenhar_cobrindo("fundo-10.png")
    if etapa == "creditos":
        nivel = int(12 * encerramento.fracao())
        if nivel > 0:
            graficos.desenhar_superficie(graficos.aurora(nivel), 0, int(cfg.altura_tela * 0.34))
    graficos.desenhar_superficie(graficos.veu(150 if etapa == "placa" else 176), 0, 0)
    troca = min(1.0, tempo / tempo_de_troca)
    if etapa == "placa":
        desenhar_placa_grande(tracos, 1.0)
    elif etapa == "resultado":
        desenhar_placa_grande(tracos, 1.0 - troca)
        desenhar_placa_pequena(tracos, troca, u(10))
        letreiro = graficos.interface("titulo-concluido.png")
        if letreiro is not None:
            graficos.desenhar_superficie(graficos.com_alfa(letreiro, int(255 * troca)),
                                         (cfg.largura_tela - letreiro.get_width()) // 2, u(80))
        desenhar_resultado(corrida, recordes, lugar, troca, u(124))
    else:
        desenhar_placa_pequena(tracos, 1.0 - troca, u(10))
        desenhar_resultado(corrida, recordes, lugar, 1.0 - troca, u(124))
        desenhar_creditos(tracos)
    if tempo > encerramento.guarda and int(relogio_da_tela * 2) % 2 == 0:
        painel.rotulo("ESPAÇO AVANÇA   ·   ESC PULA", u(8), "titulo", cfg.largura_tela - u(10),
                      cfg.altura_tela - u(16), "direita", 150)


def desenhar_chapa(posicao, linha, x, y, destaque, relogio_da_tela):
    # um lugar do ranking: o número, a assinatura, os pontos, a letra e o tempo
    chapa = graficos.interface("placa-ranking.png")
    if chapa is not None:
        graficos.desenhar_superficie(graficos.com_alfa(chapa, 255 if linha is not None else 120), x, y)
    painel.gravado(str(posicao), u(32), "numero", x + u(36), y + u(11), "esquerda", 255 if linha is not None else 120)
    if linha is None:
        return
    menu.desenhar_tracos(linha.get("assinatura", []), x + u(62), y + u(8), u(146), u(40), u(1))
    painel.gravado(painel.milhar(linha["pontos"]), u(32), "numero", x + u(350), y + u(4), "direita")
    detalhe = "%s   %s" % (linha.get("rank", "?"), painel.relogio(linha.get("tempo", 0)))
    painel.gravado(detalhe, u(8), "titulo", x + u(350), y + u(38), "direita")
    if destaque and int(relogio_da_tela * 3) % 2 == 0:
        painel.rotulo(">", u(16), "titulo", x - u(16), y + u(18))
        painel.rotulo("<", u(16), "titulo", x + u(menu.largura_da_chapa) + u(6), y + u(18))


def desenhar_ranking(placar, destaque, mouse, relogio_da_tela):
    # as cinco melhores noites, da melhor para a pior; destaque é o lugar da
    # noite que acabou de terminar, ou None
    graficos.desenhar_nitida("menu-fundo.png", 0.6)
    menu.desenhar_chuva()
    graficos.desenhar_superficie(graficos.veu(190), 0, 0)
    topo, vao = menu.geometria_do_ranking()
    menu.desenhar_titulo("titulo-ranking.png", "RANKING", u(topo))
    x = (cfg.largura_tela - u(menu.largura_da_chapa)) // 2
    for n in range(menu.lugares_do_ranking):
        y = u(topo + 27 + vao + n * (menu.altura_da_chapa + vao))
        linha = placar[n] if n < len(placar) else None
        desenhar_chapa(n + 1, linha, x, y, destaque == n + 1, relogio_da_tela)
    if not placar:
        painel.rotulo("NINGUÉM ASSINOU AINDA. A PRIMEIRA NOITE INTEIRA ENTRA AQUI.", u(8), "titulo",
                      cfg.largura_tela // 2, u(topo + 27 + vao) - u(2) + u(menu.altura_da_chapa) // 2 - u(4), "centro")
    menu.desenhar_botoes("ranking", mouse)
    menu.desenhar_cursor("ranking", mouse)
