# inicialização do jogo:
# .venv/bin/python main.py

import os
import time
import pygame
from PPlay.window import Window
from PPlay.keyboard import Keyboard
import configuracoes as cfg
import fases
import graficos
import jogo
import desenho
import menu
import painel
import transicao
import efeitos
import som
import progresso
import pontuacao
import dialogo
import narrativa
import roteiro
import assinatura
import encerramento
import epilogo
import jogador
import investigacao
import leitura

# a tela inteira, na resolução dela: sem faixa preta em volta. sem vídeo de
# verdade (testes e prévias), fica o padrão de configuracoes
pygame.display.init()
tela_real = os.environ.get("SDL_VIDEODRIVER") != "dummy"
if cfg.tela_cheia and tela_real:
    cfg.ajustar_tela(*pygame.display.get_desktop_sizes()[0])

# janela - tem que vir antes de qualquer sprite, senão convert_alpha quebra
janela = Window(cfg.largura_tela, cfg.altura_tela)
janela.set_title(cfg.titulo)
sincronia = False
if cfg.tela_cheia and tela_real:
    # a pplay abre janela; aqui ela vira tela cheia, e a pplay continua
    # copiando a tela virtual, do mesmo tamanho, para ela. com sincronia
    # vertical a troca de quadro espera o monitor, e a imagem não rasga
    try:
        janela.real_screen = pygame.display.set_mode((cfg.largura_tela, cfg.altura_tela),
                                                     pygame.FULLSCREEN | pygame.SCALED, vsync=1)
        sincronia = True
    except pygame.error:
        janela.real_screen = pygame.display.set_mode((cfg.largura_tela, cfg.altura_tela), pygame.FULLSCREEN)

# teclado e mouse
teclado = Keyboard()
mouse = janela.mouse

# ritmo do laço, medido em segundos: o relógio da pplay conta milissegundos
# inteiros, e o tick(60) do pygame dorme além do pedido no macos
ritmo = {"antes": time.perf_counter(), "proximo": time.perf_counter(), "monitor": None}


def medir_monitor():
    # com sincronia, o tempo entre duas trocas de quadro é o do monitor;
    # devolve esse período, ou None quando a troca não espera por ele
    tempos = []
    for _ in range(14):
        antes = time.perf_counter()
        pygame.display.flip()
        tempos.append(time.perf_counter() - antes)
    periodo = sorted(tempos[4:])[len(tempos[4:]) // 2]
    return periodo if 1 / 250 < periodo < 1 / 45 else None


if sincronia:
    ritmo["monitor"] = medir_monitor()

# arte, carregada de uma vez só depois da janela
graficos.carregar([nome for nome, _, _ in cfg.arte.values()])
graficos.carregar_escurecidas([a["fundo"] for a in fases.ANDARES] + [fases.TREINO["fundo"]], cfg.escurecer_fundo)
graficos.carregar_escurecidas(["divisoria.png", "divisoria-pe.png"], cfg.escurecer_coluna)
graficos.carregar_tiras(cfg.animacoes)
graficos.carregar_tiras(cfg.efeitos)
graficos.carregar(menu.arquivos())
graficos.carregar(leitura.arquivos())
for indice in list(range(len(fases.ANDARES))) + [fases.treino]:
    desenho.preparar(fases.carregar(indice))
menu.preparar_cursor()
menu.preparar_textos()

# progresso guardado, som e a faixa ambiente, que não para mais
progresso.carregar()
som.preparar()
som.definir_mudo(progresso.dados["mudo"])
som.tocar_musica()

# aviso no terminal quando algum png não está na pasta. o jogo continua
# rodando: o que falta vira bloco de cor
for ausente in graficos.faltando():
    print("faltando em assets:", ausente)

# tela em curso: "menu", "controles", "ranking", "abertura", "jogo", "pausa",
# "final", "assinatura" ou "encerramento"
estado = "menu"
jogo.carregar_andar(0)

# o que a tela guarda: há quanto tempo está aberta, a cortina que clareia
# na troca, o botão sob o mouse, os recordes desta corrida e por quanto
# tempo ainda aparece o aviso de som ligado ou desligado
tela = {"relogio": 0.0, "cortina": cfg.tempo_cortina, "foco": None, "recordes": set(), "aviso_de_som": 0.0,
        "riscando": False, "risco": 0.0}
# o que o andar que acabou rendeu, para o cartão de passagem; por quanto
# tempo ainda aparece o aviso da placa lida; a lição do treino na tela e o
# quanto ela já apareceu; o ranking lido do arquivo e o lugar a destacar
tela.update({"resultado": None, "bonus": 0.0, "licao": None, "licao_tempo": 0.0, "placar": [], "destaque": None})
# o que o aviso de pontos diz: None é a placa lida
tela["aviso"] = None

# controle de tecla da depuração
p_solto = True
numero_solto = True
capturas = 0


def teclas_de_depuracao():
    # 1 a 9 pulam de andar, P salva a tela; só com cfg.depuracao
    global p_solto, numero_solto, capturas
    algum_numero = False
    for numero in range(1, min(9, len(fases.ANDARES)) + 1):
        if teclado.key_pressed(str(numero)):
            algum_numero = True
            if numero_solto:
                jogo.carregar_andar(numero - 1)
    numero_solto = not algum_numero

    if teclado.key_pressed("P"):
        if p_solto:
            capturas = capturas + 1
            graficos.capturar(os.path.join(cfg.base, "captura-%d.png" % capturas))
        p_solto = False
    else:
        p_solto = True


def comecar(indice):
    # corrida nova a partir do andar dado: tempo zerado, e o cartão antes de clarear
    jogo.nova_corrida(indice)
    # quem continua a noite fica com o caderno do que já tinha lido
    jogo.corrida["caderno"] = progresso.caderno_ate(indice)
    progresso.guardar_caderno(jogo.corrida["caderno"])
    narrativa.reiniciar()
    tela["recordes"] = set()
    tela["resultado"] = None
    tela["bonus"] = 0.0
    tela["licao"] = None
    jogo.carregar_andar(indice)
    transicao.iniciar(indice, escurecer=False)
    progresso.chegar(indice)


def comecar_treino():
    # o treino fica fora da noite: não grava progresso, recorde nem placar
    jogo.nova_corrida(fases.treino)
    narrativa.reiniciar()
    tela["recordes"] = set()
    tela["resultado"] = None
    tela["licao"] = None
    jogo.carregar_andar(fases.treino)
    transicao.iniciar(fases.treino, escurecer=False)


def sair_do_treino():
    dialogo.calar()
    som.parar("alerta")
    som.tocar("saida")


def passar(tempo):
    # com a transição em curso o jogo fica parado; no escuro, troca o andar
    destino = transicao.atualizar(tempo)
    if destino is not None:
        jogo.carregar_andar(destino)


def ouvir_falas():
    # o rádio abrindo e fechando, e a voz de quem fala, letra a letra
    for evento in dialogo.eventos:
        if evento == "abre":
            som.tocar("radio-abre")
        elif evento == "fecha":
            som.tocar("radio-fecha")
        elif evento.startswith("voz:"):
            som.tocar("voz-" + evento[4:])


def anotar_andar():
    # o tempo do andar que acabou; melhor tempo vira losango na placa final
    indice = jogo.andar["indice"]
    if progresso.anotar_andar(indice, jogo.corrida["andares"].get(indice, 0.0)):
        tela["recordes"].add(indice)


def pontos_guardados():
    # os pontos dos andares já vencidos nesta corrida: o que a hud mostra
    pontos = pontuacao.pontos_da_corrida(jogo.corrida)
    return sum(valor for indice, valor in pontos.items() if indice != jogo.andar["indice"])


def resultado_do_andar():
    # o que o andar que acabou rendeu: índice, tempo, pontos e letra
    indice = jogo.andar["indice"]
    pontos = pontuacao.pontos_da_corrida(jogo.corrida).get(indice, 0)
    return indice, jogo.corrida["andares"].get(indice, 0.0), pontos, pontuacao.letra(pontos)


def anotar_placa():
    # a placa do autor lida pela primeira vez nesta corrida soma pontos
    indice = jogo.andar["indice"]
    if indice in narrativa.dito["placas"] and indice not in jogo.corrida["placas"]:
        jogo.corrida["placas"].add(indice)
        tela["bonus"] = cfg.tempo_do_bonus
        tela["aviso"] = None


def anotar_investigacao(na_noite):
    # a pista nova entra no caderno e soma pontos; a tranca que cede rende
    # uma fala da íris
    if "pista_nova" in jogo.sinais and na_noite:
        tela["bonus"] = cfg.tempo_do_bonus
        tela["aviso"] = "PISTA ANOTADA  +%d" % cfg.bonus_da_pista_mostrado
        progresso.guardar_caderno(jogo.corrida["caderno"])
    if jogo.andar["abriu"] is not None:
        narrativa.abrir_tranca(jogo.andar["abriu"])
    if "tranca_erro" in jogo.sinais:
        tranca = investigacao.aberto["tranca"]
        if tranca["erros"] == cfg.erros_para_a_dica:
            narrativa.dar_dica(tranca["enigma"])


def acompanhar_licao(tempo):
    # treino: a lição da sala em que a íris está; ao trocar de sala, a nova
    # entra do zero
    licao = fases.licao_em(jogo.andar["fase"], jogador.x + cfg.largura_jogador / 2)
    nome = licao[1] if licao is not None else None
    if nome != tela["licao"]:
        tela["licao"] = nome
        tela["licao_tempo"] = 0.0
    tela["licao_tempo"] = tela["licao_tempo"] + tempo


def sair_do_andar():
    anotar_andar()
    tela["resultado"] = resultado_do_andar()
    dialogo.calar()
    som.parar("alerta")
    som.tocar("saida")
    progresso.chegar(jogo.andar["indice"] + 1)
    transicao.iniciar(jogo.andar["indice"] + 1)


def pegar_diamante():
    # o fim: só a corrida que saiu do andar 1 disputa o melhor total
    anotar_andar()
    dialogo.calar()
    som.tocar("diamante")
    menu.situacao["lugar"] = None
    if jogo.corrida["partida"] == 0:
        if progresso.anotar_corrida(jogo.corrida["total"]):
            tela["recordes"].add("total")
    else:
        progresso.chegar(0)
    dialogo.iniciar(roteiro.final)


def concluir_noite():
    # a placa está assinada: a noite que partiu do andar 1 entra no ranking,
    # com a assinatura, e começa o encerramento
    if jogo.corrida["partida"] == 0:
        menu.situacao["lugar"] = pontuacao.registrar(jogo.corrida, assinatura.para_guardar())
    encerramento.iniciar(len(jogo.corrida["andares"]))
    som.tocar("placa")


def atualizar_jogo(tempo):
    # um quadro de jogo; devolve a tela seguinte: "final" quando a íris pega
    # o diamante, "menu" quando ela sai do treino
    if transicao.ativa():
        passar(tempo)
        return "jogo"
    # com pista, tranca ou caderno aberto o tempo não é anotado
    if not jogo.em_modal():
        jogo.anotar(tempo)
    desfecho = jogo.atualizar(tempo, teclado)
    anotar_investigacao(jogo.andar["indice"] != fases.treino)
    som.ouvir(efeitos.eventos + jogo.sinais + jogo.andar["fase"]["eventos"])
    narrativa.atualizar(tempo, jogo.andar["fase"], jogo.andar["indice"], jogo.corrida["passos"], jogo.sinais)
    ouvir_falas()
    if narrativa.leitura["chegou"]:
        som.tocar("placa")
    if cfg.depuracao and not jogo.em_modal():
        teclas_de_depuracao()
    tela["bonus"] = max(0.0, tela["bonus"] - tempo)
    if jogo.andar["indice"] == fases.treino:
        acompanhar_licao(tempo)
        if desfecho == "saida":
            sair_do_treino()
            return "menu"
        return "jogo"
    anotar_placa()
    ultimo = jogo.andar["indice"] + 1 >= len(fases.ANDARES)
    if desfecho == "diamante" or (desfecho == "saida" and ultimo):
        pegar_diamante()
        return "final"
    if desfecho == "saida":
        sair_do_andar()
    return "jogo"


def assinar():
    # a jogadora grava o nome na placa com o mouse; enter conclui, r apaga
    ax, ay, al, aa = menu.area_de_assinar()
    mx, my = mouse.get_position()
    riscou = assinatura.gravar((mx - ax) / al, (my - ay) / aa, mouse.button_pressed(mouse.LEFT))
    tela["riscando"] = riscou
    if riscou and tela["relogio"] - tela["risco"] > 0.3:
        som.tocar("gravando")
        tela["risco"] = tela["relogio"]
    if teclado.key_down("R"):
        assinatura.limpar()
    if teclado.key_down("ENTER") and tela["relogio"] > 0.5:
        concluir_noite()
        return "encerramento"
    return "assinatura"


def encerrar(tempo):
    # a placa pronta, o resultado e os créditos; espaço passa de etapa, esc
    # vai direto ao ranking
    if teclado.key_down("ESC"):
        encerramento.encerrar()
    elif avancou():
        encerramento.avancar()
    encerramento.atualizar(tempo)
    for evento in encerramento.eventos:
        som.tocar({"linha": "tique", "letra": "diamante", "creditos": "radio-fecha"}[evento])
    if encerramento.ativo():
        return "encerramento"
    abrir_ranking(menu.situacao["lugar"])
    return "ranking"


def abrir_ranking(destaque):
    tela["placar"] = pontuacao.ler_placar()
    tela["destaque"] = destaque


def tela_do_ranking():
    # volta ao menu pelo botão, por esc ou, depois de uma noite, por espaço
    voltar = clicado("ranking") == "voltar" or teclado.key_down("ESC")
    passou = tela["destaque"] is not None and tela["relogio"] > 1.0 and \
        (teclado.key_down("SPACE") or teclado.key_down("ENTER"))
    return "menu" if voltar or passou else "ranking"


def avancou():
    # a tecla ou o clique que passa a fala
    return (teclado.key_down("SPACE") or teclado.key_down("E") or teclado.key_down("ENTER")
            or mouse.button_down(mouse.LEFT))


def conversar(tempo, esc_pula=True):
    # uma conversa que para o jogo; devolve True quando ela acaba. no final,
    # esc só passa a linha: um toque não joga fora a última fala do jogo
    comecando = dialogo.conversa["indice"] == 0 and dialogo.conversa["tempo"] == 0.0
    if teclado.key_down("ESC") and esc_pula:
        dialogo.encerrar()
    elif (avancou() or teclado.key_down("ESC")) and not comecando:
        dialogo.avancar()
    dialogo.atualizar(tempo)
    ouvir_falas()
    return not dialogo.ativa()


def tempo_do_quadro():
    # o tempo medido oscila um pouco a cada quadro, e o movimento oscilaria
    # junto: perto de um número inteiro de quadros do ritmo, vale o inteiro
    agora = time.perf_counter()
    tempo = max(0.0, min(agora - ritmo["antes"], cfg.dt_maximo))
    ritmo["antes"] = agora
    periodo = ritmo["monitor"] or 1 / cfg.quadros_por_segundo
    inteiros = round(tempo / periodo)
    if inteiros >= 1 and abs(tempo - inteiros * periodo) < 0.25 * periodo:
        tempo = min(inteiros * periodo, cfg.dt_maximo)
    return tempo


def esperar_quadro():
    # com sincronia vertical quem marca o ritmo é o monitor, na troca de
    # quadro; dois relógios quase iguais fariam o quadro falhar de vez em quando
    if ritmo["monitor"] is not None:
        return
    # dorme até 2 ms antes da hora do quadro e espera o resto ativamente
    periodo = 1 / cfg.quadros_por_segundo
    ritmo["proximo"] = ritmo["proximo"] + periodo
    agora = time.perf_counter()
    if ritmo["proximo"] < agora:
        # atrasou: recomeça o compasso em vez de correr atrás
        ritmo["proximo"] = agora
        return
    if ritmo["proximo"] - agora > 0.002:
        time.sleep(ritmo["proximo"] - agora - 0.002)
    while time.perf_counter() < ritmo["proximo"]:
        pass


def perdeu_o_foco():
    # a janela saiu da frente (alt-tab, minimizar): o cronômetro é a
    # pontuação, e não pode correr sem ninguém jogando
    return any(ev.type == pygame.WINDOWFOCUSLOST for ev in janela.eventos)


def som_do_menu(nome_da_tela):
    # um tique quando o mouse chega a um botão
    foco = menu.botao_sob_mouse(nome_da_tela, mouse)
    if foco is not None and foco != tela["foco"]:
        som.tocar("foco")
    tela["foco"] = foco


def clicado(nome_da_tela):
    som_do_menu(nome_da_tela)
    botao = menu.clicado(nome_da_tela, mouse)
    if botao is not None:
        som.tocar("clique")
    return botao


def tela_do_menu():
    menu.situacao["continuar"] = 0 < progresso.dados["andar"] < len(fases.ANDARES)
    menu.situacao["melhor_total"] = progresso.dados["melhor_total"]
    menu.situacao["melhores"] = progresso.dados["melhores"]
    botao = clicado("menu")
    escolhido = menu.andar_sob_mouse(mouse)
    if botao is None and escolhido is not None and mouse.button_down(mouse.LEFT):
        # rejogar um andar pela lista de melhores tempos
        som.tocar("clique")
        comecar(escolhido)
        return "jogo"
    if botao == "jogar" or (botao is None and teclado.key_down("ENTER") and not menu.situacao["continuar"]):
        dialogo.iniciar(roteiro.abertura)
        som.tocar("radio-abre")
        return "abertura"
    if botao == "continuar" or (botao is None and teclado.key_down("ENTER")):
        comecar(progresso.dados["andar"])
        return "jogo"
    if botao == "treino":
        comecar_treino()
        return "jogo"
    if botao == "ranking":
        abrir_ranking(None)
        return "ranking"
    return {"controles": "controles", "sair": "fim"}.get(botao, "menu")


def tela_da_pausa():
    botao = clicado("pausa")
    if botao == "continuar" or teclado.key_down("ESC"):
        return "jogo"
    if botao == "reiniciar":
        jogo.reiniciar_andar()
        som.parar("alerta")
        som.tocar("reinicio")
        return "jogo"
    if botao == "menu_inicial":
        dialogo.calar()
        som.parar("alerta")
        return "menu"
    return "pausa"


def proxima_tela(tempo):
    # decide a tela do próximo quadro; "fim" fecha o jogo
    if estado == "menu":
        return tela_do_menu()
    if estado == "controles":
        voltar = clicado("controles") == "voltar" or teclado.key_down("ESC")
        return "menu" if voltar else "controles"
    if estado == "abertura":
        if conversar(tempo):
            comecar(0)
            return "jogo"
        return "abertura"
    if estado == "jogo":
        # com algo aberto, esc fecha o que está aberto, e não pausa
        esc = teclado.key_down("ESC") and not jogo.em_modal()
        if (esc or perdeu_o_foco()) and not transicao.ativa():
            return "pausa"
        return atualizar_jogo(tempo)
    if estado == "final":
        if conversar(tempo, False):
            assinatura.limpar()
            return "assinatura"
        return "final"
    if estado == "assinatura":
        return assinar()
    if estado == "encerramento":
        return encerrar(tempo)
    if estado == "ranking":
        return tela_do_ranking()
    return tela_da_pausa()


def trocar_de_tela(nova):
    # relógio da tela zerado; as telas cheias entram clareando do escuro
    global estado
    if nova == estado:
        return
    # da assinatura ao encerramento não há cortina: a placa é a mesma
    if nova in ("abertura", "assinatura", "ranking") or (nova == "menu" and estado in ("pausa", "ranking", "jogo")):
        tela["cortina"] = cfg.tempo_cortina
    tela["relogio"] = 0.0
    tela["risco"] = 0.0
    tela["foco"] = None
    estado = nova


def desenhar_jogo():
    indice = jogo.andar["indice"]
    # a tecla E aparece sobre cada tipo de coisa até a íris mexer nele uma
    # vez; nos monitores, sempre: é o único jeito de saber que se pode olhar
    dicas = ({"alavanca", "gaveta", "eco"} - jogo.corrida["usados"]) | {"monitores"}
    desenho.desenhar_cena(janela, jogo.andar["fase"], dicas)
    na_noite = isinstance(indice, int)
    painel.desenhar_hud(indice, jogo.corrida["total"], pontos_guardados() if na_noite else None,
                        tela["bonus"] / cfg.tempo_do_bonus, tela["aviso"])
    if not jogo.em_modal():
        lidas = sum(1 for andar_da_pista, _ in jogo.corrida["caderno"] if andar_da_pista == indice)
        painel.desenhar_caderno_na_hud(len(jogo.corrida["caderno"]), (lidas, leitura.pistas_do_andar(indice)))
    eco = jogo.andar["fase"]["eco"]
    if eco["gravando"]:
        painel.desenhar_gravacao(eco["tempo"] / cfg.tempo_eco)
    elif eco["tocando"] and eco["fita"]:
        painel.desenhar_gravacao(eco["indice"] / len(eco["fita"]), "O ECO REPETE")
    olhar = jogo.andar["fase"]["olhar"]
    if olhar is not None:
        painel.desenhar_olhar(olhar["vez"] + 1, len(jogo.andar["fase"]["cameras"]))
    if jogo.andar["detectada"] is not None:
        menu.desenhar_detectada()
    if estado == "final":
        painel.desenhar_conversa(dialogo.fala_atual(), dialogo.letras(), dialogo.escrita(), tela["relogio"], True)
        return
    andar = fases.andar_de(indice)
    # a fala da íris fica por cima da folha e da tranca: é ali que ela comenta
    leitura.desenhar(jogo.corrida["caderno"], jogo.corrida["placas"])
    painel.desenhar_placa_lida(andar["nome"], andar["ano"], narrativa.opacidade_da_placa())
    painel.desenhar_aviso(dialogo.aviso["fala"], dialogo.letras_do_aviso() if dialogo.aviso["fala"] else 0,
                          dialogo.opacidade_do_aviso())
    destino = transicao.passagem["destino"]
    if not na_noite and tela["licao"] is not None and not transicao.ativa() and not jogo.em_modal():
        titulo, texto = roteiro.licoes[tela["licao"]]
        painel.desenhar_licao(titulo, texto, min(1.0, tela["licao_tempo"] / cfg.tempo_da_licao))
    painel.desenhar_passagem(transicao.escuridao(), transicao.cartao(),
                             destino if isinstance(destino, int) else indice, tela["resultado"])
    if estado == "pausa":
        menu.desenhar_pausa(mouse)


def desenhar_tela():
    if estado == "menu":
        menu.desenhar_principal(mouse)
    elif estado == "controles":
        menu.desenhar_controles(mouse)
    elif estado == "abertura":
        menu.desenhar_abertura(dialogo.fala_atual(), dialogo.letras(), dialogo.escrita(), tela["relogio"])
    elif estado == "assinatura":
        menu.desenhar_assinatura(assinatura.tracos, mouse, tela["riscando"], tela["relogio"])
    elif estado == "encerramento":
        epilogo.desenhar_encerramento(jogo.corrida, tela["recordes"], assinatura.tracos, menu.situacao["lugar"],
                                      tela["relogio"])
    elif estado == "ranking":
        epilogo.desenhar_ranking(tela["placar"], tela["destaque"], mouse, tela["relogio"])
    else:
        desenhar_jogo()
    if tela["cortina"] > 0:
        graficos.desenhar_superficie(graficos.veu(int(255 * tela["cortina"] / cfg.tempo_cortina)), 0, 0)
    if tela["aviso_de_som"] > 0:
        painel.desenhar_aviso_de_som(som.estado["mudo"], min(1.0, tela["aviso_de_som"] / 0.3))


def tecla_do_som():
    # m liga e desliga o som em qualquer tela, e a escolha fica guardada
    if teclado.key_down("M"):
        progresso.guardar_mudo(som.alternar_mudo())
        tela["aviso_de_som"] = 1.5


# laço principal
while True:
    tempo = tempo_do_quadro()

    tela["relogio"] = tela["relogio"] + tempo
    menu.vida["tempo"] = menu.vida["tempo"] + tempo
    tela["cortina"] = max(0.0, tela["cortina"] - tempo)
    tela["aviso_de_som"] = max(0.0, tela["aviso_de_som"] - tempo)
    tecla_do_som()
    proxima = proxima_tela(tempo)
    if proxima == "fim":
        janela.close()
        break
    trocar_de_tela(proxima)
    desenhar_tela()

    esperar_quadro()
    janela.update()
