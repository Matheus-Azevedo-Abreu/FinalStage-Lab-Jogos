# Final Stage

Projeto da disciplina Laboratório de Introdução à Programação, UFF.

## O que é

Jogo de puzzle e plataforma 2D, feito em Python com PPlay. É o projeto final da disciplina, em dupla. O jogador atravessa um prédio andar por andar até a cobertura, sem ser detectado pela segurança (fonte: documento de conceito da dupla, fora deste repositório).

## Objetivo

Entregar o jogo como projeto final da disciplina, cumprindo as regras do GDD: grade de 32 px, pulo de 2 tiles, câmera que detecta em 1 segundo, tempo como pontuação.

## Estado atual

Versão 8, de 18 de novembro de 2026: jogo completo, do menu ao ranking. Na versão 8: pistas reposicionadas para ninguém precisar recomeçar o andar atrás de uma que ficou para trás, e a arte dos andares toda redesenhada por código (panos de fundo da largura do andar, peças que parecem o que são, gavetas, vigas e móveis). Na versão 7: investigação. Cada andar de 1 a 9 tem pistas deixadas pelo autor e uma tranca de segredo que só abre por dedução; a história deixou de ser enfeite e virou o quebra-cabeça. Da versão 6: câmera com cone de verdade, cenário de cada autor dentro do quebra-cabeça, treino com a lição escrita, pontuação na tela, ranking com a assinatura, encerramento com créditos. O que ficou aberto está em `docs/auditoria.md`.

- **Investigação** (`docs/andares.md`, "Versão 7"): pistas examinadas com E (calendário, lembretes, estante, esquema na parede, livro de ocorrências…), caderno na tecla C e trancas de rodas. O segredo nunca está escrito pronto: sai de juntar as pistas com o que se vê no andar. Com uma dessas telas aberta o tempo não corre. Textos em `documentos.py`, regras em `investigacao.py`.

- **Jogo:** os dez andares de `docs/andares.md`, da recepção ao diamante da cobertura, com botão e folga, alavanca, dois botões, porta invertida, caixa, câmera de segurança e porta de relógio. Cada andar tem roteiro de solução, tentativas ingênuas que precisam falhar e teste de atalho em `testes/`.
- **História** (`docs/historia.md`, falas em `roteiro.py`): abertura na calçada com o briefing da Selene pelo rádio; uma linha de rádio na entrada dos andares ímpares; nos pares, a Íris conta os passos (os que a jogadora deu de verdade); placa de latão do autor em cada andar a partir do 2, lida ao parar diante dela; aviso da Selene no flagrante; final na cobertura e a placa sendo gravada com os tempos. A Selene não dá a solução; quem conta a história de cada autor são as pistas dele.
- **Som** (GDD, seção 5): 25 efeitos, um por interação, e uma faixa ambiente de 64 s em laço, todos sintetizados por `preparar-som.py`. M liga e desliga.
- **Progresso:** `progresso.json` (fora do git) guarda o andar em curso, o melhor tempo de cada andar e da corrida inteira. O menu oferece CONTINUAR e mostra o melhor tempo; a placa final marca os recordes com um losango.
- **Apresentação:** tela cheia na resolução da tela, pixels em escala inteira, câmera suave, HUD com andar e cronômetro, passagem entre andares com cartão, cortina entre telas, tremor curto no flagrante, tecla E sobre a primeira alavanca. Fontes do GDD: Silkscreen e VT323.
- **Mecânica do autor em cada andar:** gavetas (Prado), vigas de ferro (Ferraz), eco (Solano), esteiras (Contreiras), caixa (Selene), pilha (Sobral), câmera (Mirante), portas que contam passos (Quaresma). Regras em `docs/andares.md`, "Versão 4".
- **Final assinado:** a jogadora grava o nome na placa da cobertura com o mouse. Depois vêm a placa pronta, o resultado da noite gravado linha a linha, os créditos e o ranking.
- **Pontuação e ranking:** por andar, até 1000 pontos pelo tempo, menos 150 por flagrante e 30 por segredo errado, mais 50 pela placa do autor lida e 25 por pista; letra de S a D. As cinco melhores noites ficam no ranking, com a assinatura de quem as fez (`placar.json`, fora do git).
- **Treino:** doze salas, uma por mecanismo, cada uma com a lição na tela; R e flagrante voltam ao começo da sala.
- **Cenário vivo:** relógio na hora de verdade (andar 9), monitores com o que cada câmera vê e que se podem olhar com E (andar 8), lousa com os botões do canal (andar 7), lugares das vigas tracejados (andar 3).
- **Menu:** melhores tempos por andar, com clique para rejogar qualquer andar já alcançado.
- **Andar feito das coisas do autor:** plataformas e paredes de cada andar saem de `preparar-temas.py` (arquivos de aço do Prado, ferro da Ferraz, baias do Vieira, tijolo da Contreiras, armários da Selene, andaime do Sobral, racks da Mirante, relojoaria do Quaresma), e o que se empurra muda com o andar (caixote de plantas, monitor, relógio). Halo quente em volta de tudo o que é interativo, sombra da Íris, poeira no ar.
- **Arte:** gerada no ChatGPT e processada por `preparar-arte.py`; o que faltava de interface (teclas R e M, botão REINICIAR, capas) é derivado por `preparar-interface.py`. Procedência em `assets/CREDITOS.md`.
- **Branches:** `main` e `reserva`.

### Pendências

- Olhar a rolagem jogando: a câmera foi refeita (mola amortecida, sincronia vertical) e medida por simulação, mas a sincronia com o monitor só se confere na tela de verdade.
- Lista completa do que está aberto, com severidade e correção sugerida: `docs/auditoria.md`. Os dois de maior efeito: R recomeça o andar inteiro (falta ponto de retorno por sala) e controles cujo efeito fica fora da tela.
- Ver jogando o que só foi visto em quadro renderizado: cone da câmera, monitores, lição do treino, encerramento e ranking; e, da versão 7, as pistas, a tranca, o caderno, a tinta das câmeras e as setas repintadas (`previas/telas-versao-7.py`).
- Jogar os nove enigmas com gente de fora: a dificuldade deles nunca foi medida.
- Ver jogando a arte da versão 8 (panos, peças, gavetas, vigas, móveis): só foi vista em render.
- Decidir o que fazer com a arte antiga sem uso (`fundo-02` a `fundo-09`, `parede-NN`, `cenario-*`, peças soltas `tema-<nome>-<peça>`): continua no disco.
- `entrega/trailer.mp4` é o trailer de anúncio da versão 8 (60 s, com música sintetizada por `preparar-trailer.py`); a música só foi conferida por medida, falta ouvir. O resto de `entrega/` (capturas, teaser, vídeo da partida, GDD em pdf e docx) ficou da versão de 10 de novembro.
- Andar 5 é curto (9 s no roteiro) e mais de execução que de raciocínio.
- Ouvir o áudio com atenção: foi sintetizado e conferido só por medida (duração, pico, laço), não por ouvido. Volumes em `configuracoes.py` (`volume_efeitos`, `volume_musica`); o pico de cada som em `preparar-som.py`.
- Teste com jogadores (`docs/teste-com-jogadores.md`): a dificuldade dos andares ainda não foi medida com gente de fora.
- Fundos panorâmicos para os andares largos (`assets/LEIA-ME.md`, "Arte que falta"); hoje o fundo de 800 px se repete.
- Publicação: página no itch.io, teaser no YouTube e galeria do PPlay (material e textos em `entrega/`).
- Confirmar com o professor se a disciplina tem regra sobre arte gerada por IA.

### Divergências conhecidas

- `PPlay/uikit.py` funciona com esta PPlay, mas nada no jogo o usa desde a reescrita do `menu.py`.
- O GDD de agosto previa movimento em grade, sala única de 640 × 480 e painel de acesso; o jogo é plataforma com rolagem. O GDD atualizado (`docs/gdd.md`, versão 2.0) registra cada mudança e o motivo.

## Estrutura

### Módulos

- `configuracoes.py` — janela, física, medidas, tempos, tabela de arte e de animações, colisão
- `fases.py` — os dez andares, validação e carregamento
- `jogo.py` — o andar em curso e um quadro de jogo (sem pygame; os testes rodam este código)
- `jogador.py` — movimento, gravidade e colisão da Íris
- `mecanismos.py` — caixas, botões, alavancas, canais, portas, câmeras, saída e diamante
- `documentos.py` — o texto das pistas e os segredos das trancas
- `investigacao.py` — pista, tranca de segredo e caderno (sem pygame)
- `leitura.py` — desenha a folha da pista, as rodas da tranca e o caderno
- `preparar-investigacao.py` — script à parte: grava a arte da investigação
- `preparar-fundos.py` — script à parte: grava o pano de fundo de cada andar, na largura dele
- `preparar-mobilia.py` — script à parte: grava os móveis e objetos de cada autor
- `animacao.py` — estado da animação da Íris
- `efeitos.py` — transições de portas, alavancas e botões, poeira e brilho
- `enquadramento.py` — a visão que segue a Íris
- `graficos.py` — carregamento e cache de sprites e superfícies, textos, véu e ampliação da visão
- `desenho.py` — desenho da cena
- `cenario.py` — os objetos de cada autor no andar, e os que mostram o estado do quebra-cabeça
- `menu.py` — telas de menu, controles, abertura, pausa, detecção e assinatura
- `encerramento.py` — etapas e texto do fim: placa, resultado e créditos
- `epilogo.py` — desenho do encerramento e do ranking
- `painel.py` — hud (andar e cronômetro), cartão de passagem, caixa de fala, linha do rádio e placa lida
- `transicao.py` — passagem entre andares
- `roteiro.py` — as falas do jogo, só texto
- `dialogo.py` — estado das falas: a conversa que para o jogo e a linha do rádio que não para
- `narrativa.py` — quando a história fala: entrada do andar, placas, flagrante
- `som.py` — efeitos e faixa ambiente, pela `Sound` e pela `Music` da PPlay
- `progresso.py` — andar em curso e melhores tempos, em `progresso.json`
- `pontuacao.py` — pontos e letra (S a D) por andar e da noite, e o ranking de cinco em `placar.json`
- `assinatura.py` — os traços da assinatura na placa final
- `main.py` — tela cheia, ritmo do laço, cronômetro e troca de telas
- `preparar-arte.py` — script à parte: gera `assets/` a partir da arte de origem em `codex/`
- `preparar-temas.py` — script à parte: desenha as peças de cada andar e o que se empurra
- `preparar-som.py` — script à parte: sintetiza `assets/sons/`
- `preparar-interface.py` — script à parte: desenha os botões de menu e a chapa do ranking; deriva teclas e capas
- `preparar-cenario.py` — script à parte: recorta dos fundos os objetos de cada autor e grava a parede limpa

Outras pastas:
- `assets/` — arte do jogo; tabela de arquivos em `assets/LEIA-ME.md`;
- `entrega/` — o que vai ao professor e às páginas do jogo: capas, capturas, textos do itch.io e do PPlay, roteiro do teaser;
- `docs/` — `gdd.md` (o GDD atualizado, versão 2.0), `historia.md` (a história), `andares.md` (o desenho aprovado dos dez andares), `prompt-andares.md` (o roteiro que os construiu), `prompts-chatgpt.md` e `prompts-chatgpt-lote-2.md` (especificação da arte);
- `testes/` — testes versionados, sem janela (seção "Testes" do `CLAUDE.md`);
- `PPlay/` — biblioteca;
- `codex/`, `previas/`, `arte-original/` e `temporario/` — ignoradas pelo `.gitignore`.

### Os dez andares

Desenho, solução e dificuldade de cada um em `docs/andares.md` (versão 2). Do andar 2 ao 9, cada um tem pelo menos um quebra-cabeça de raciocínio: a tentativa óbvia falha, e isso é verificado por código (`roteiros.ingenuos`, em `testes/testar_andares.py`). Tempos da solução automática no mesmo teste; um jogador leva de 2 a 4 vezes isso, mais o tempo de pensar. Dificuldade não se mede por código: a ficha de `docs/teste-com-jogadores.md` é a medida de verdade.

| Andar | Autor | O que ensina | Quebra-cabeça | Largura | Solução automática |
|---|---|---|---|---|---|
| 1 | Recepção | andar, pular, subir plataformas, explorar com a rolagem | — | 40 | 7,5 s |
| 2 | Benedito Prado, 2009 | gavetas de arquivo: abrem com E e fecham sozinhas em 3 s | degrau, escada e ponte de gavetas | 50 | 9,8 s |
| 3 | Adélia Ferraz, 2011 | três alavancas que deslocam três vigas de ferro | a combinação que monta a escada, com uma viga servindo a dois lugares | 54 | 19,0 s |
| 4 | Solano Vieira, 2012 | o eco: grave o que fez e esteja em dois lugares | o eco precisa fazer dois serviços, e você, o terceiro | 56 | 20,8 s |
| 5 | Noemi Contreiras, 2014 | esteiras: levam, e lançam quem pula | a saída fica para trás: ir até o fim para repintar as setas e voltar | 56 | 9,1 s |
| 6 | Selene Amparo, 2016 | a caixa: empurrar, degrau, botão, cair, empilhar, segurar a porta | a caixa certa primeiro, ou ela se perde no poço | 70 | 19,1 s |
| 7 | Aníbal Sobral, 2018 | "todos" sem memória | uma caixa para dois botões; a pilha de duas | 59 | 17,9 s |
| 8 | Cássia Mirante, 2020 | câmera com cone e ponto cego; porta fechada cega, monitor não | fechar a janela, e não desligar a câmera | 76 | 16,3 s |
| 9 | Otávio Quaresma, 2022 | portas que contam os passos da Íris, não os segundos | a caixa no vão (calço) | 79 | 31,2 s |
| 10 | Cobertura | nenhum mecanismo; o diamante no fim | — | 30 | 5,0 s |

### Mapas

Cada andar em `fases.py` é um dicionário com 12 linhas de texto, um caractere por tile de 32×32, e `detalhes` e `regras` para o que a letra não carrega (canal, porta invertida, porta aberta ou com caixa no vão, duração do relógio, direção e alcance da câmera, decoração), além de `memorias` (memória do botão por canal) e `marcas` (marcas de canal) opcionais. Tabela de letras e campos no `CLAUDE.md`, seção "Formato do mapa". Porta, saída e diamante ocupam duas células empilhadas. Andar novo é uma entrada nova em `ANDARES`, sem tocar em `main.py`; `fases.carregar` recusa mapa mal formado.

### Decisões de física

Pulo de 380 px/s com gravidade de 1000 px/s² alcança 72 px (69 px medidos a 60 quadros por segundo): vence dois tiles e não vence três, como o GDD determina.

A porta de botão respeita a folga de 3 segundos depois de perder o acionamento. Caixa em cima segura indefinidamente. Num canal "todos", a memória do botão é do andar: 0 por padrão, e o andar 4 declara 3 segundos (`memorias`). Nenhuma porta fecha com a Íris ou uma caixa no vão. A porta de relógio fecha depois da sua duração mesmo com o canal ativo e só reabre numa nova ativação. A câmera detecta depois de 1 segundo contínuo com a Íris no cone e a visão livre, e o andar recomeça; o tempo nunca é derrota. O cone sai da lente, inclinado para o chão, e é cortado por parede e porta fechada; logo abaixo da câmera há ponto cego.

O empurrão desloca a caixa exatamente um tile, deslizando a 120 px/s, e alinha à grade. A caixa é sólida de lado: o empurrão acontece no contato, e só com a Íris no chão; no ar, dá para subir nela. Caixa caindo não é empurrada.

## Como usar

Python 3.12 e pygame 2.6.1; a PPlay vai junto, na pasta `PPlay/`.

    python3.12 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python main.py

No Windows: `py -3.12 -m venv .venv`, `.venv\Scripts\pip install -r requirements.txt`, `.venv\Scripts\python main.py`. Ou dois cliques em `Jogar no Windows.bat`, `Jogar no Mac.command` ou `Jogar no Linux.sh`, que fazem isso na primeira vez. No Linux, se o gerenciador de arquivos não abrir com dois cliques: botão direito e "Executar como programa", ou no terminal, `bash "Jogar no Linux.sh"`.

### Controles

| Tecla | Ação |
|---|---|
| ← → ou A D | mover |
| espaço | pular |
| E | mexer no que é dourado: alavanca, gaveta, porta-retratos do eco; examinar pista e tranca; passar a fala |
| C | abrir e fechar o caderno |
| A D, W S, 0 a 9, ENTER | na tranca: escolher a roda, girar, digitar o algarismo, conferir |
| ESC | fechar pista, tranca ou caderno; pausar e retomar; na tela de controles, voltar; na abertura e no final, pular as falas |
| R | reiniciar o andar |
| M | ligar e desligar o som |
| ENTER | no menu, jogar (ou continuar) |
| mouse | botões do menu e da pausa; passar a fala; assinar a placa final (segurando o botão) |
| 1 a 9 | pular para o andar (só com `depuracao = True` em `configuracoes.py`) |
| P | salvar a tela em `captura-N.png` (só com `depuracao = True`) |

## Responsáveis

| Pessoa | Papel |
|---|---|
| Matheus Azevedo Abreu | coautor; arte; desenvolvimento das mecânicas entre personagem e ambiente |
| Gabriel Ribeiro Ota Yida | coautor; desenvolvimento da movimentação do personagem; menus |
| Enzo Lemos Von Paumgartten Klautau | coautor; arte; level design; resolução de bugs e documentos |
