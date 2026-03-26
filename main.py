import pygame
import random

# Inicialização
pygame.init()

# Configurações
TILE = 40
LINHAS = 10
COLUNAS = 10

LARGURA = COLUNAS * TILE
ALTURA = LINHAS * TILE

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Pac-Man")

# Cores
PRETO = (0,0,0)
AZUL = (0,0,255)
AMARELO = (255,255,0)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)

# Mapa (1=parede, 0=caminho, 2=comida)
mapa = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,1,2,2,2,2,1],
    [1,2,1,2,1,2,1,1,2,1],
    [1,2,1,2,2,2,2,1,2,1],
    [1,2,1,1,1,1,2,1,2,1],
    [1,2,2,2,2,1,2,2,2,1],
    [1,1,1,1,2,1,1,1,2,1],
    [1,2,2,1,2,2,2,1,2,1],
    [1,2,2,2,2,1,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1],
]

# Jogador
player_x = 1
player_y = 1

# Fantasma
ghost_x = 8
ghost_y = 8

score = 0

clock = pygame.time.Clock()

def desenhar():
    tela.fill(PRETO)

    for y in range(LINHAS):
        for x in range(COLUNAS):
            tile = mapa[y][x]

            if tile == 1:
                pygame.draw.rect(tela, AZUL, (x*TILE, y*TILE, TILE, TILE))

            elif tile == 2:
                pygame.draw.circle(tela, BRANCO,
                    (x*TILE + TILE//2, y*TILE + TILE//2), 5)

    # Jogador
    pygame.draw.circle(tela, AMARELO,
        (player_x*TILE + TILE//2, player_y*TILE + TILE//2), 15)

    # Fantasma
    pygame.draw.rect(tela, VERMELHO,
        (ghost_x*TILE+5, ghost_y*TILE+5, TILE-10, TILE-10))

    pygame.display.flip()

def mover_player(dx, dy):
    global player_x, player_y, score

    nx = player_x + dx
    ny = player_y + dy

    if mapa[ny][nx] != 1:
        player_x = nx
        player_y = ny

        if mapa[ny][nx] == 2:
            mapa[ny][nx] = 0
            score += 10

def mover_fantasma():
    global ghost_x, ghost_y

    direcoes = [(1,0),(-1,0),(0,1),(0,-1)]
    random.shuffle(direcoes)

    for dx, dy in direcoes:
        nx = ghost_x + dx
        ny = ghost_y + dy

        if mapa[ny][nx] != 1:
            ghost_x = nx
            ghost_y = ny
            break

def checar_colisao():
    if player_x == ghost_x and player_y == ghost_y:
        print("Game Over! Pontuação:", score)
        pygame.quit()
        exit()

# Loop principal
rodando = True

while rodando:
    clock.tick(8)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                mover_player(0, -1)
            elif evento.key == pygame.K_DOWN:
                mover_player(0, 1)
            elif evento.key == pygame.K_LEFT:
                mover_player(-1, 0)
            elif evento.key == pygame.K_RIGHT:
                mover_player(1, 0)

    mover_fantasma()
    checar_colisao()
    desenhar()

pygame.quit()