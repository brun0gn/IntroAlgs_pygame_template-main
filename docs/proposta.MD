# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

> Nave Infinita

## 2. Integrantes do grupo

- Bruno Gonçalves Belo
- Francisco Carvalho Borges
- Sadee Torres Queiroz

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Jogo de nave com tiro e desvio de obstáculos (shoot 'em up vertical).

## 4. Descrição geral do jogo

Descrição:

> Na tela aparece uma nave espacial controlada pelo jogador, naves inimigas que descem disparando projéteis e asteroides que descem em direção ao jogador. O jogador move a nave livremente pela tela usando o teclado e atira para destruir os inimigos. Os desafios são os projéteis disparados pelas naves inimigas, a colisão direta com inimigos e asteroides, e o aumento progressivo de velocidade e frequência de spawn a cada onda.

## 5. Objetivo do jogador

Objetivo:

> Sobreviver pelo maior tempo possível, destruindo naves inimigas e asteroides para acumular pontos e superar o recorde salvo.

## 6. Regras principais

Regras do grupo:

- Regra 1: O jogador começa com 3 vidas.
- Regra 2: Destruir uma nave inimiga vale 10 pontos; destruir um asteroide vale 5 pontos.
- Regra 3: Colidir com uma bala inimiga, uma nave inimiga ou um asteroide remove 1 vida.
- Regra 4: A partida termina quando o jogador perde todas as vidas.
- Regra 5: A cada 8 alvos destruídos o jogo avança de onda, aumentando a velocidade e a frequência dos inimigos.

## 7. Condição de vitória

Condição de vitória:

> O jogo não tem fim definido: o jogador busca sempre superar o próprio recorde de pontuação. A partida é infinita enquanto o jogador tiver vidas.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> A partida termina quando o jogador perde as 3 vidas. Ao perder a última vida, a nave explode com uma animação de partículas e a tela de game over é exibida com a pontuação final e o recorde.

## 9. Elementos previstos no jogo

### Jogador ou elemento principal

> Uma nave espacial azul e branca controlada pelo teclado, que pode se mover em quatro direções e disparar projéteis para cima.

### Obstáculos, inimigos ou desafios

> Dois tipos de elementos vêm do topo da tela em posições aleatórias: naves inimigas (losango vermelho), que descem atirando projéteis contra o jogador; e asteroides (dois tipos de rocha, cinza e marrom), que descem em direção ao jogador mas não atiram. A velocidade e a frequência de aparição aumentam a cada onda.

### Itens, alvos ou objetos de interação

> Naves inimigas e asteroides são os alvos do jogador. Destruí-los com projéteis concede pontos.

### Pontuação, vidas, tempo ou progresso

> O jogador começa com 3 vidas. A pontuação aumenta ao destruir inimigos (10 pontos) e asteroides (5 pontos). Um temporizador exibe o tempo de sobrevivência em formato MM:SS. O recorde é salvo em arquivo e exibido no HUD durante a partida e na tela de game over.

## 10. Controles previstos

Controles do grupo:

- W / Seta para cima: mover a nave para cima
- S / Seta para baixo: mover a nave para baixo
- A / Seta para esquerda: mover a nave para esquerda
- D / Seta para direita: mover a nave para direita
- Espaço: disparar projétil
- Enter: iniciar ou reiniciar a partida

## 11. Organização inicial do código

Organização planejada:

- `main.py`: ponto de entrada, chama `executar_jogo()`;
- `src/jogo.py`: contém o loop principal, a lógica de atualização (movimentação, spawn, colisões, ondas) e o desenho de todos os elementos na tela;
- `src/config.py`: guarda configurações centrais como tamanho da tela, cores, tamanhos de sprites e parâmetros de balanceamento;
- `src/funcoes.py`: contém funções auxiliares puras (cálculo de pontos, colisão, partículas, formatação de tempo);
- `src/sprites.py`: contém funções que desenham cada sprite do jogo com `pygame.draw`;
- `src/dados.py`: contém funções de leitura e escrita do recorde em arquivo texto.

## 12. Recursos externos previstos

Recursos previstos:

> Não pretendemos utilizar recursos externos. Todos os sprites são desenhados em código com as primitivas do pygame, sem depender de arquivos de imagem ou sons externos.

## 13. Principais dificuldades esperadas

Dificuldades previstas:

- Dificuldade 1: Implementar a detecção de colisão corretamente entre todos os elementos (balas do jogador, balas inimigas, naves e asteroides).
- Dificuldade 2: Balancear a dificuldade progressiva das ondas para que o jogo fique desafiador sem ficar injogável rapidamente.
- Dificuldade 3: Organizar o código em módulos separados de forma que as funções sejam independentes e fáceis de testar.

## 14. Escopo mínimo para a entrega final

Escopo mínimo:

> A versão mínima do jogo terá uma nave controlada pelo teclado, sistema de tiro, naves inimigas e asteroides aparecendo na tela, sistema de vidas, sistema de pontuação, temporizador, recorde salvo em arquivo e tela de game over.

## 15. Possíveis melhorias, caso haja tempo

Melhorias possíveis:

- Melhoria 1: Adicionar efeitos sonoros (tiro, explosão, trilha de fundo).
- Melhoria 2: Adicionar power-ups coletáveis (tiro duplo, escudo temporário, vida extra).
- Melhoria 3: Criar um ranking com as melhores pontuações salvas em arquivo, exibido na tela inicial.