import pygame
import pirate
import settings

pygame.init()

# Establecer el reloj del juego y FPS
clock = pygame.time.Clock()
FPS = 60

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Impel Down - Ivankov Adventure")

# Crear un jugador
player = pirate.Pirate('pirate', 200, 200, 1, 4)
enemy = pirate.Pirate('enemy', 400, 200, 1, 4)

# define colours
BG = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
GREEN = (144, 201, 120)
LINE = (255,0,0)


# dibujar en segundo plano
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, LINE, (0, 400), (SCREEN_WIDTH,400)) #linea rojo -> simula suelo


# Variables de movimiento
move_left = False
move_right = False
attack = False

# Bucle principal del juego
run = True
while run:

    # Establecer la velocidad del juego
    clock.tick(FPS)
    draw_bg()

    # Realiza las animaciones
    player.update_animation()

    # Dibujar jugador
    player.draw()
    enemy.draw()

    # Actualiza la accion del jugador
    if player.attack:
        player.update_action(3) #3 -> animacion ataque
    elif player.in_air:
        player.update_action(2) #2 -> animacion jump
    elif move_left or move_right:
        player.update_action(1) #1 -> animacion run
    else:
        player.update_action(0) #0 -> animacion idle

    player.move(move_left, move_right)


    # Actualizar la pantalla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Presionar teclas para mover al jugador

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_SPACE:
                player.jump = True
            if event.key == pygame.K_f:
                player.attack = True
            if event.type == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_f:
                player.attack = False

    pygame.display.update()

# Salir del juego
pygame.quit()
