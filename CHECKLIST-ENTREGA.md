# Final Stage — Checklist de Entrega (24/11)

Equipe: Matheus Azevedo Abreu · Gabriel Ribeiro Ota Yida · Enzo Lemos Von Paumgartten Klautau  
Repositório: https://github.com/Matheus-Azevedo-Abreu/FinalStage

---

## O que entregar ao professor

| Item | Situação | O que fazer |
|---|---|---|
| Link do jogo no itch.io | ⬜ FALTA PUBLICAR | Ver seção 1 abaixo |
| Link do teaser no YouTube | ⬜ FALTA PUBLICAR | Ver seção 2 abaixo |
| Projeto completo no GitHub | ⬜ FALTA commit/push da versão final | Ver seção 3 abaixo |
| GDD atualizado | ✅ Pronto | `final-stage-gdd-v2.pdf` nesta pasta |
| Publicação na página do PPlay | ⬜ FALTA (fazer após o itch.io) | Ver seção 4 abaixo |

---

## 1. Publicar no itch.io

Acesse https://itch.io/game/new e preencha:

- **Title:** Final Stage
- **Short description:** Suba dez andares sem ser vista. Puzzle-plataforma em pixel art sobre a última etapa de um processo seletivo.
- **Kind of project:** Downloadable · **Release status:** Released · **Pricing:** No payments
- **Uploads:** `final-stage.zip` (gerar — ver seção 5), marcado para Windows, macOS e Linux
- **Cover image:** `capa-itch-630x500.png` (nesta pasta)
- **Genre:** Puzzle · **Tags:** puzzle-platformer, pixel-art, 2d, stealth, singleplayer, pygame, portuguese
- **Gameplay video:** link do YouTube (após publicar o teaser)
- **Visibility:** Public

**Descrição para colar:**

> **A sétima etapa não é entrevista.**
>
> Íris Portela passou por seis etapas do processo seletivo da Vértice. A última acontece à noite, no prédio, e ela vai sozinha: no topo há um diamante, e a vaga é de quem chegar até ele. A segurança fica ligada. Se uma câmera enxergar você por um segundo inteiro, o andar recomeça. O tempo é anotado. Não elimina. É só anotado.
>
> **Final Stage** é um puzzle-plataforma 2D em pixel art com dez andares. Cada andar foi projetado por alguém que passou antes de você, e cada um deixou a sua invenção: gavetas que fecham sozinhas, vigas de ferro que três alavancas deslocam, um eco que repete o que você fez, esteiras que lançam quem pula, caixas, câmeras e portas que contam os seus passos.
>
> - 10 andares, do saguão à cobertura  
> - nenhum tutorial em texto: você aprende mexendo  
> - errar nunca custa mais que o andar; R recomeça na hora  
> - o tempo é a pontuação: melhor marca guardada por andar e no total  
> - uma voz gentil no rádio que nunca dá a resposta  
> - no fim, você assina a placa com o mouse  
>
> **Controles:** setas ou A/D para andar · espaço para pular · E para acionar · R reinicia o andar · Esc pausa · M som
>
> **Como jogar:** baixe e extraia o zip. No Windows, dois cliques em `jogar.bat`; no macOS, em `jogar.command`. Precisa do Python 3.12 (python.org); na primeira vez o lançador instala o pygame. Ou no terminal: `pip install pygame==2.6.1` e `python main.py`.
>
> Projeto final de Laboratório de Introdução à Programação (UFF, 2026), Prof. Esteban Clua.  
> Por Matheus Azevedo Abreu, Gabriel Ribeiro Ota Yida e Enzo Lemos Von Paumgartten Klautau.  
> Código: https://github.com/Matheus-Azevedo-Abreu/FinalStage

---

## 2. Publicar o teaser no YouTube

- **Arquivo:** `entrega/teaser.mp4` dentro do projeto (gerar se não existir — ver seção 5)
- **Título:** Final Stage — teaser (puzzle-plataforma em Python/PPlay, UFF 2026)
- **Visibilidade:** Não listado ou Público
- **Descrição para colar:**

> A sétima etapa do processo seletivo não é entrevista. Suba dez andares, não seja vista, pegue o diamante. O tempo é anotado.
>
> Final Stage é um puzzle-plataforma 2D em pixel art feito em Python com a PPlay, projeto final de Laboratório de Introdução à Programação (UFF, 2026, Prof. Esteban Clua).
> Por Matheus Azevedo Abreu, Gabriel Ribeiro Ota Yida e Enzo Lemos Von Paumgartten Klautau.
>
> Jogue: (colar link do itch.io)  
> Código: https://github.com/Matheus-Azevedo-Abreu/FinalStage

---

## 3. Commit e push do repositório

No terminal, dentro de `FinalStage-main`:

```bash
git add -A
git commit -m "versão final — entrega 24/11"
git push origin main
```

Após o push, o link do repositório para entregar é:
**https://github.com/Matheus-Azevedo-Abreu/FinalStage**

---

## 4. Publicar na página do PPlay

Formulário: https://www2.ic.uff.br/pplay/submeter-jogo/
(Verificar com as instruções que o professor enviou — elas prevalecem)

- **Nome do jogo:** Final Stage
- **Resumo:** Puzzle-plataforma em pixel art. Íris enfrenta a última etapa de um processo seletivo: subir dez andares à noite e pegar o diamante da cobertura. Cada andar tem a invenção de quem o projetou: gavetas, vigas, um eco, esteiras, câmeras. O tempo é a pontuação.
- **Imagem principal:** `capa-pplay-1280x800.png` (nesta pasta)
- **Link para jogar:** link do itch.io
- **Nome ou equipe:** Matheus Azevedo Abreu, Gabriel Ribeiro Ota Yida e Enzo Lemos Von Paumgartten Klautau
- **Gênero:** Puzzle / Plataforma
- **Controles:** Setas ou A/D andam, espaço pula, E aciona, R reinicia, Esc pausa, M som
- **Código-fonte:** https://github.com/Matheus-Azevedo-Abreu/FinalStage
- **Trailer:** link do YouTube
- **Turma/curso:** Laboratório de Introdução à Programação, UFF, 2026-2

---

## 5. Gerar o zip e o teaser (precisa do jogo rodando)

Após configurar o ambiente (Python 3.12 + pygame), rode dentro de `FinalStage-main`:

```bash
.venv/bin/python preparar-arte.py
.venv/bin/python preparar-temas.py
.venv/bin/python preparar-interface.py
.venv/bin/python preparar-cenario.py
.venv/bin/python preparar-fundos.py
.venv/bin/python preparar-mobilia.py
.venv/bin/python preparar-som.py
.venv/bin/python preparar-investigacao.py

# gravar a partida para o teaser (~2 min):
.venv/bin/python testes/testar_partida.py --video entrega/partida.mp4 1920 1080

# montar teaser (60 s) e zip:
.venv/bin/python preparar-trailer.py
.venv/bin/python preparar-entrega.py
```

O zip `entrega/final-stage.zip` e o teaser `entrega/teaser.mp4` estarão prontos.
Copie o zip para esta pasta `entrega-24-11/`.

---

## Arquivos nesta pasta

| Arquivo | O que é |
|---|---|
| `final-stage-gdd-v2.pdf` | GDD para entregar ao professor |
| `final-stage-gdd-v2.docx` | GDD fonte editável |
| `capa-itch-630x500.png` | Capa para o itch.io |
| `capa-pplay-1280x800.png` | Capa para a galeria do PPlay |
| `cartao-final.png` | Cartão visual do jogo |
| `final-stage.zip` | ⬜ FALTA GERAR (ver seção 5) |
| `teaser.mp4` | ⬜ FALTA GERAR (ver seção 5) |
