"""
funcoes.py
----------
Funções auxiliares e "puras" do jogo: recebem dados, fazem um cálculo e
devolvem um resultado, sem desenhar nada na tela e sem depender do
pygame. Isso facilita testar essas funções isoladamente (ver tests/).

As funções estão agrupadas por assunto:
  1) Pontuação e vida
  2) Colisão
  3) Geração de posições (spawns)
  4) Partículas (usadas na animação de explosão)
  5) Formatação para o HUD (interface)
"""

import math
import random

from src.config import LARGURA, ALTURA


# ===========================================================================
# 1) Pontuação e vida
# ===========================================================================

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual e retorna o novo total."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Retorna True quando o jogador não tem mais vidas (fim de jogo)."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """
    Restringe 'valor' ao intervalo [minimo, maximo].
    Usado para impedir que o jogador saia da área visível da tela.
    """
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


# ===========================================================================
# 2) Colisão
# ===========================================================================

def colidindo(ax, ay, aw, ah, bx, by, bw, bh):
    """
    Verifica se dois retângulos estão sobrepostos (colisão AABB simples).

    Cada objeto é descrito pelo seu CENTRO (x, y) e seu tamanho (w, h).
    A colisão ocorre quando a distância entre os centros, em cada eixo,
    é menor que a soma das metades das larguras/alturas.
    """
    return (abs(ax - bx) < (aw + bw) / 2 and
            abs(ay - by) < (ah + bh) / 2)


# ===========================================================================
# 3) Geração de posições (spawns)
# ===========================================================================

def gerar_x_aleatorio(largura_objeto):
    """
    Sorteia uma posição X dentro dos limites da tela, já considerando a
    largura do objeto para que ele não nasça "cortado" pela borda.
    """
    return random.randint(largura_objeto, LARGURA - largura_objeto)


def tipo_obstaculo_aleatorio():
    """
    Sorteia qual sprite de obstáculo usar (revezamento aleatório entre
    os dois tipos disponíveis: 'obstaculo1' e 'obstaculo2').
    """
    return random.choice(["obstaculo1", "obstaculo2"])


# ===========================================================================
# 4) Partículas (animação de explosão)
# ===========================================================================

def criar_particulas(x, y, cor, quantidade=12):
    """
    Gera uma lista de partículas que se espalham em direções aleatórias
    a partir do ponto (x, y). Usado tanto para pequenas faíscas (ao
    destruir um inimigo/obstáculo) quanto para a explosão grande do
    jogador ao perder a última vida.

    Cada partícula é um dicionário com posição, velocidade (vx, vy),
    tempo de vida (life) e cor.
    """
    particulas = []
    for _ in range(quantidade):
        angulo = random.uniform(0, 2 * math.pi)       # direção aleatória (0 a 360°)
        velocidade = random.uniform(1.5, 5)            # intensidade aleatória
        particulas.append({
            "x": x, "y": y,
            "vx": math.cos(angulo) * velocidade,
            "vy": math.sin(angulo) * velocidade,
            "life": 30, "max_life": 30, "cor": cor
        })
    return particulas


def atualizar_particulas(particulas):
    """
    Avança um frame da simulação de partículas: move cada uma de acordo
    com sua velocidade e reduz seu tempo de vida. Partículas com
    'life' esgotado são removidas da lista (efeito de desaparecer).
    """
    for p in particulas:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
    return [p for p in particulas if p["life"] > 0]


# ===========================================================================
# 5) Formatação para o HUD
# ===========================================================================

def formatar_tempo(frames, fps):
    """
    Converte uma contagem de frames em uma string "MM:SS" para exibir
    o temporizador da partida (ex.: 90 frames a 60 FPS -> "00:01").
    """
    segundos_totais = frames // fps
    minutos = segundos_totais // 60
    segundos = segundos_totais % 60
    return f"{minutos:02d}:{segundos:02d}"
