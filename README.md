# Ethnos

Jogo de tabuleiro digital inspirado em Ethnos, feito em Python com pygame.

O projeto foi preparado para rodar com Python 3.12.9 e possui suporte para execucao local e via Docker.

## Visao geral

O aplicativo abre uma interface grafica com menu inicial, configuracao das tribos dos 4 jogadores e a partida em si.

Arquivos principais:

- `ethnos.py`: ponto de entrada da aplicacao.
- `classes/`: regras do jogo, entidades, renderizacao e interface.
- `ethnos/`: imagens, mapa e dados das cartas.
- `Dockerfile`: imagem pronta com Python 3.12.9.
- `requirements.txt`: dependencia Python do projeto.

## Requisitos

### Execucao local

- Python 3.12.9
- pip
- Ambiente grafico para abrir a janela do jogo

### Execucao com Docker

- Docker instalado
- Para ver a janela do jogo, voce precisa de suporte a interface grafica no host

## Como rodar localmente

Na raiz do repositorio, crie e ative um ambiente virtual e instale as dependencias:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Depois inicie o jogo:

```powershell
python ethnos.py
```

Importante: execute o comando sempre na raiz do repositorio para que os imports relativos e os assets da pasta `ethnos/` sejam encontrados corretamente.

## Como rodar com Docker

A imagem ja fixa a versao do Python em 3.12.9.

Build da imagem:

```powershell
docker build -t ethnos .
```

Execucao:

```powershell
docker run --rm -it ethnos
```

Se o seu ambiente nao tiver display grafico disponivel, o container sobe com Xvfb apenas para inicializacao. Nesse caso, a janela nao aparece na tela do host.

## Fluxo de uso

1. Abra o jogo.
2. No menu inicial, clique em iniciar.
3. Na tela de setup, escolha a tribo de cada um dos 4 jogadores.
4. Clique em iniciar a partida.
5. No seu turno, use os botoes da interface para comprar do baralho, comprar do mercado, jogar um bando ou passar a vez.
6. Quando necessario, selecione as cartas na mao e confirme a jogada.
7. Ao final de uma era, avance para a proxima ou veja o resultado final.

## Controles principais

- Mouse: interacao principal com a interface.
- `ESC`: sai do jogo ou volta da tela de setup para o menu.
- `R`: na tela de fim de jogo, volta para o menu.

## Regras de uso dentro da interface

- O jogo trabalha com 4 jogadores locais.
- Cada jogador escolhe uma tribo na tela de setup.
- A mao de cartas tem limite de 10 cartas.
- Para jogar bando, selecione apenas cartas validas da mao e confirme a acao.
- Se houver mais de uma carta no bando, e necessario escolher um lider.

## Estrutura do projeto

- `classes/app.py`: loop principal da aplicacao.
- `classes/jogo.py`: regras de partida, turnos e pontuacao.
- `classes/tabuleiro.py`: baralho, mercado e dragoes.
- `classes/renderer.py`: desenho da interface.
- `classes/jogador.py`: estado do jogador.
- `classes/tribo.py`: habilidades das tribos.
- `classes/reino.py`: dados dos reinos.

## Observacoes

- Se a interface nao abrir no Docker, o caminho mais simples e rodar localmente com Python 3.12.9.
- Se voce quiser distribuir o projeto, envie junto a pasta `ethnos/`, pois ela contem os assets usados pelo jogo.

## Comandos rapidos

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ethnos.py
```

```powershell
docker build -t ethnos .
docker run --rm -it ethnos
```