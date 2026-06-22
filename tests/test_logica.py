"""Testes unitários para as funções de lógica do jogo."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.funcoes import (
    calcular_pontos,
    tomar_dano,
    jogador_perdeu,
    limitar_valor,
    colidindo,
    criar_particulas,
    atualizar_particulas,
    formatar_tempo,
)


def test_calcular_pontos_soma_corretamente():
    assert calcular_pontos(0, 10) == 10
    assert calcular_pontos(50, 10) == 60


def test_tomar_dano_reduz_vida():
    assert tomar_dano(3, 1) == 2
    assert tomar_dano(1, 1) == 0


def test_jogador_perdeu_com_zero_vidas():
    assert jogador_perdeu(0) is True
    assert jogador_perdeu(1) is False


def test_limitar_valor_dentro_do_intervalo():
    assert limitar_valor(5, 0, 10) == 5
    assert limitar_valor(-1, 0, 10) == 0
    assert limitar_valor(11, 0, 10) == 10


def test_colidindo_detecta_sobreposicao():
    assert colidindo(0, 0, 10, 10, 5, 5, 10, 10) is True
    assert colidindo(0, 0, 10, 10, 100, 100, 10, 10) is False


def test_particulas_sao_criadas_e_atualizadas():
    particulas = criar_particulas(0, 0, (255, 0, 0), quantidade=5)
    assert len(particulas) == 5
    particulas = atualizar_particulas(particulas)
    assert all(p["life"] == 29 for p in particulas)


def test_formatar_tempo():
    assert formatar_tempo(0, 60) == "00:00"
    assert formatar_tempo(60, 60) == "00:01"
    assert formatar_tempo(3600, 60) == "01:00"
