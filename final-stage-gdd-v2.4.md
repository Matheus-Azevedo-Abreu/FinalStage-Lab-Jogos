# Final Stage — Documento de Game Design

Jogo de puzzle e plataforma 2D em pixel art

Laboratório de Introdução à Programação — Universidade Federal Fluminense
Prof. Esteban Walter Gonzalez Clua
Matheus Azevedo Abreu · Gabriel Ribeiro Ota Yida · Enzo Lemos Von Paumgartten Klautau

**Versão 2.4 — 20 de novembro de 2026.**
Atualiza a versão 2.3 (18 de novembro de 2026) para registrar a adição do terceiro integrante da equipe, o estado atual do jogo na data de entrega e o balanço entre o que foi planejado e o que foi de fato realizado. As seções anteriores estão mantidas; as novidades estão nas seções 8, 14 e 15.

---

## 1. Nome do Projeto

Final Stage. O nome carrega o duplo sentido que estrutura o jogo: é a etapa final de um processo seletivo e, ao mesmo tempo, a última fase de um jogo. A candidata e quem joga atravessam a mesma prova.

## 2. High Concept

Final Stage é um jogo de puzzle e plataforma 2D em pixel art, de visão lateral. Íris Portela, recém-formada em Ciência da Computação, enfrenta a sétima e última etapa do processo seletivo da Vértice: subir, sozinha e à noite, os dez andares do prédio da empresa, sem ser flagrada pelas câmeras, e pegar o diamante que está na cobertura. Cada andar é um quebra-cabeça feito com a invenção de quem o projetou: gavetas de arquivo, vigas de ferro, um eco que repete o que a Íris fez, esteiras, caixas, câmeras e portas que contam passos.

O jogo não tem tutorial em texto: cada mecânica aparece primeiro num lugar em que errar não custa nada, e só depois é cobrada. O diferencial está em duas coisas. A primeira é a integração entre tema e mecânica: os quebra-cabeças são a entrevista, e cada andar foi "projetado" por um candidato contratado antes, cujo nome está numa placa de latão na entrada. A segunda é a direção visual: a cor funciona como interface. O prédio é frio e recua; tudo o que se pode tocar é quente e avança.

## 3. Gameplay e Enredo

### 3.1 Premissa narrativa

Ninguém sabe ao certo o que a Vértice faz. Sabe-se que o processo seletivo tem sete etapas e que a sétima não é entrevista. Ela acontece à noite, no prédio, e a candidata vai sozinha: no topo há um diamante, e a etapa termina quando ela o pega. O sistema de segurança fica ligado. Se uma câmera a enxerga por um segundo inteiro, a segurança a acompanha de volta à entrada do andar, e o andar recomeça. Ninguém é eliminado. O tempo é anotado.

Pelo rádio, a coordenadora Selene Amparo explica as regras, comenta a subida e nunca dá a solução. A partir do segundo andar, uma placa ao lado da entrada traz um nome e um ano: os andares foram projetados pelos candidatos contratados nos anos anteriores. Ser contratada pela Vértice significa projetar o próximo andar.

### 3.2 Pilares de design

- **Aprender fazendo.** Cada mecânica é ensinada sozinha antes de ser combinada. A única letra que aparece no cenário é a tecla que se aperta.
- **Clareza visual.** Distingue-se num relance o que é cenário do que é interativo. Ambiente frio, interativo quente. Vermelho, verde e magenta são só de estado e perigo.
- **Profundidade sobre quantidade.** Dez andares completos, com poucos mecanismos explorados a fundo.

### 3.3 Ciclo de aprendizado

Aprender → Experimentar → Entender → Resolver → Avançar. Do andar 2 ao 9, todo andar tem pelo menos um quebra-cabeça de raciocínio verificado por código.

### 3.4 Mecânicas do núcleo

| Elemento | Andar e autor | Comportamento | Papel no quebra-cabeça |
|---|---|---|---|
| Gaveta de arquivo | 2, Benedito Prado | Abre com E, vira tábua, fecha sozinha em 3 s | Degrau, escada e ponte com prazo |
| Viga de ferro | 3, Adélia Ferraz | Vai para o outro lugar com número ímpar de alavancas | Montar a escada com três alavancas |
| Eco | 4, Solano Vieira | Grava 6 s do que a Íris faz; o eco repete e pesa como ela | Estar em dois lugares ao mesmo tempo |
| Esteira | 5, Noemi Contreiras | Leva a 240 px/s; quem pula leva o embalo | Vãos que só se cruzam a favor |
| Caixa | 6, Selene Amparo | Empurrada um tile por vez; cai de bordas; empilha | Peso, degrau, calço de porta |
| Pilha | 7, Aníbal Sobral | Duas caixas empilhadas andam juntas | O que fica por cima |
| Câmera | 8, Cássia Mirante | Cone fixo; 1 s no cone reinicia o andar | Restringe a rota |
| Porta que conta passos | 9, Otávio Quaresma | Fecha depois de N passos; pulo vale três | Distância como prazo |

### 3.5 Regras precisas

Plataforma lateral: caminhada 180 px/s, pulo 380 px/s, gravidade 1000 px/s². A Íris sobe 2 tiles (3 sobre caixa). Cruza vão de 4 tiles. Caixa anda 1 tile por empurrão. Nenhuma porta fecha com a Íris ou caixa no vão. Detecção: 1 s contínuo no cone reinicia o andar. Tempo é pontuação, nunca derrota.

### 3.6 Progressão

| Nº | Andar | A invenção |
|---|---|---|
| 1 | Recepção | andar, pular, explorar |
| 2 | Benedito Prado, 2009 | gavetas de arquivo |
| 3 | Adélia Ferraz, 2011 | três alavancas, três vigas |
| 4 | Solano Vieira, 2012 | o eco |
| 5 | Noemi Contreiras, 2014 | esteiras com setas repintadas |
| 6 | Selene Amparo, 2016 | a caixa |
| 7 | Aníbal Sobral, 2018 | a pilha |
| 8 | Cássia Mirante, 2020 | a câmera |
| 9 | Otávio Quaresma, 2022 | portas que contam passos |
| 10 | Cobertura | silêncio, o diamante e a assinatura |

### 3.7 Fluxo de jogo

Menu → abertura → dez andares → diamante → assinatura com o mouse → resultado com tempo de cada andar → menu. O menu mostra melhor tempo e permite rejogar qualquer andar já alcançado. Fechar o jogo guarda o progresso.

## 4. Interface de Usuário

### 4.1 Controles

| Ação | Tecla |
|---|---|
| Mover | Setas ou A / D |
| Pular | Espaço, W ou ↑ |
| Acionar / examinar | E |
| Caderno de pistas | C |
| Reiniciar o andar | R |
| Pausar | Esc |
| Som | M |

### 4.2 HUD

Indicador de andar (canto superior esquerdo), cronômetro (canto superior direito), alerta de detecção no cone, tempo das portas acima delas, fita do eco no alto, marcas de canal douradas no mundo, faixa de rádio na parte inferior.

## 5. Áudio

32 efeitos sintetizados por código (`preparar-som.py`, só biblioteca padrão do Python). Faixa ambiente de 64 s em laço. Nenhum arquivo de terceiro.

## 6. Arte

Pixel art em grade de 32 px. Paleta do mundo fechada em 25 cores. Arte gerada com IA (ChatGPT, OpenAI) sob direção de arte da equipe; peças dos andares, interface e cenário desenhados por código. Fontes Silkscreen e VT323 (SIL OFL).

## 7. Especificação Técnica

| Item | Valor |
|---|---|
| Linguagem | Python 3.12 |
| Biblioteca | Power PPlay 2.0 sobre pygame 2.6.1 |
| Tela | Tela cheia na resolução do monitor |
| Tile | 32 × 32 px |
| FPS | 60 |
| Testes | 6 roteiros automáticos sem janela |
| Repositório | https://github.com/Matheus-Azevedo-Abreu/FinalStage |

## 8. Equipe e Divisão de Trabalho

| | Matheus Azevedo Abreu | Gabriel Ribeiro Ota Yida | Enzo Lemos Von Paumgartten Klautau |
|---|---|---|---|
| Código | Versão inicial jogável, menu e primeira integração de sprites | Base reestruturada, mecanismos, dez andares, câmera, testes, som, falas e progresso | Apoio na resolução de bugs |
| Arte | — | Direção da arte gerada por IA | Sprites, assets e direção de arte |
| Documentos | GDD, balanceamento e testes | GDD e documentação técnica | Revisão e contribuição nos documentos |
| Outros | Organização do repositório | Arquitetura do código | Suporte em arte e integração |

## 9. Marcos de Desenvolvimento

| Marco | Entrega | Situação |
|---|---|---|
| M1 | Movimento, colisão, carregador de mapa | ✅ Feito |
| M2 | Porta, botão e transição de andar | ✅ Feito |
| M3 | Alavanca e vínculos mecanismo → porta | ✅ Feito |
| M4 | Caixa empurrável e caixa sobre botão | ✅ Feito |
| M5 | Câmera, cone de visão e detecção | ✅ Feito |
| M6 | Temporizador de porta | ✅ Feito |
| M7 | Cobertura e diamante — jogo mínimo completo | ✅ Feito |
| M8 | Painel de acesso | ❌ Não feito (cortado — expansão) |
| M9 | Diálogo, retratos e briefing | ✅ Feito |
| M10 | Andares de expansão | ❌ Não feito (cortado — expansão) |
| M11 | Áudio, menus, telas de resultado | ✅ Feito |
| M12 | Balanceamento, teste cruzado e polimento | ✅ Feito (teste externo em aberto) |

## 10. Ideias Adicionais e Observações

### 10.1 Andares de expansão

Havendo tempo após o M7, o prédio ganha andares entre o 9 e a cobertura, aprofundando as combinações sem introduzir sistemas novos além do painel de acesso:

| Nº | Andar | O que acrescenta |
|---|---|---|
| 11 | Duas Caixas | Duas caixas, dois botões; a ordem importa |
| 12 | Câmeras Cruzadas | Cones que se cruzam exigem rota calculada |
| 13 | Acesso | Estreia do painel de acesso |
| 14 | Contra o Relógio | Temporizador e câmera na mesma sala |
| 15 | Sala Técnica I | Ambiente novo; alavanca e caixa recombinadas |

### 10.2 Fora do escopo

Os itens abaixo foram avaliados e conscientemente excluídos:

- Avaliação de soft skills (persuasão, liderança) como sistema de jogo.
- Múltiplos desfechos ou ramificações narrativas.
- Derrota por tempo esgotado — o tempo permanece como pontuação.
- Mecânicas adicionais: plataformas móveis, teletransportadores, espelhos, portas de mão única.
- Animação de caminhada antes do marco de polimento.

## 11. O que mudou desde a versão 1.0

| Item | Versão 1.0 | Versão 2.0 | Motivo |
|---|---|---|---|
| Gênero e movimento | Puzzle em grade, 4 direções, um tile por passo | Puzzle e plataforma lateral, com pulo e gravidade | O pulo de 2 tiles e a queda das caixas viraram matéria dos quebra-cabeças (degrau, poço, pilha), que a grade vista de cima não dava |
| Tela e câmera | 640 × 480, sala única, sem rolagem | Tela cheia, andares largos com rolagem | Um andar tem de 3 a 5 salas em sequência; a rolagem permite esconder o que vem depois e mostrar o essencial de cada sala |
| Interagir | Espaço ou E | E; espaço pula | O pulo precisava de tecla própria |
| Premissa | Cinco finalistas competindo | Uma candidata sozinha, a voz no rádio e as placas dos autores | A competição não tinha mecânica que a sustentasse; as placas ligam cada mecanismo a quem o "projetou" e dão sentido ao final |
| Cobertura | Combinação final de todas as mecânicas | Laje aberta, sem mecanismo | A combinação mais difícil ficou no andar 9; o desfecho pede silêncio antes do diamante |
| Painel de acesso | Mecânica do núcleo, marco M8 | Não feito | Pilar "profundidade sobre quantidade": era expansão |
| Personagem | 32 × 32, um tile de colisão | Quadro de 64 × 64, colisor de 16 × 48 | Corpo em pé de plataforma lateral, com animação legível |
| Ferramenta de arte | PixelLab | Gerador de imagem do ChatGPT, com scripts de preparo | Consistência de estilo entre personagem, cenários e interface |
| Áudio | Bibliotecas livres de direitos | Síntese por código do projeto | Nenhuma licença de terceiro a conferir num repositório público |
| Mecânicas | Botão, alavanca, caixa, temporizador, câmera | Uma invenção por autor: gaveta, viga, eco, esteira, caixa, pilha, câmera, passos | O quebra-cabeça de cada andar passa a ser a coisa de quem o projetou |
| Final | Tela de resultado | A jogadora assina a placa com o mouse antes do resultado | A última fala pergunta como ela quer ser gravada; a resposta é de quem joga |
| Progresso | Não previsto | Andar em curso guardado; menu oferece continuar | Fechar o jogo não pode custar a subida |

## 12. O que mudou na versão 2.2

Versão 6 do jogo, de 11 de novembro de 2026.

| Assunto | Versão 2.1 | Versão 2.2 | Motivo |
|---|---|---|---|
| Câmera | Área de detecção retangular de 3 tiles de altura | Cone que sai da lente, inclinado para o chão, cortado por parede e porta fechada; ponto cego logo abaixo da câmera | O retângulo não se parecia com o que uma câmera vê |
| Cenário | Objetos do autor pintados no fundo, sem função | Objetos postos onde o quebra-cabeça acontece; relógio, monitores e lousa mostram o estado do andar | A história passa a fazer parte do quebra-cabeça |
| Pontuação | Pontos pelo tempo e flagrantes, vistos só no fim | Mais 50 pontos por placa de autor lida; pontos na HUD e no cartão de cada andar | A pontuação precisava aparecer durante a noite |
| Ranking | As dez melhores noites, sem nome | As cinco melhores noites, cada uma com a assinatura gravada na placa | O ranking mostra quem fez cada noite |
| Treino | Cinco salas sem texto | Doze salas, uma por mecanismo, com a lição escrita | O treino não explicava nada |
| Final | Assinatura e uma pintura parada da placa sendo gravada | Assinatura, placa com reflexo, resultado gravado linha a linha, créditos e ranking | A pintura mostrava uma mão gravando o que a jogadora já tinha gravado |
| Controles | ESPAÇO pula e, segurado, repete | ESPAÇO, W ou ↑ pulam na descida da tecla; segurar não repete | No andar 9 cada pulo custa passos |

## 13. O que mudou na versão 2.3

Versão 7 do jogo, de 18 de novembro de 2026.

| Assunto | Versão 2.2 | Versão 2.3 | Motivo |
|---|---|---|---|
| Quebra-cabeça | Só de mecanismo: chegar à saída bastava | Cada andar de 1 a 9 tem pistas do autor e uma tranca de segredo; a saída depende dela | Os quebra-cabeças eram só de plataforma; faltava raciocínio e ligação com a história |
| História | Placas, rádio e cenário; ler era opcional | As pistas dos autores entregam a história, e o segredo de cada andar sai delas | A jogadora aprende quem fez o andar para conseguir sair dele |
| Controles | E mexe | E também examina; C abre o caderno; na tranca, A D, W S, algarismos e ENTER | — |
| Tempo | Corre sempre | Para com pista, tranca ou caderno aberto | Ler e pensar não podem custar pontos |
| Pontuação | Tempo, flagrantes e placas | Mais 25 por pista lida, menos 30 por segredo errado | A investigação também é anotada |
| Andar 8 | Olhar pelos monitores era opcional | A porta da primeira sala pede o algarismo que cada câmera acende, e só se lê pelos monitores | Quem não descobria os monitores não via as câmeras |
| Arte | — | Objetos das pistas, tranca, folhas de leitura, figuras e setas repintadas, por código, na paleta do jogo | Sem gerador de imagem ao alcance; o estilo segue o das peças já feitas por código |

## 14. Situação do jogo na data de entrega (20/11/2026)

O jogo está completo e jogável do início ao fim. Todos os dez andares funcionam, com quebra-cabeças de mecanismo e de investigação (pistas dos autores e trancas de segredo). Os sistemas principais estão implementados e testados por roteiros automáticos sem janela.

**O que está funcionando:**
- Dez andares jogáveis do início ao fim, incluindo treino
- Todos os mecanismos: gaveta, viga, eco, esteira, caixa, pilha, câmera, porta de passos, botão, alavanca, porta de relógio
- Sistema de investigação: pistas dos autores, trancas de segredo e caderno
- Câmera com cone de visão real (não mais retangular)
- Pontuação por tempo, flagrantes, placas lidas e segredos
- Ranking com assinatura da jogadora
- Progressão salva entre sessões
- Áudio completo: 32 efeitos + faixa ambiente
- Falas da Selene e da Íris
- Treino com lições escritas por mecanismo
- Peças de cenário por andar, ligadas ao autor de cada fase
- Scripts de geração de assets, trailer e zip de entrega

**O que ficou de fora (decisão tomada durante o projeto):**
- Painel de acesso (marco M8): cortado no início como expansão
- Andares de expansão entre o 9 e a cobertura (marco M10): cortado como expansão
- Teste com jogadores externos: em aberto
- Arquivo de licença no repositório: pendente

**Pendências de publicação (a concluir até 24/11):**
- Configurar ambiente Python 3.12 e rodar os scripts de preparação de assets
- Gerar `final-stage.zip` com `preparar-entrega.py`
- Publicar no itch.io
- Subir teaser no YouTube
- Fazer commit/push da versão final no GitHub
- Enviar formulário da galeria do PPlay

## 15. O que dissemos que faríamos × o que foi feito

| O que estava planejado | Foi feito? | Observação |
|---|---|---|
| Jogo de puzzle com movimento em 4 direções e grade | ❌ Mudou | Virou plataforma lateral com pulo e gravidade — a mudança enriqueceu os quebra-cabeças |
| Tela fixa de 640 × 480 | ❌ Mudou | Tela cheia com rolagem lateral — necessário para andares com 3 a 5 salas em sequência |
| Cinco finalistas competindo no mesmo prédio | ❌ Mudou | Uma candidata sozinha com voz no rádio — a competição não tinha mecânica que a sustentasse |
| Dez andares jogáveis | ✅ Feito | Todos os dez andares implementados e testados |
| Mecânicas: botão, alavanca, caixa, temporizador, câmera | ✅ Feito | E mais: gaveta, viga, eco, esteira, pilha, porta de passos |
| Painel de acesso (minijogo de lógica) | ❌ Cortado | Decisão de equipe: "profundidade sobre quantidade"; era expansão |
| Andares de expansão | ❌ Cortado | Mesma decisão; os dez andares ficaram mais densos no lugar |
| Personagem de 32 × 32 px | ❌ Mudou | 64 × 64 com colisor de 16 × 48 — necessário para plataforma lateral com animações legíveis |
| Arte feita no PixelLab | ❌ Mudou | Gerada com IA (ChatGPT) sob direção da equipe, processada por scripts do projeto |
| Áudio com bibliotecas livres de terceiros | ❌ Mudou | Todo áudio sintetizado por código próprio — sem nenhuma licença de terceiro a conferir |
| Sistema de pontuação por tempo | ✅ Feito | Tempo + flagrantes + placas lidas + acertos/erros de segredo |
| Tela de resultado ao fim | ✅ Feito | Com assinatura da jogadora com o mouse, placar por andar e ranking |
| Progressão salva | ✅ Feito | Andar em curso e melhores tempos guardados em arquivo |
| Cobertura com combinação de todas as mecânicas | ❌ Mudou | Laje aberta e silenciosa — a combinação mais difícil ficou no andar 9; o desfecho pede silêncio |
| Diálogo e retratos dos personagens | ✅ Feito | Falas da Selene (rádio) e da Íris; retratos em cinco expressões |
| Treino inicial | ✅ Feito | Doze salas, uma por mecanismo, com lição escrita; fora da numeração dos andares |
| Teste com jogadores externos | ⬜ Em aberto | Ficha preparada em `docs/teste-com-jogadores.md`; execução não realizada |
| Sistema de investigação (pistas e trancas) | ✅ Feito | Adicionado na versão 2.3; pistas dos autores, trancas de segredo e caderno em todos os andares 1–9 |
| Cone de visão real nas câmeras | ✅ Feito | Substituiu a área retangular; cone geométrico com ponto cego, cortado por paredes e portas |
| Cenário ligado ao autor de cada andar | ✅ Feito | Cada andar tem peças próprias que contam quem o projetou |
| Créditos com os três integrantes da equipe | ✅ Feito | Matheus, Gabriel e Enzo creditados no jogo e no README |
