"""
jogo.py
-------
Coração do jogo: contém o estado da partida, a lógica de atualização
(física simples, spawns, colisões), o desenho de tudo na tela e o
loop principal que mantém o jogo rodando.

Organização do arquivo (nessa ordem):
  1) Estado do jogo       -> novo_jogo()
  2) Spawns                -> cria inimigos e obstáculos
  3) Atualização (lógica)  -> move objetos, trata colisões, avança onda
  4) Desenho               -> renderiza tudo na tela (HUD, telas de menu/fim)
  5) Loop principal        -> executar_jogo(), ponto de entrada do jogo
"""

import sys
import random

import pygame

from src.config import (
    LARGURA, ALTURA, FPS, TITULO_JOGO,
    FUNDO, VERDE, VERMELHO, AMARELO, BRANCO, CINZA, LARANJA,
    CAMINHO_RECORDE,
    TAMANHO_INIMIGO, TAMANHO_OBSTACULO,
    TAMANHO_JOGADOR_W, TAMANHO_JOGADOR_H,
    VIDAS_INICIAIS, PONTOS_POR_INIMIGO,
    SPAWN_INTERVAL_INICIAL, SPAWN_INTERVAL_MINIMO,
    DESTRUIDOS_POR_ONDA,
)
from src.funcoes import (
    calcular_pontos, tomar_dano, jogador_perdeu, limitar_valor,
    colidindo, gerar_x_aleatorio, tipo_obstaculo_aleatorio,
    criar_particulas, atualizar_particulas, formatar_tempo,
)
from src.sprites import carregar_sprites_do_jogo
from src.dados import salvar_recorde, carregar_recorde


# ===========================================================================
# 1) ESTADO DO JOGO
# ===========================================================================
# O estado inteiro da partida é guardado em um único dicionário ("g", de
# "game"), o que facilita passar tudo para as funções de atualização e
# desenho sem precisar de variáveis globais.

def novo_jogo():
    """
    Cria e retorna o dicionário com todo o estado inicial de uma nova
    partida: posição do jogador, vidas, pontuação, listas de balas,
    inimigos, obstáculos e partículas, todas vazias no começo.
    """
    jogador = {
        "x": LARGURA // 2, "y": ALTURA - 60,        # nasce centralizado, perto da base
        "w": TAMANHO_JOGADOR_W, "h": TAMANHO_JOGADOR_H,
        "speed": 4,           # velocidade de movimento (pixels por frame)
        "shoot_cd": 0,        # cooldown (contagem regressiva) até poder atirar de novo
    }
    return dict(
        jogador=jogador,
        vidas=VIDAS_INICIAIS,
        pontos=0,
        onda=1,                         # dificuldade atual (sobe com o tempo/abates)
        tempo=0,                        # contador de frames, usado no temporizador (HUD)
        spawn_timer=0,                  # contagem de frames até o próximo spawn
        spawn_interval=SPAWN_INTERVAL_INICIAL,
        destruidos=0,                   # total de inimigos/obstáculos destruídos
        destruidos_por_onda=DESTRUIDOS_POR_ONDA,
        balas=[],                       # projéteis disparados pelo jogador
        balas_inimigo=[],               # projéteis disparados pelas naves inimigas
        inimigos=[],                    # naves inimigas em cena
        obstaculos=[],                  # obstáculos (não atiram) em cena
        particulas=[],                  # partículas de efeito visual (explosões/faíscas)
        explodindo=False,               # True durante a animação de morte do jogador
        explosao_timer=0,               # frames restantes da animação de explosão
    )


# ===========================================================================
# 2) SPAWNS
# ===========================================================================
# Funções responsáveis por criar novos elementos no topo da tela, que
# depois descem em direção ao jogador.

def spawnar_inimigo(g):
    """
    Cria uma nova nave inimiga no topo da tela, em uma posição X
    aleatória. A velocidade de descida e o cooldown de tiro aumentam
    com a onda atual, deixando o jogo progressivamente mais difícil.
    """
    x = gerar_x_aleatorio(TAMANHO_INIMIGO)
    speed = 1 + g["onda"] * 0.3
    shoot_cd = random.randint(60, 120)   # tempo (em frames) até o primeiro tiro
    g["inimigos"].append({
        "x": x, "y": -TAMANHO_INIMIGO,
        "w": TAMANHO_INIMIGO, "h": TAMANHO_INIMIGO,
        "speed": speed, "shoot_cd": shoot_cd,
    })


def spawnar_obstaculo(g):
    """
    Cria um novo obstáculo no topo da tela (não atira, só colide).
    O tipo de sprite (obstaculo1 ou obstaculo2) é sorteado, fazendo
    com que os dois revezem aleatoriamente durante a partida.
    """
    x = gerar_x_aleatorio(TAMANHO_OBSTACULO)
    speed = 2 + g["onda"] * 0.25
    g["obstaculos"].append({
        "x": x, "y": -TAMANHO_OBSTACULO,
        "w": TAMANHO_OBSTACULO, "h": TAMANHO_OBSTACULO,
        "speed": speed, "tipo": tipo_obstaculo_aleatorio(),
    })


# ===========================================================================
# 3) ATUALIZAÇÃO (LÓGICA DO JOGO)
# ===========================================================================
# Todas as funções abaixo recebem o estado "g" e o modificam diretamente
# (não retornam um novo estado). São chamadas, em ordem, pela função
# update(), uma vez por frame.

def mover_jogador(g, teclas):
    """
    Move o jogador conforme as teclas pressionadas (WASD ou setas),
    mantendo a nave sempre dentro dos limites da tela.
    """
    j = g["jogador"]
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        j["x"] = limitar_valor(j["x"] - j["speed"], j["w"] // 2, LARGURA - j["w"] // 2)
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        j["x"] = limitar_valor(j["x"] + j["speed"], j["w"] // 2, LARGURA - j["w"] // 2)
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        j["y"] = limitar_valor(j["y"] - j["speed"], j["h"] // 2, ALTURA - j["h"] // 2)
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        j["y"] = limitar_valor(j["y"] + j["speed"], j["h"] // 2, ALTURA - j["h"] // 2)


def atualizar_tiro_jogador(g, teclas):
    """
    Controla o disparo do jogador: enquanto o cooldown ("shoot_cd") não
    chegar a zero, novos tiros não são permitidos. Isso evita disparos
    infinitamente rápidos ao segurar a tecla de espaço.
    """
    j = g["jogador"]
    if j["shoot_cd"] > 0:
        j["shoot_cd"] -= 1
    if teclas[pygame.K_SPACE] and j["shoot_cd"] == 0:
        g["balas"].append({"x": j["x"], "y": j["y"] - j["h"] // 2, "w": 4, "h": 12, "speed": 9})
        j["shoot_cd"] = 14   # frames até o próximo tiro ser permitido


def atualizar_balas(g):
    """
    Move todas as balas (do jogador, para cima; dos inimigos, para
    baixo) e remove as que já saíram da área visível da tela.
    """
    g["balas"] = [b for b in g["balas"] if b["y"] > -20]
    for b in g["balas"]:
        b["y"] -= b["speed"]

    g["balas_inimigo"] = [b for b in g["balas_inimigo"] if b["y"] < ALTURA + 20]
    for b in g["balas_inimigo"]:
        b["y"] += b["speed"]


def atualizar_spawns(g):
    """
    Controla o cronômetro de spawn: a cada "spawn_interval" frames,
    cria um novo elemento, alternando aleatoriamente entre nave
    inimiga (50% de chance) e obstáculo (50% de chance).
    """
    g["spawn_timer"] += 1
    if g["spawn_timer"] >= g["spawn_interval"]:
        g["spawn_timer"] = 0

        if random.random() < 0.5:
            spawnar_inimigo(g)
        else:
            spawnar_obstaculo(g)


def atualizar_inimigos(g):
    """
    Move as naves inimigas para baixo e faz com que disparem
    periodicamente contra o jogador (cooldown próprio de cada nave).
    Remove as naves que já passaram do fim da tela sem serem atingidas.
    """
    velocidade_tiro = 3 + g["onda"] * 0.2   # tiros ficam mais rápidos em ondas avançadas
    for e in g["inimigos"]:
        e["y"] += e["speed"]
        e["shoot_cd"] -= 1
        if e["shoot_cd"] <= 0:
            g["balas_inimigo"].append({
                "x": e["x"], "y": e["y"] + e["h"] // 2, "w": 4, "h": 10,
                "speed": velocidade_tiro,
            })
            e["shoot_cd"] = random.randint(60, 120)
    g["inimigos"] = [e for e in g["inimigos"] if e["y"] < ALTURA + 30]


def atualizar_obstaculos(g):
    """
    Move os obstáculos para baixo. Diferente das naves inimigas, eles
    nunca atiram — representam apenas perigo de colisão direta.
    """
    for o in g["obstaculos"]:
        o["y"] += o["speed"]
    g["obstaculos"] = [o for o in g["obstaculos"] if o["y"] < ALTURA + 30]


def verificar_colisao_balas_jogador(g):
    """
    Verifica se alguma bala do jogador acertou uma nave inimiga ou um
    obstáculo. Em caso de acerto: gera partículas de impacto, remove o
    alvo, soma pontos e marca a bala como "usada" (ela some também).

    Naves inimigas valem PONTOS_POR_INIMIGO; obstáculos valem metade
    disso, já que são mais fáceis de evitar (não atiram de volta).
    """
    balas_vivas = []
    for b in g["balas"]:
        acertou = False

        # Primeiro tenta acertar uma nave inimiga
        for i in range(len(g["inimigos"]) - 1, -1, -1):
            e = g["inimigos"][i]
            if colidindo(b["x"], b["y"], b["w"], b["h"], e["x"], e["y"], e["w"], e["h"]):
                g["particulas"] += criar_particulas(e["x"], e["y"], LARANJA)
                g["inimigos"].pop(i)
                g["pontos"] = calcular_pontos(g["pontos"], PONTOS_POR_INIMIGO)
                g["destruidos"] += 1
                acertou = True
                break

        # Se não acertou nenhuma nave, tenta acertar um obstáculo
        if not acertou:
            for i in range(len(g["obstaculos"]) - 1, -1, -1):
                o = g["obstaculos"][i]
                if colidindo(b["x"], b["y"], b["w"], b["h"], o["x"], o["y"], o["w"], o["h"]):
                    g["particulas"] += criar_particulas(o["x"], o["y"], CINZA)
                    g["obstaculos"].pop(i)
                    g["pontos"] = calcular_pontos(g["pontos"], PONTOS_POR_INIMIGO // 2)
                    g["destruidos"] += 1
                    acertou = True
                    break

        # Balas que não acertaram nada continuam existindo no próximo frame
        if not acertou:
            balas_vivas.append(b)

    g["balas"] = balas_vivas


def verificar_colisao_jogador(g):
    """
    Verifica se o jogador foi atingido por balas inimigas ou colidiu
    diretamente com uma nave/obstáculo. Cada acerto custa 1 vida. Se
    as vidas chegarem a zero, inicia a animação de explosão do jogador.

    Não faz nada se o jogador já estiver explodindo (evita perder
    "vidas negativas" durante a animação de morte).
    """
    if g["explodindo"]:
        return

    j = g["jogador"]
    atingido = False

    # Colisão com balas inimigas (a bala desaparece ao acertar)
    balas_ini_vivas = []
    for b in g["balas_inimigo"]:
        if colidindo(b["x"], b["y"], b["w"], b["h"], j["x"], j["y"], j["w"], j["h"]):
            atingido = True
        else:
            balas_ini_vivas.append(b)
    g["balas_inimigo"] = balas_ini_vivas

    # Colisão direta (choque) com naves inimigas
    for i in range(len(g["inimigos"]) - 1, -1, -1):
        e = g["inimigos"][i]
        if colidindo(j["x"], j["y"], j["w"], j["h"], e["x"], e["y"], e["w"], e["h"]):
            g["inimigos"].pop(i)
            atingido = True

    # Colisão direta (choque) com obstáculos
    for i in range(len(g["obstaculos"]) - 1, -1, -1):
        o = g["obstaculos"][i]
        if colidindo(j["x"], j["y"], j["w"], j["h"], o["x"], o["y"], o["w"], o["h"]):
            g["obstaculos"].pop(i)
            atingido = True

    if atingido:
        g["vidas"] = tomar_dano(g["vidas"], 1)
        g["particulas"] += criar_particulas(j["x"], j["y"], VERMELHO, quantidade=18)

        if jogador_perdeu(g["vidas"]):
            # Última vida perdida: inicia a sequência de explosão do jogador.
            # O jogo só vai para a tela de "game over" depois que o
            # temporizador da explosão (explosao_timer) chegar a zero.
            g["explodindo"] = True
            g["explosao_timer"] = 40


def atualizar_explosao(g):
    """
    Atualiza a animação de morte do jogador: a cada 6 frames, gera uma
    nova leva de partículas alaranjadas na posição onde a nave estava,
    simulando uma explosão contínua até o temporizador acabar.
    """
    if g["explodindo"]:
        g["explosao_timer"] -= 1
        if g["explosao_timer"] % 6 == 0:
            j = g["jogador"]
            g["particulas"] += criar_particulas(j["x"], j["y"], LARANJA, quantidade=6)


def update(g, teclas):
    """
    Atualiza um frame completo da partida, chamando, em ordem, cada uma
    das funções de lógica acima. É o "maestro" da simulação: decide o
    que acontece a cada tick do jogo.
    """
    g["tempo"] += 1   # temporizador da partida (independe do estado de explosão)

    if not g["explodindo"]:
        # Enquanto o jogador estiver "vivo", ele pode se mover e atirar.
        mover_jogador(g, teclas)
        atualizar_tiro_jogador(g, teclas)

    # Balas, inimigos e obstáculos continuam se movendo mesmo durante a
    # explosão, para a cena não "congelar" de repente.
    atualizar_balas(g)
    atualizar_spawns(g)
    atualizar_inimigos(g)
    atualizar_obstaculos(g)

    if not g["explodindo"]:
        verificar_colisao_balas_jogador(g)
        verificar_colisao_jogador(g)
    else:
        atualizar_explosao(g)

    g["particulas"] = atualizar_particulas(g["particulas"])

    # Avança de onda quando o jogador destrói alvos suficientes.
    # A exigência cresce a cada onda (onda 2 pede o dobro da onda 1, etc.),
    # e o intervalo de spawn diminui até o piso definido em config.py.
    if g["destruidos"] >= g["onda"] * g["destruidos_por_onda"]:
        g["onda"] += 1
        g["spawn_interval"] = max(SPAWN_INTERVAL_MINIMO, g["spawn_interval"] - 8)


# ===========================================================================
# 4) DESENHO
# ===========================================================================
# Funções responsáveis por desenhar o estado atual do jogo na tela.
# Nenhuma delas modifica o estado "g"; elas apenas o "leem" para saber
# o que desenhar.

def desenhar_jogo(tela, fonte, sprites, recorde, g):
    """
    Desenha um frame completo da partida: fundo, balas, obstáculos,
    inimigos, o jogador (se não estiver explodindo), partículas e o
    HUD (vidas, pontos, onda, recorde, tempo).
    """
    tela.fill(FUNDO)
    j = g["jogador"]

    # Balas do jogador (retângulos amarelos subindo)
    for b in g["balas"]:
        pygame.draw.rect(tela, AMARELO, (b["x"] - b["w"] // 2, b["y"] - b["h"] // 2, b["w"], b["h"]))

    # Balas inimigas (retângulos vermelhos descendo)
    for b in g["balas_inimigo"]:
        pygame.draw.rect(tela, VERMELHO, (b["x"] - b["w"] // 2, b["y"] - b["h"] // 2, b["w"], b["h"]))

    # Obstáculos (não atiram, só descem)
    for o in g["obstaculos"]:
        img = sprites[o["tipo"]]
        tela.blit(img, (o["x"] - o["w"] // 2, o["y"] - o["h"] // 2))

    # Naves inimigas
    for e in g["inimigos"]:
        img = sprites["inimigo"]
        tela.blit(img, (e["x"] - e["w"] // 2, e["y"] - e["h"] // 2))

    # Jogador: some da tela durante a animação de explosão
    if not g["explodindo"]:
        img = sprites["jogador"]
        tela.blit(img, (j["x"] - j["w"] // 2, j["y"] - j["h"] // 2))

    # Partículas (faíscas de impacto e explosão do jogador).
    # O "alpha" (transparência) diminui conforme a partícula envelhece,
    # criando um efeito de desvanecimento suave.
    for p in g["particulas"]:
        alpha = int(255 * p["life"] / p["max_life"])
        cor = tuple(min(255, max(0, c)) for c in p["cor"])
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        s.fill((*cor, alpha))
        tela.blit(s, (int(p["x"]) - 2, int(p["y"]) - 2))

    desenhar_hud(tela, fonte, recorde, g)


def desenhar_hud(tela, fonte, recorde, g):
    """
    Desenha a interface (HUD) no topo da tela: vidas restantes,
    pontuação atual, onda (dificuldade), recorde salvo e o
    temporizador da partida em formato MM:SS.
    """
    txt_vidas   = fonte.render(f"VIDAS: {max(g['vidas'], 0)}", True, BRANCO)
    txt_pontos  = fonte.render(f"PONTOS: {g['pontos']}", True, BRANCO)
    txt_onda    = fonte.render(f"ONDA: {g['onda']}", True, CINZA)
    txt_recorde = fonte.render(f"RECORDE: {recorde}", True, AMARELO)
    txt_tempo   = fonte.render(formatar_tempo(g["tempo"], FPS), True, VERDE)

    tela.blit(txt_vidas, (8, 8))
    tela.blit(txt_pontos, (LARGURA // 2 - txt_pontos.get_width() // 2, 8))
    tela.blit(txt_onda, (LARGURA - txt_onda.get_width() - 8, 8))
    tela.blit(txt_recorde, (8, 28))
    tela.blit(txt_tempo, (LARGURA - txt_tempo.get_width() - 8, 28))


def tela_menu(tela, fonte, fonte_grande, recorde):
    """Desenha a tela inicial (menu), exibida antes de a partida começar."""
    tela.fill(FUNDO)
    t1 = fonte_grande.render("NAVE INFINITA", True, VERDE)
    t2 = fonte.render("Pressione ENTER para jogar", True, BRANCO)
    t3 = fonte.render("WASD / Setas: mover   Espaco: atirar", True, CINZA)
    t4 = fonte.render(f"Recorde atual: {recorde}", True, AMARELO)

    tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, ALTURA // 3))
    tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, ALTURA // 2))
    tela.blit(t3, (LARGURA // 2 - t3.get_width() // 2, ALTURA // 2 + 30))
    tela.blit(t4, (LARGURA // 2 - t4.get_width() // 2, ALTURA // 2 + 60))


def tela_game_over(tela, fonte, fonte_grande, g, recorde, recorde_novo):
    """
    Desenha a tela de fim de jogo, mostrando a pontuação final, o
    tempo de sobrevivência e o recorde (com destaque se foi superado
    nesta partida).
    """
    tela.fill(FUNDO)
    t1 = fonte_grande.render("GAME OVER", True, VERMELHO)
    t2 = fonte.render(f"Pontos: {g['pontos']}", True, BRANCO)
    t3 = fonte.render(f"Tempo: {formatar_tempo(g['tempo'], FPS)}", True, BRANCO)
    t4 = fonte.render(f"Recorde: {recorde}", True, AMARELO)
    t5 = fonte.render("Pressione ENTER para reiniciar", True, CINZA)

    tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, ALTURA // 3))
    tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, ALTURA // 2))
    tela.blit(t3, (LARGURA // 2 - t3.get_width() // 2, ALTURA // 2 + 25))
    tela.blit(t4, (LARGURA // 2 - t4.get_width() // 2, ALTURA // 2 + 50))
    tela.blit(t5, (LARGURA // 2 - t5.get_width() // 2, ALTURA // 2 + 80))

    if recorde_novo:
        t6 = fonte.render("NOVO RECORDE!", True, VERDE)
        tela.blit(t6, (LARGURA // 2 - t6.get_width() // 2, ALTURA // 2 - 25))


# ===========================================================================
# 5) LOOP PRINCIPAL
# ===========================================================================

def executar_jogo():
    """
    Ponto de entrada do jogo (chamado pelo main.py).

    Inicializa o pygame e a janela, carrega sprites e recorde, e então
    entra no loop principal, que roda continuamente até o jogador
    fechar a janela. O loop controla três estados de tela:

      - "menu":     tela inicial, aguardando ENTER para começar
      - "jogando":  partida em andamento (lógica + desenho a cada frame)
      - "gameover": tela final, aguardando ENTER para reiniciar
    """
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    fonte = pygame.font.SysFont("monospace", 14)
    fonte_grande = pygame.font.SysFont("monospace", 28, bold=True)

    sprites = carregar_sprites_do_jogo()
    recorde = carregar_recorde(CAMINHO_RECORDE)
    recorde_novo = False   # usado para exibir "NOVO RECORDE!" na tela de game over

    estado = "menu"
    g = novo_jogo()

    while True:
        relogio.tick(FPS)   # limita o jogo a FPS quadros por segundo

        # --- Tratamento de eventos (fechar janela, apertar ENTER) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                if estado in ("menu", "gameover"):
                    g = novo_jogo()
                    recorde_novo = False
                    estado = "jogando"

        # --- Atualização e desenho conforme o estado atual ---
        if estado == "menu":
            tela_menu(tela, fonte, fonte_grande, recorde)

        elif estado == "jogando":
            teclas = pygame.key.get_pressed()
            update(g, teclas)
            desenhar_jogo(tela, fonte, sprites, recorde, g)

            # Atualiza e salva o recorde em tempo real, assim que for superado
            if g["pontos"] > recorde:
                recorde = g["pontos"]
                recorde_novo = True
                salvar_recorde(CAMINHO_RECORDE, recorde)

            # Só vai para a tela de game over depois que a animação de
            # explosão terminar (explosao_timer chega a zero)
            if g["explodindo"] and g["explosao_timer"] <= 0:
                estado = "gameover"

        elif estado == "gameover":
            tela_game_over(tela, fonte, fonte_grande, g, recorde, recorde_novo)

        pygame.display.flip()   # mostra o frame desenhado na janela
