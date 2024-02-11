import pygame
import pirate

pygame.init()

# Establecer el reloj del juego y FPS
clock = pygame.time.Clock()
FPS = 60

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Impel Down - Luffy's Adventure")

# Cargar el fondo
background = pygame.image.load('Imagenes/Background/dungeon3.png').convert_alpha()

# Crear un jugador
player = pirate.Pirate(50, 500, 1)


# Bucle principal del juego
run = True
while run:

    # Dibujar jugador
    player.draw()

    # Actualizar la pantalla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Salir del juego
pygame.quit()
