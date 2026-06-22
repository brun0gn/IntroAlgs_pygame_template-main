"""
dados.py
--------
Funções de persistência de dados em arquivo: leitura e gravação do
recorde de pontuação. Mantém a partida "lembrando" da melhor pontuação
mesmo depois de fechar o jogo.
"""


def salvar_recorde(caminho_arquivo, pontuacao):
    """
    Grava a pontuação informada em um arquivo de texto simples,
    sobrescrevendo o conteúdo anterior.
    """
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """
    Lê o recorde salvo em arquivo e retorna como número inteiro.
    Se o arquivo não existir ou estiver vazio/corrompido, retorna 0
    (comportamento seguro para a primeira execução do jogo).
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if conteudo == "":
                return 0
            return int(conteudo)
    except FileNotFoundError:
        return 0
