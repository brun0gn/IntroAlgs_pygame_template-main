"""
sprites.py
----------
Geração das imagens (sprites) usadas no jogo.

Em vez de carregar arquivos PNG externos, cada sprite é desenhado
diretamente em código usando as primitivas de desenho do pygame
(pygame.draw.polygon, .circle, .ellipse, .rect). Essa abordagem deixa
o protótipo independente de arquivos de imagem: ele roda em qualquer
máquina só com o código-fonte, sem precisar copiar a pasta assets/.

Cada função "criar_sprite_*" devolve uma Surface (uma "folha" onde foi
desenhado o sprite) com fundo transparente (pygame.SRCALPHA).
"""

import pygame

from src.config import TAMANHO_INIMIGO, TAMANHO_OBSTACULO


# ===========================================================================
# Nave do jogador
# ===========================================================================

def criar_sprite_jogador():
    """Desenha a nave do jogador: um caça azul/branco apontado para cima."""
    W, H = 48, 56
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    AZUL_ESCURO = (30,  90, 200)
    AZUL_CLARO  = (80, 160, 255)
    BRANCO      = (220, 230, 255)
    BRANCO_PURO = (255, 255, 255)
    CINZA_AZUL  = (140, 170, 220)
    AMARELO     = (255, 220,  60)

    cx = W // 2

    # Corpo principal (triângulo apontando para cima)
    pygame.draw.polygon(s, AZUL_ESCURO, [(cx, 2), (4, H - 10), (W - 4, H - 10)])
    # Miolo branco (detalhe central do corpo)
    pygame.draw.polygon(s, BRANCO, [(cx, 6), (cx - 10, H - 18), (cx + 10, H - 18)])
    # Asas laterais
    pygame.draw.polygon(s, AZUL_CLARO, [(4, H - 10), (0, H - 2), (cx - 6, H - 14)])
    pygame.draw.polygon(s, AZUL_CLARO, [(W - 4, H - 10), (W, H - 2), (cx + 6, H - 14)])
    # Contorno do corpo
    pygame.draw.polygon(s, CINZA_AZUL, [(cx, 2), (4, H - 10), (W - 4, H - 10)], 1)
    # Cockpit (cabine do piloto)
    pygame.draw.ellipse(s, AZUL_CLARO, (cx - 6, 10, 12, 16))
    pygame.draw.ellipse(s, BRANCO_PURO, (cx - 6, 10, 12, 16), 1)
    # Motores (caixas na traseira)
    pygame.draw.rect(s, CINZA_AZUL, (cx - 14, H - 12, 10, 8), border_radius=2)
    pygame.draw.rect(s, CINZA_AZUL, (cx + 4,  H - 12, 10, 8), border_radius=2)
    # Chamas dos motores
    pygame.draw.ellipse(s, AMARELO, (cx - 12, H - 8, 6, 10))
    pygame.draw.ellipse(s, AMARELO, (cx + 6,  H - 8, 6, 10))

    return s


# ===========================================================================
# Nave inimiga (desce atirando contra o jogador)
# ===========================================================================

def criar_sprite_inimigo():
    """Desenha a nave inimiga: um losango vermelho com núcleo brilhante."""
    W = H = TAMANHO_INIMIGO
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    VERMELHO      = (220,  60,  60)
    VERMELHO_ESC  = (140,  20,  20)
    LARANJA       = (255, 140,   0)

    cx, cy = W // 2, H // 2

    # Corpo em formato de losango
    pygame.draw.polygon(s, VERMELHO, [(cx, 2), (W - 2, cy), (cx, H - 2), (2, cy)])
    # Borda escura (contorno)
    pygame.draw.polygon(s, VERMELHO_ESC, [(cx, 2), (W - 2, cy), (cx, H - 2), (2, cy)], 2)
    # Núcleo central (parece um "olho"/canhão)
    pygame.draw.circle(s, LARANJA, (cx, cy), 5)
    pygame.draw.circle(s, (255, 220, 180), (cx, cy), 2)

    return s


# ===========================================================================
# Obstáculos (descem em direção ao jogador, mas NÃO atiram)
# ===========================================================================
# Os dois tipos de obstáculo usam o mesmo tamanho (TAMANHO_OBSTACULO),
# maior que o da nave inimiga, para ficarem mais visíveis e ameaçadores.

def criar_sprite_obstaculo1():
    """Desenha o obstáculo 1: um asteroide de rocha cinza, irregular."""
    W = H = TAMANHO_OBSTACULO
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    CINZA_ESC  = ( 80,  80,  90)
    CINZA      = (120, 120, 130)
    CINZA_CLR  = (160, 160, 170)

    cx, cy = W // 2, H // 2

    # Forma irregular (octógono distorcido) escalada proporcionalmente
    # ao tamanho definido em config.py, para manter o mesmo "desenho"
    # independente do tamanho final do sprite.
    pontos = [
        (cx,           int(H * 0.07)),
        (int(W * 0.86), int(H * 0.21)),
        (int(W * 0.93), cy),
        (int(W * 0.82), int(H * 0.89)),
        (cx,            int(H * 0.93)),
        (int(W * 0.11), int(H * 0.82)),
        (int(W * 0.07), cy),
        (int(W * 0.18), int(H * 0.14)),
    ]
    pygame.draw.polygon(s, CINZA, pontos)
    pygame.draw.polygon(s, CINZA_ESC, pontos, 2)

    # Detalhes de textura (crateras)
    raio_a = max(2, int(W * 0.11))
    raio_b = max(2, int(W * 0.07))
    pygame.draw.circle(s, CINZA_CLR, (cx - int(W * 0.14), cy - int(H * 0.11)), raio_a)
    pygame.draw.circle(s, CINZA_ESC, (cx + int(W * 0.14), cy + int(H * 0.11)), raio_b)

    return s


def criar_sprite_obstaculo2():
    """
    Desenha o obstáculo 2: um asteroide de rocha marrom, irregular,
    como uma variação visual do obstaculo1 (mesma forma, paleta diferente).
    """
    W = H = TAMANHO_OBSTACULO
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    MARROM_ESC = ( 90,  60,  30)
    MARROM     = (140,  90,  50)
    MARROM_CLR = (180, 130,  80)

    cx, cy = W // 2, H // 2

    # Forma irregular (hexágono distorcido) escalada proporcionalmente
    # ao tamanho definido em config.py.
    pontos = [
        (cx,            int(H * 0.11)),
        (int(W * 0.82), int(H * 0.25)),
        (int(W * 0.89), int(H * 0.79)),
        (cx,            int(H * 0.89)),
        (int(W * 0.14), int(H * 0.75)),
        (int(W * 0.11), int(H * 0.29)),
    ]
    pygame.draw.polygon(s, MARROM, pontos)
    pygame.draw.polygon(s, MARROM_ESC, pontos, 2)

    # Detalhes de textura (crateras)
    raio_a = max(2, int(W * 0.14))
    raio_b = max(2, int(W * 0.07))
    pygame.draw.circle(s, MARROM_CLR, (cx + int(W * 0.11), cy - int(H * 0.14)), raio_a)
    pygame.draw.circle(s, MARROM_ESC, (cx - int(W * 0.11), cy + int(H * 0.14)), raio_b)

    return s


# ===========================================================================
# Carregamento conjunto
# ===========================================================================

def carregar_sprites_do_jogo():
    """
    Gera todos os sprites do jogo de uma vez e retorna em um dicionário,
    facilitando o acesso em jogo.py (ex.: sprites["jogador"]).
    """
    return {
        "jogador":    criar_sprite_jogador(),
        "inimigo":    criar_sprite_inimigo(),
        "obstaculo1": criar_sprite_obstaculo1(),
        "obstaculo2": criar_sprite_obstaculo2(),
    }


def girar_sprite(imagem, angulo):
    """Retorna uma cópia da imagem rotacionada pelo ângulo informado (graus)."""
    return pygame.transform.rotate(imagem, angulo)
