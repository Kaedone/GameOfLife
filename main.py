
import pygame
from itertools import product, chain

pygame.init()
screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
board = {(0,0),(1,0),(1,1),(0,1),(2,3),(2,2),(3,3),(3,2)}
pygame.time.set_timer(pygame.USEREVENT, 1500)

CELLSIZE = 32
H_CELLSIZE = CELLSIZE / 2

def neighbors(point):
    x,y = point
    for dx, dy in product((-1,0,1), repeat=2):
        if dx != 0 or dy != 0:
            if x + dx >= 0 and y + dy >= 0:
                yield x + dx, y + dy

def step(board):
    new_board = set()
    with_neighbors = board | set(chain(*map(neighbors, board)))
    for point in with_neighbors:
        count = sum((neigh in board) for neigh in neighbors(point))
        if count == 3 or (count == 2 and point in board):
            new_board.add(point)
    return new_board

def scr_to_board(pos):
    x, y = pos
    return (x / CELLSIZE , y / CELLSIZE)

def board_to_scr(pos):
    x, y = pos
    return (x * CELLSIZE + H_CELLSIZE, y * CELLSIZE + H_CELLSIZE)

while True:
    if pygame.event.get(pygame.QUIT): 
        break

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            board ^= {scr_to_board(pygame.mouse.get_pos())}
        if e.type == pygame.USEREVENT:
            board = step(board)

    screen.fill(pygame.color.Color('white'))
    for cell in board:
        pygame.draw.circle(screen, pygame.color.Color('black'), board_to_scr(cell), H_CELLSIZE, 0)

    pygame.display.flip()
    clock.tick(60)
