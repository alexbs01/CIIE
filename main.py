import pygame

import Enemies
import pirate
from settings import *
from Tile import Tile
import LevelGenerator
from Ui import Ui

pygame.init()
pygame.font.init()

# Establecer el reloj del juego y FPS
clock = pygame.time.Clock()
FPS = 60

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Impel Down - Ivankov Adventure")

# Crear un jugador
player = pirate.Pirate('pirate', 200, 200, 1, 4)
enemy = Enemies.CucumberEnemy('enemy', 400, 370, 1, 4)

level1 = LevelGenerator.LevelGenerator(r'PruebasYEditor/level1_data.csv')
print(level1.load_level())
level1.load_level()
# Crear suelo
tiles = level1.create_level()
print(tiles)

font = pygame.font.SysFont('Futura', 30)

# dibujar en segundo plano
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, LINE, (0, 400), (SCREEN_WIDTH,400)) #linea rojo -> simula suelo
    
    # Muestra barra de salud
    health_observer.update_health(player.health)
    ui.draw_text('Vida',font,WHITE,30,25)

# Creamos instancia Ui para guardar la pantalla 
ui = Ui()

# Creamos observador de salud
health_observer = Ui.HealthObserver(30,45, ui.display_surface, player.health, player.health)
player.register(health_observer) 

# Variables de movimiento
move_left = False
move_right = False

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

    # Muestra enemigo
    enemy.draw()

    for tile in tiles:
        tile.update()
    # Actualiza la accion del jugador
    if player.attack:
        player.update_action(3, tiles) #3 -> animacion ataque
    elif player.in_air:
        player.update_action(2, tiles) #2 -> animacion jump
    elif move_left or move_right:
        player.update_action(1, tiles) #1 -> animacion run
    else:
        player.update_action(0, tiles) #0 -> animacion idle

    player.move(move_left, move_right, tiles)

    # haz que el enemigo se mueva mas rapido que el jugador
    enemy.move(move_left, move_right)
    enemy.update_animation()


    # Actualizar la pantalla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Presionar teclas para mover al jugador

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                player.jump = True
            if event.key == pygame.K_SPACE:
                player.attack = True
            if event.type == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_h:
                print(player.health)
                # Actualizara la barra de salud mediante el patron observador
                player.get_Hit(10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                player.attack = False

    pygame.display.update()

# Salir del juego
pygame.quit()