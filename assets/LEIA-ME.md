# assets — pasta definitiva

Tudo que o jogo carrega do disco está aqui. Todos os PNGs saem do
`preparar-arte.py`, que lê `codex/` (fora do git) e grava nesta pasta:

    .venv/bin/python preparar-arte.py

Não edite PNG à mão: rode o script de novo. Blocos de cor de reserva vão
para `temporario/`, fora do git. Procedência: `CREDITOS.md`.

Última conferência: 10 de novembro de 2026 (versão final: som, falas, placas).

## Regras

- Objetos, Íris e peças de construção: paleta do mundo de 25 cores
  (`paleta.json`), transparência binária.
- Fundos, cenas, retratos e interface: fora da paleta, transparência binária.
- Deslocamento `(x, y)` = onde o PNG é desenhado em relação à posição do
  objeto no código; `y = altura da célula − base da figura`. A tabela vive
  em `configuracoes.py`, em `arte`.
- Íris: quadro de 64×64 desenhado em `(x − 24, y − 16)` em relação ao
  colisor de 16×48. Só leste; oeste por espelhamento no carregamento.

## Arquivos

| Arquivo | Tamanho | Uso no código |
|---|---|---|
| `iris-parada.png` | 256×64 | 4 quadros de 64×64, ciclo 0.8 s; desenho em (x−24, y−16) |
| `iris-andando.png` | 384×64 | 6 quadros de 64×64, ciclo 0.6 s; desenho em (x−24, y−16) |
| `iris-pulando.png` | 64×64 | 1 quadro de 64×64; desenho em (x−24, y−16) |
| `iris-caindo.png` | 64×64 | 1 quadro de 64×64; desenho em (x−24, y−16) |
| `iris-empurrando.png` | 384×64 | 6 quadros de 64×64, ciclo 0.6 s; desenho em (x−24, y−16) |
| `iris-acionando.png` | 192×64 | 3 quadros de 64×64, ciclo 0.3 s; desenho em (x−24, y−16) |
| `iris-preparando.png` | 64×64 | 1 quadro, 0.05 s no começo da subida; desenho em (x−24, y−16) |
| `iris-aterrissando.png` | 128×64 | 2 quadros de 64×64, 0.16 s ao tocar o chão parada; desenho em (x−24, y−16) |
| `iris-detectada.png` | 192×64 | 3 quadros de 64×64, 0.9 s, tocados uma vez quando a câmera detecta |
| `caixa.png` | 32×32 | deslocamento (+0, +0) |
| `botao-solto.png` | 32×16 | deslocamento (+0, +0) |
| `botao-pressionado.png` | 32×16 | deslocamento (+0, +0) |
| `alavanca-desligada.png` | 32×32 | deslocamento (-8, +0) |
| `alavanca-ligada.png` | 32×32 | deslocamento (-8, +1) |
| `alavanca-meio.png` | 32×32 | deslocamento (-8, +0); 0.08 s ao trocar de estado |
| `botao-meio.png` | 32×16 | deslocamento (+0, +0); 0.08 s ao trocar de estado |
| `camera.png` | 32×32 | vigiando; olha para a direita, espelhada para a esquerda no carregamento |
| `camera-alerta.png` | 32×32 | deslocamento (+0, +0) |
| `camera-desligada.png` | 32×32 | deslocamento (+0, +0) |
| `porta-trancada.png` | 32×64 | deslocamento (+0, +0) |
| `porta-aberta.png` | 32×64 | deslocamento (+0, +0) |
| `porta-abrindo.png` | 96×64 | 3 quadros de 32×64 em 0.24 s; ao contrário ao fechar |
| `saida.png` | 32×64 | deslocamento (+0, +0) |
| `diamante.png` | 32×64 | deslocamento (+0, +0) |
| `icone-botao.png` | 16×16 | deslocamento (+8, -14) |
| `icone-alavanca.png` | 16×16 | deslocamento (+8, -14) |
| `icone-relogio.png` | 16×16 | deslocamento (+8, -14), acima da porta de relógio |
| `placa.png` | 32×16 | placa do autor, na célula `p`; deslocamento (+0, +8) |
| `parede-interna.png` | 32×32 | deslocamento (+0, +0) |
| `laje.png` | 32×32 | deslocamento (+0, +0) |
| `divisoria.png` | 32×32 | deslocamento (+0, +0) |
| `laje-esquerda.png` | 32×32 | deslocamento (+0, +0); ponta esquerda da plataforma |
| `laje-direita.png` | 32×32 | deslocamento (+0, +0); ponta direita da plataforma |
| `divisoria-pe.png` | 32×32 | deslocamento (+0, +0); fim de baixo da divisória |
| `poeira-passo.png` | 64×16 | 4 quadros de 16×16 em 0.32 s; passos e aterrissagem |
| `poeira-caixa.png` | 128×16 | 4 quadros de 32×16 em 0.32 s; caixa empurrada |
| `brilho-diamante.png` | 64×16 | 4 quadros de 16×16 em 0.8 s, em laço, a (+8, +10) do diamante |
| `retrato-neutra.png` | 192×192 | falas da Íris: 96 na caixa da conversa, 38 na linha do rádio (× escala da interface) |
| `retrato-atenta.png` | 192×192 | falas da Íris: 96 na caixa da conversa, 38 na linha do rádio (× escala da interface) |
| `retrato-cansada.png` | 192×192 | falas da Íris: 96 na caixa da conversa, 38 na linha do rádio (× escala da interface) |
| `retrato-desconfiada.png` | 192×192 | falas da Íris: 96 na caixa da conversa, 38 na linha do rádio (× escala da interface) |
| `retrato-indecifravel.png` | 192×192 | falas da Íris: 96 na caixa da conversa, 38 na linha do rádio (× escala da interface) |
| `radio-falando.png` | 192×192 | a Selene, enquanto a linha é escrita |
| `radio-silencio.png` | 192×192 | a Selene, com a linha escrita |
| `titulo-final-stage.png` | 480×62 | — |
| `titulo-detectada.png` | 480×39 | — |
| `titulo-concluido.png` | 480×38 | — |
| `titulo-pausa.png` | 480×27 | tela de pausa, centrado |
| `titulo-controles.png` | 480×27 | tela de controles, centrado |
| `botao-jogar.png` | 192×48 | — |
| `botao-jogar-ativo.png` | 192×48 | — |
| `botao-controles.png` | 192×48 | — |
| `botao-controles-ativo.png` | 192×48 | — |
| `botao-sair.png` | 192×48 | — |
| `botao-sair-ativo.png` | 192×48 | — |
| `botao-continuar.png` | 192×48 | pausa |
| `botao-continuar-ativo.png` | 192×48 | pausa |
| `botao-menu-inicial.png` | 192×48 | pausa |
| `botao-menu-inicial-ativo.png` | 192×48 | pausa |
| `botao-voltar.png` | 192×48 | controles |
| `botao-voltar-ativo.png` | 192×48 | controles |
| `tecla-esquerda.png` | 32×32 | — |
| `tecla-direita.png` | 32×32 | — |
| `tecla-a.png` | 32×32 | — |
| `tecla-d.png` | 32×32 | — |
| `tecla-e.png` | 32×32 | — |
| `tecla-espaco.png` | 96×32 | — |
| `tecla-esc.png` | 32×32 | — |
| `tecla-p.png` | 32×32 | sem uso: P só salva a tela, e só com `depuracao` |
| `tecla-r.png` | 32×32 | tela de controles e decoração do andar 6; sai do `preparar-interface.py` |
| `tecla-m.png` | 32×32 | tela de controles; sai do `preparar-interface.py` |
| `botao-reiniciar.png`, `botao-reiniciar-ativo.png` | 192×48 | pausa; saem do `preparar-interface.py` |
| `cursor-seta.png` | 16×16 | ponta em (0, 0) |
| `cursor-mao.png` | 16×16 | sobre botões; ponta em (3, 0) |
| `placa-leitura.png` | 384×128 | placa lida, no alto da tela, com nome e ano gravados por código |
| `fundo-01.png` | 800×384 | chão em y=352 |
| `fundo-02.png` | 800×384 | chão em y=352 |
| `fundo-03.png` | 800×384 | chão em y=352 |
| `fundo-04.png` | 800×384 | chão em y=352 |
| `fundo-05.png` | 800×384 | chão em y=352 |
| `fundo-06.png` | 800×384 | chão em y=352 |
| `fundo-07.png` | 800×384 | chão em y=352 |
| `fundo-08.png` | 800×384 | chão em y=352 |
| `fundo-09.png` | 800×384 | chão em y=352 |
| `fundo-10.png` | 800×384 | chão em y=352 |
| `cena-abertura.png` | 800×384 | fundo da abertura |
| `cena-final.png` | 800×384 | — |
| `menu-fundo.png` | 800×384 | — |

Alavancas têm 32 de largura, e não 16: o cabo vira para lados opostos nos
dois estados, e a base fica centrada. O colisor continua 16×32.

## Fontes

`fontes/silkscreen.ttf` (títulos, rótulos, indicador de andar) e
`fontes/vt323.ttf` (cronômetro e números), as duas do GDD, sob licença OFL,
com o texto da licença ao lado. Desenhadas sem suavização, em tamanhos
múltiplos da escala da interface.

## Peças por andar

`tema-<nome>-<peça>.png` (10 temas, 6 peças de 32×32 cada: `laje`, `laje-esquerda`, `laje-direita`, `parede`, `divisoria`, `divisoria-pe`) e `caixa-<nome>.png` (o que se empurra: `sobral`, `mirante`, `quaresma`; `prado` ainda sem uso). Desenhados por código, na paleta do mundo, pelo `preparar-temas.py`:

    .venv/bin/python preparar-temas.py

Do mesmo script saem as peças das mecânicas: `gaveta-fechada.png` e `gaveta-aberta.png` (32×12), `viga.png` (32×16, repetida pela largura), `esteira.png` (32×32) com `seta.png` (7×5) pintada por cima, `eco-marca.png` (32×32, o porta-retratos) e `buril.png` (40×40, a ponta de gravar da assinatura, com a ponta no canto de baixo à esquerda).

O andar escolhe o tema e a caixa em `fases.py` (`tema`, `caixa`). `laje.png`, `parede-interna.png`, `divisoria*.png` continuam como reserva de andar sem tema.

## Sons

`sons/`, 33 arquivos WAV mono, todos sintetizados por `preparar-som.py`
(biblioteca padrão do Python, semente fixa: rodar de novo grava os mesmos
arquivos). Não edite à mão; mude o script e rode:

    .venv/bin/python preparar-som.py

| Arquivo | Quando toca |
|---|---|
| `passo-1.wav`, `passo-2.wav` | passos, alternados |
| `pulo.wav`, `pouso.wav` | sair do chão e voltar a ele |
| `botao-pressionado.wav`, `botao-solto.wav` | botão de pressão |
| `alavanca.wav` | alavanca acionada |
| `porta-abrindo.wav`, `porta-fechando.wav` | qualquer porta |
| `caixa.wav`, `caixa-caiu.wav` | caixa empurrada um tile; caixa que caiu |
| `tique.wav` | um segundo a menos na porta em contagem |
| `alerta.wav` | a câmera contando o segundo; para se a Íris sai do cone |
| `detectada.wav`, `reinicio.wav` | flagrante; tecla R e REINICIAR |
| `saida.wav`, `diamante.wav` | fim do andar; o diamante |
| `foco.wav`, `clique.wav` | botões dos menus |
| `radio-abre.wav`, `radio-fecha.wav` | a Selene entra e sai do rádio |
| `voz-selene.wav`, `voz-iris.wav` | uma sílaba a cada três letras da fala |
| `gaveta-abrindo.wav`, `gaveta-fechando.wav` | gaveta de arquivo |
| `viga.wav` | viga de ferro começa a correr |
| `eco-grava.wav`, `eco-toca.wav` | o eco começa a gravar; o eco aparece |
| `esteira.wav`, `lancada.wav` | as setas repintadas; o pulo com embalo |
| `placa.wav`, `gravando.wav` | a placa aparece; a placa final sendo gravada |
| `ambiente.wav` | faixa ambiente, 64 s, 22 050 Hz, em laço sem emenda |

## Ainda sem uso no código

Só `tecla-p.png`.

## Arte antiga

A pasta `sprites/`, com a arte e a documentação da base antiga, saiu em
29 de setembro de 2026: nada no código a carregava e os botões foram
substituídos pelo lote 2. Continua no histórico do git.

## Arte que falta

Lista acumulada pelas fases de `docs/prompt-andares.md`, para gerar de uma
vez no fim. Até lá, o jogo usa o substituto indicado.

| Arte | Onde entra | Substituto atual |
|---|---|---|
| fundos panorâmicos por andar, 384 px de altura, chão em y = 352: andar 1 com 1280 px, 2 com 1728, 3 e 4 com 1920, 5 e 6 com 2240, 7 com 2368, 8 e 9 com 2880 (o 8 passou de 70 para 90 colunas nos andares v2), 10 com 960 | os dez andares, todos mais largos que 800 px | o fundo de 800 px repetido, com uma coluna escurecida em cada junta; na cobertura (andar 10) a coluna fica em pé no céu aberto |

## Versão 6 (11 de novembro de 2026)

Arte refeita ou nova, toda por código. Depois de um `preparar-arte.py`,
rode `preparar-temas.py`, `preparar-interface.py` e
`preparar-cenario.py`, nessa ordem: o primeiro regrava versões antigas
de ícones, placa e botões.

| Arquivo | Tamanho | Script | Uso no código |
|---|---|---|---|
| `botao-<nome>.png`, `botao-<nome>-ativo.png` | 192×40 | `preparar-interface.py` | botões de menu: continuar, jogar, treino, ranking, controles, sair, voltar, reiniciar, menu-inicial |
| `titulo-ranking.png` | 480×27 | `preparar-interface.py` | letreiro da tela do ranking |
| `placa-ranking.png` | 384×56 | `preparar-interface.py` | chapa de cada lugar do ranking; área livre x 30–353, y 6–49 |
| `icone-botao.png`, `icone-alavanca.png`, `icone-relogio.png` | 16×16 | `preparar-temas.py` | acima das portas; deslocamento (+8, −14) |
| `placa.png` | 32×16 | `preparar-temas.py` | placa do autor, na célula `p`; deslocamento (+0, +8) |
| `gaveta-fechada.png`, `gaveta-aberta.png` | 32×32 | `preparar-temas.py` | módulo de arquivo na célula `g`; aberta, a tábua são os 10 px de cima |
| `viga.png`, `viga-lugar.png` | 32×16 | `preparar-temas.py` | trecho da viga; tracejado dos dois lugares dela na parede |
| `esteira.png`, `seta.png` | 32×32, 7×5 | `preparar-temas.py` | faixa por cima da peça do andar; setas correndo em y 1–5 |
| `eco-marca.png`, `eco-marca-ativa.png` | 32×32 | `preparar-temas.py` | porta-retratos virado para a parede; de frente enquanto grava e repete |
| `raspao-caixa.png` | 128×16 | `preparar-temas.py` | 4 quadros de 32×16 em 0,32 s: caixa arrastada sobre outra |
| `lousa.png` | 64×48 | `preparar-temas.py` | lousa do andar 7; o giz é desenhado pelo jogo em x 5–58, y 5–36 |
| `lugar-da-caixa.png` | 32×32 | `preparar-temas.py` | marca no chão do lugar de cada caixa (andar 6) |
| `parede-02.png` a `parede-09.png` | 800×384 | `preparar-cenario.py` | o fundo do andar sem os objetos do autor; repete lado a lado |
| `cenario-prado.png` | 108×88 | `preparar-cenario.py` | calendário de 2009, cadeira, mesa e copo |
| `cenario-ferraz.png` | 88×50 | `preparar-cenario.py` | bancada com o manual |
| `cenario-vieira.png` | 124×62 | `preparar-cenario.py` | duas mesas, uma cadeira |
| `cenario-contreiras.png` | 56×82 | `preparar-cenario.py` | porta emparedada |
| `cenario-amparo-copa.png`, `cenario-amparo-estantes.png` | 82×54, 230×64 | `preparar-cenario.py` | balcão com a xícara; estantes e mesa |
| `cenario-sobral.png` | 336×284 | `preparar-cenario.py` | esquema do prédio a giz |
| `cenario-mirante.png` | 51×200 | `preparar-cenario.py` | pilha de monitores e cadeira; vidros em (13, 18/41/65/88/112/136), 24×14 |
| `cenario-quaresma.png` | 56×58 | `preparar-cenario.py` | relógio sem ponteiros; centro (27, 25), raio 15 |

Os objetos de `cenario-*.png` têm transparência parcial na borda (saem de
fundo de arte suave) e são desenhados escurecidos como o fundo.
`fundo-02.png` a `fundo-09.png` continuam na pasta: são a origem do
`preparar-cenario.py`. `cena-final.png` não é mais usada pelo jogo.
