import pygame

import Enemies
import pirate
import Collectables
from ResourceManager import ResourceManager
from settings import *
from Tile import Tile
from World import World
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

# En tu juego principal
resource_manager = ResourceManager()

# Creamos jugador y enemigo
player = pirate.Pirate('pirate', 200, 200, 1, 4, resource_manager)
enemy = Enemies.CucumberEnemy(800, 540, 1, resource_manager)

world = World()

level1 = LevelGenerator.LevelGenerator(r'PruebasYEditor/level1_data.csv')
tiles = level1.load_level()
print(tiles)
# Crear suelo
map = world.process_data(tiles)

font = pygame.font.SysFont('Futura', 30)

# Grupos de Sprites
item_boxes_Group = pygame.sprite.Group()

# Creamos objetos recogibles
item_box = Collectables.Collectables('Health',  100,  550,  1.25, player)
item_boxes_Group.add(item_box)

item_box = Collectables.Collectables('Key',  200,  550,  1.25, player)
item_boxes_Group.add(item_box)

item_box = Collectables.Collectables('Berries',  300,  550,  1.25, player)
item_boxes_Group.add(item_box)



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

screen_scroll = 0
bg_scroll = 0

# Bucle principal del juego
run = True
while run:
    # Establecer la velocidad del juego
    clock.tick(FPS)
    draw_bg()

    # Realiza las animaciones
    player.update(screen_scroll)

    # Dibujar jugador
    player.draw()

    # Muestra enemigo
    enemy.draw(screen)

    # Mover enemigo
    enemy.move()

    # Verificar si el enemigo está atacando al pirata
    #enemy.attack(player)

    # dibujar items y pintarlos
    item_boxes_Group.update(screen_scroll)
    item_boxes_Group.draw(screen)

    screen_scroll = player.move(move_left, move_right, world, bg_scroll)
    bg_scroll -= screen_scroll

    world.draw(screen, screen_scroll)

    # Actualiza la accion del jugador
    if player.attack:
        player.update_action(3)  # 3 -> animacion ataque
        # Realizar ataque si el jugador está sobre el enemigo y presiona la tecla de espacio
        if player.collision_rect.colliderect(enemy.collision_rect):
            enemy.get_Hit(35)  # Reducir la salud del enemigo en 35
    elif player.in_air:
        player.update_action(2)  # 2 -> animacion jump
    elif move_left or move_right:
        player.update_action(1)  # 1 -> animacion run
    else:
        player.update_action(0)  # 0 -> animacion idle

    # haz que el enemigo se mueva mas rapido que el jugador
    enemy.move()
    enemy.update(screen_scroll)

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
