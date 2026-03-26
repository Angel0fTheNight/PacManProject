import pygame
import random
import json

# --- INICIALIZAÇÃO ---
pygame.init()

# Configurações de Tela
TILE = 40
LINHAS = 10
COLUNAS = 10
LARGURA = COLUNAS * TILE
ALTURA = LINHAS * TILE

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Pac-Man - Edição BFF")

# Fonte para textos
fonte = pygame.font.SysFont("Arial", 30)

# Cores
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)


# --- SISTEMA DE RANKING ---
def salvar_pontuacao(nome, pontos):
    try:
        with open("ranking.json", "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = []

    dados.append({"nome": nome, "pontos": pontos})
    # Mantém apenas os 5 melhores
    dados = sorted(dados, key=lambda x: x["pontos"], reverse=True)[:5]

    with open("ranking.json", "w") as f:
        json.dump(dados, f)


def ler_ranking():
    try:
        with open("ranking.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# --- VARIÁVEIS DE ESTADO E JOGO ---
estado = "menu"
opcoes_menu = ["Jogar", "Ranking", "Sair"]
opcao_selecionada = 0
nome_usuario = ""

mapas = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 1, 2, 2, 2, 2, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 2, 1],
        [1, 2, 2, 1, 2, 2, 2, 1, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 1, 2, 2, 2, 1, 2, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 1],
        [1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 1, 1, 2, 1, 1, 1, 2, 1, 1],
        [1, 2, 2, 2, 2, 2, 1, 2, 2, 1],
        [1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 2, 1, 2, 2, 2, 1, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
]

fase = 0
mapa = [linha[:] for linha in mapas[fase]]
player_x, player_y = 1, 1
ghost_x, ghost_y = 8, 8
score = 0
clock = pygame.time.Clock()


# --- FUNÇÕES DE DESENHO ---
def desenhar_menu():
    tela.fill(PRETO)
    titulo = fonte.render("Mini Pac-Man", True, AMARELO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))
    for i, opcao in enumerate(opcoes_menu):
        cor = AMARELO if i == opcao_selecionada else BRANCO
        texto = fonte.render(opcao, True, cor)
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 150 + i * 50))
    pygame.display.flip()


def desenhar_ranking():
    tela.fill(PRETO)
    titulo = fonte.render("TOP 5 SCORE", True, AMARELO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 30))
    ranking = ler_ranking()
    for i, item in enumerate(ranking):
        texto = fonte.render(f"{i + 1}. {item['nome']} - {item['pontos']}", True, BRANCO)
        tela.blit(texto, (50, 100 + i * 40))
    aviso = fonte.render("ESC para voltar", True, AMARELO)
    tela.blit(aviso, (LARGURA // 2 - aviso.get_width() // 2, ALTURA - 50))
    pygame.display.flip()


def desenhar_input_nome():
    tela.fill(PRETO)
    msg = fonte.render("FIM DE JOGO!", True, VERMELHO)
    tela.blit(msg, (LARGURA // 2 - msg.get_width() // 2, 50))
    pergunta = fonte.render("Teu nome, lenda:", True, BRANCO)
    tela.blit(pergunta, (LARGURA // 2 - pergunta.get_width() // 2, 120))
    caixa_texto = fonte.render(nome_usuario + "|", True, AMARELO)
    tela.blit(caixa_texto, (LARGURA // 2 - caixa_texto.get_width() // 2, 180))
    instrucao = fonte.render("ENTER para salvar", True, BRANCO)
    tela.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, 250))
    pygame.display.flip()


def desenhar_jogo():
    tela.fill(PRETO)
    for y in range(LINHAS):
        for x in range(COLUNAS):
            tile = mapa[y][x]
            if tile == 1:
                pygame.draw.rect(tela, AZUL, (x * TILE, y * TILE, TILE, TILE))
            elif tile == 2:
                pygame.draw.circle(tela, BRANCO, (x * TILE + TILE // 2, y * TILE + TILE // 2), 5)
    pygame.draw.circle(tela, AMARELO, (player_x * TILE + TILE // 2, player_y * TILE + TILE // 2), 15)
    pygame.draw.rect(tela, VERMELHO, (ghost_x * TILE + 5, ghost_y * TILE + 5, TILE - 10, TILE - 10))
    pygame.display.flip()


# --- LÓGICA DE MOVIMENTO ---
def mover_player(dx, dy):
    global player_x, player_y, score
    nx, ny = player_x + dx, player_y + dy
    if mapa[ny][nx] != 1:
        player_x, player_y = nx, ny
        if mapa[ny][nx] == 2:
            mapa[ny][nx] = 0
            score += 10


def mover_fantasma():
    global ghost_x, ghost_y
    direcoes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(direcoes)
    for dx, dy in direcoes:
        nx, ny = ghost_x + dx, ghost_y + dy
        if mapa[ny][nx] != 1:
            ghost_x, ghost_y = nx, ny
            break


# --- LOOP PRINCIPAL ---
rodando = True
while rodando:
    clock.tick(10)  # Velocidade controlada

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado == "menu":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes_menu)
                elif evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes_menu)
                elif evento.key == pygame.K_RETURN:
                    if opcoes_menu[opcao_selecionada] == "Jogar":
                        fase, score = 0, 0
                        mapa = [linha[:] for linha in mapas[fase]]
                        player_x, player_y, ghost_x, ghost_y = 1, 1, 8, 8
                        estado = "jogo"
                    elif opcoes_menu[opcao_selecionada] == "Ranking":
                        estado = "ranking"
                    elif opcoes_menu[opcao_selecionada] == "Sair":
                        rodando = False

        elif estado == "ranking":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado = "menu"

        elif estado == "jogo":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    mover_player(0, -1)
                elif evento.key == pygame.K_DOWN:
                    mover_player(0, 1)
                elif evento.key == pygame.K_LEFT:
                    mover_player(-1, 0)
                elif evento.key == pygame.K_RIGHT:
                    mover_player(1, 0)

        elif estado == "input_nome":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    salvar_pontuacao(nome_usuario if nome_usuario else "Anonimo", score)
                    nome_usuario = ""
                    estado = "menu"
                elif evento.key == pygame.K_BACKSPACE:
                    nome_usuario = nome_usuario[:-1]
                else:
                    if len(nome_usuario) < 10:
                        nome_usuario += evento.unicode

    # ATUALIZAÇÃO E DESENHOS
    if estado == "menu":
        desenhar_menu()
    elif estado == "ranking":
        desenhar_ranking()
    elif estado == "input_nome":
        desenhar_input_nome()
    elif estado == "jogo":
        mover_fantasma()

        # 1. Checar Vitória Primeiro
        vitoria = True
        for linha in mapa:
            if 2 in linha:
                vitoria = False
                break

        if vitoria:
            fase += 1
            if fase >= len(mapas):
                estado = "input_nome"
            else:
                mapa = [linha[:] for linha in mapas[fase]]
                player_x, player_y, ghost_x, ghost_y = 1, 1, 8, 8
                pygame.time.delay(300)

        # 2. Só checa derrota se não venceu a fase
        elif player_x == ghost_x and player_y == ghost_y:
            estado = "input_nome"

        desenhar_jogo()

pygame.quit()