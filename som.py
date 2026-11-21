import os
import pygame
from PPlay.sound import Sound, Music, SoundManager
import configuracoes as cfg

# áudio do jogo (gdd, seção 5): efeitos curtos por mecanismo e uma faixa
# ambiente em laço. só toca; quem decide o que aconteceu é o jogo. sem
# placa de som, ou sem os arquivos, tudo aqui vira silêncio e o jogo segue

estado = {"disponivel": False, "mudo": False, "passo": 0, "musica": None}

# efeitos carregados uma vez, por nome de arquivo sem extensão
efeitos_sonoros = {}

# evento do jogo -> arquivo; os de efeitos.eventos e os de jogo.sinais
arquivo_do_evento = {
    "pulo": "pulo", "pouso": "pouso", "caixa": "caixa", "caixa_caiu": "caixa-caiu",
    "botao_pressionado": "botao-pressionado", "botao_solto": "botao-solto",
    "alavanca": "alavanca", "porta_abrindo": "porta-abrindo", "porta_fechando": "porta-fechando",
    "gaveta_abrindo": "gaveta-abrindo", "gaveta_fechando": "gaveta-fechando", "viga": "viga",
    "eco_grava": "eco-grava", "eco_toca": "eco-toca", "esteira": "esteira", "lancada": "lancada",
    "pista": "pista", "roda": "roda", "tranca_abre": "tranca-abre", "tranca_erro": "tranca-erro",
    "olhar": "foco", "tique": "tique", "alerta": "alerta", "detectada": "detectada", "reinicio": "reinicio",
}


def preparar():
    # depois da janela; devolve False quando não há como tocar
    try:
        SoundManager.inicializar()
    except pygame.error:
        return False
    for nome in cfg.sons:
        caminho = os.path.join(cfg.pasta_sons, nome + ".wav")
        if os.path.exists(caminho):
            efeitos_sonoros[nome] = Sound(caminho)
    estado["disponivel"] = True
    aplicar_volume()
    return True


def aplicar_volume():
    if not estado["disponivel"]:
        return
    SoundManager.set_sfx_volume(0 if estado["mudo"] else cfg.volume_efeitos)
    SoundManager.set_music_volume(0 if estado["mudo"] else cfg.volume_musica)


def tocar(nome):
    if nome in efeitos_sonoros:
        efeitos_sonoros[nome].play()


def parar(nome):
    if nome in efeitos_sonoros:
        efeitos_sonoros[nome].stop()


def tocar_musica():
    # a faixa ambiente não para entre telas nem quando o andar recomeça
    caminho = os.path.join(cfg.pasta_sons, cfg.musica)
    if not estado["disponivel"] or estado["musica"] is not None or not os.path.exists(caminho):
        return
    estado["musica"] = Music(caminho)
    estado["musica"].play()


def definir_mudo(mudo):
    estado["mudo"] = mudo
    aplicar_volume()


def alternar_mudo():
    definir_mudo(not estado["mudo"])
    return estado["mudo"]


def tocar_passo():
    # dois passos que se alternam: um pé e o outro
    estado["passo"] = 1 - estado["passo"]
    tocar("passo-%d" % (estado["passo"] + 1))


def ouvir(eventos):
    # os eventos de um quadro de jogo viram som
    # o mesmo evento duas vezes no quadro (duas portas no canal) soa uma vez
    for evento in dict.fromkeys(eventos):
        if evento == "passo":
            tocar_passo()
        elif evento in ("alerta_fim", "retorno"):
            # a íris saiu do cone, ou o andar recomeçou: a contagem se cala
            parar("alerta")
        elif evento in arquivo_do_evento:
            tocar(arquivo_do_evento[evento])
