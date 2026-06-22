"""
config.py
---------
Arquivo de configuração central do jogo.

Aqui ficam reunidos todos os "números mágicos" e valores fixos usados
pelo jogo: dimensões da tela, paleta de cores, caminhos de arquivos e
parâmetros de balanceamento (velocidade, vidas, pontuação, etc.).

Centralizar essas constantes facilita ajustar a dificuldade ou a
aparência do jogo sem precisar mexer na lógica em si (jogo.py).
"""

# ---------------------------------------------------------------------------
# Janela e tempo
# ---------------------------------------------------------------------------
LARGURA, ALTURA = 360, 520          # dimensões da janela do jogo, em pixels
FPS = 60                            # quadros por segundo (velocidade do loop)
TITULO_JOGO = "Nave Infinita - Prototipo"

# ---------------------------------------------------------------------------
# Paleta de cores (RGB)
# ---------------------------------------------------------------------------
FUNDO    = (5, 8, 15)        # cor de fundo do espaço (quase preto)
VERDE    = (93, 202, 165)    # textos de sucesso / temporizador
VERMELHO = (226, 75, 74)     # balas inimigas / dano / game over
AMARELO  = (250, 199, 117)   # balas do jogador / destaques do HUD
BRANCO   = (220, 220, 220)   # texto padrão do HUD
CINZA    = (120, 120, 130)   # textos secundários (onda, instruções)
LARANJA  = (245, 166, 35)    # partículas de explosão / fogo

# ---------------------------------------------------------------------------
# Caminhos de arquivos
# ---------------------------------------------------------------------------
CAMINHO_RECORDE = "data/recorde.txt"   # arquivo onde o recorde é salvo

# Os PNGs abaixo fazem parte do projeto (pasta assets/imagens), mas não são
# carregados diretamente: todos os sprites do jogo são desenhados em código
# em src/sprites.py (usando pygame.draw), o que evita depender de arquivos
# externos para rodar o protótipo. Os caminhos ficam aqui apenas como
# referência caso o grupo queira voltar a usar imagens no futuro.
CAMINHO_SPRITE_JOGADOR     = "assets/imagens/nave.png"
CAMINHO_SPRITE_INIMIGO     = "assets/imagens/nave_inimiga.png"
CAMINHO_SPRITE_OBSTACULO1  = "assets/imagens/obstaculo1.png"
CAMINHO_SPRITE_OBSTACULO2  = "assets/imagens/obstaculo2.png"

# ---------------------------------------------------------------------------
# Tamanho dos sprites na tela (em pixels, sprite quadrado/retangular)
# ---------------------------------------------------------------------------
# Nave do jogador: maior que os demais elementos, para ficar bem visível.
TAMANHO_JOGADOR_W = 48
TAMANHO_JOGADOR_H = 56

# Nave inimiga (atira contra o jogador).
TAMANHO_INIMIGO = 38

# Obstáculos (asteroides/destroços que NÃO atiram, só colidem).
# Aumentados em relação à nave inimiga para deixá-los mais ameaçadores
# visualmente e exigir desvios mais precisos do jogador.
TAMANHO_OBSTACULO = 50

# Mantido por compatibilidade com versões anteriores do código
# (era usado tanto para inimigos quanto obstáculos).
TAMANHO_SPRITE = TAMANHO_INIMIGO

# ---------------------------------------------------------------------------
# Parâmetros de balanceamento do jogo
# ---------------------------------------------------------------------------
VIDAS_INICIAIS = 3              # vidas com que o jogador começa a partida
PONTOS_POR_INIMIGO = 10         # pontos ganhos ao destruir uma nave inimiga
                                 # (obstáculos valem metade disso, ver funcoes.py)

SPAWN_INTERVAL_INICIAL = 90     # frames entre spawns no início (quanto menor, mais rápido)
SPAWN_INTERVAL_MINIMO = 40      # piso de dificuldade: o spawn nunca fica mais rápido que isso

DESTRUIDOS_POR_ONDA = 8         # quantos alvos destruídos são necessários para subir de onda
