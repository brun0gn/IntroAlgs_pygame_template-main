# Nave Infinita

Projeto da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

## Integrantes do grupo

- Bruno Gonçalves Belo
- Francisco Carvalho Borges
- Sadee Torres Queiroz

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo.
  - `jogo.py`: loop principal, lógica e desenho.
  - `funcoes.py`: funções auxiliares (pontuação, colisão, partículas, tempo).
  - `sprites.py`: geração dos sprites (jogador, inimigo, obstáculos) desenhados proceduralmente com `pygame.draw`.
  - `dados.py`: leitura e gravação do recorde.
  - `config.py`: configurações centrais (tela, cores, caminhos, parâmetros).
- `assets/imagens/`: imagens PNG originais (não usadas no momento; os sprites atuais são gerados em código no `sprites.py`).
- `data/recorde.txt`: arquivo persistente com o recorde de pontuação.
- `tests/`: testes unitários com `pytest`.

## Descrição do jogo

Nave Infinita é um jogo de nave estilo *shoot 'em up* vertical e infinito. O jogador controla uma nave que se move pela tela e atira contra naves inimigas que descem disparando, enquanto também precisa evitar obstáculos que vêm em sua direção (e que não atiram).

## Objetivo do jogador

Sobreviver o máximo de tempo possível, destruir naves inimigas e obstáculos para ganhar pontos, e tentar superar o recorde salvo.

## Regras do jogo

- O jogador se move com **WASD** ou **setas direcionais**.
- **Espaço** dispara um projétil para cima.
- Naves inimigas (vermelhas) descem disparando contra o jogador.
- Obstáculos (sprites `obstaculo1`/`obstaculo2`, desenhados em código) descem revezando entre si e **não atiram**, mas causam dano em colisão direta. Eles são desenhados maiores que as naves inimigas, para serem mais visíveis e exigir desvios mais precisos.
- Acertar uma nave inimiga ou obstáculo com tiro destrói o alvo e soma pontos.
- Colidir com balas inimigas, naves ou obstáculos reduz **1 vida**.
- Ao perder as **3 vidas**, a nave do jogador explode (animação de partículas) e o jogo termina.
- O recorde é salvo automaticamente em `data/recorde.txt` sempre que superado.
- Um temporizador (MM:SS) é exibido durante a partida.
- A dificuldade aumenta progressivamente (ondas): a cada **8 alvos destruídos** (multiplicado pela onda atual), o jogo avança de onda, deixando inimigos e obstáculos mais rápidos e o intervalo de spawn menor.

## Controles

| Tecla | Ação |
|---|---|
| W / ↑ | Mover para cima |
| S / ↓ | Mover para baixo |
| A / ← | Mover para esquerda |
| D / → | Mover para direita |
| Espaço | Atirar |
| Enter | Iniciar / reiniciar |

## Como executar o projeto

```bash
pip install -r requirements.txt
python main.py
```

(Caso `pip`/`python` não sejam reconhecidos no Windows, use `py -m pip install -r requirements.txt` e `py main.py`, ou reinstale o Python marcando "Add Python to PATH".)

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- [x] Loop principal funcionando com `python main.py`
- [x] Controle de movimentação da nave (WASD/setas) e tiro (espaço)
- [x] Sprites do jogador, nave inimiga e obstáculos
- [x] Colisão entre balas, naves inimigas, obstáculos e jogador
- [x] Animação de explosão do jogador (partículas)
- [x] Sistema de recorde persistente
- [x] Temporizador de partida
- [x] Código organizado em módulos/funções
- [x] Testes unitários passando com `pytest`
- [x] Preencher nomes dos integrantes no README
