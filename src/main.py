import pygame
import sys
import csv

import menu
from menu import main_menu  # Importa la función main_menu desde el archivo menu.py
from asyncio import sleep

from entities import Enemies
from entities import pirate
from items import Collectables as Collectables
from world_generation.ResourceManager import ResourceManager
from settings import *
from world_generation.World import World
from world_generation.LevelGenerator import LevelGenerator
from entities.Ui import Ui
from items import Interactives as Interactives

pygame.init()
pygame.font.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Impel Down - Ivankov Adventure")
# load images
#dungeon_img = pygame.image.load('./assets/Background/dungeon3.png').convert_alpha()

# Establecer el reloj del juego y FPS
clock = pygame.time.Clock()

# Cargar el sonido de fondo
musica = pygame.mixer.Sound("./assets/Music/pirates.mp3")
musica.set_volume(BACKGROUND_MUSIC_VOLUME)

# Cargar el sonido de la espada
espada = pygame.mixer.Sound("./assets/Music/Espada.ogg")

# Variable global que usaremos para manipular los niveles del juego
global level_num
level_num = 0

def main(level_num):
    # Reproducir el sonido de fondo en un bucle continuo
    musica.play(-1)  # El argumento -1 indica que el sonido se reproduce en un bucle infinito

    # En tu juego principal
    resource_manager = ResourceManager()

    # Guarda la posición inicial del pirata
    initial_player_x = 200
    initial_player_y = 600

    # Implementacion para que el jugador reviva en el nivel que muere
    if level_num == 0:
        level_num = INITIAL_LEVEL

    # Creamos jugador y enemigo
    player = pirate.Pirate('pirate', initial_player_x, initial_player_y, 1, 6, resource_manager)
    #spikes = Enemies.Enemy.Spike(640, 545, resource_manager)
    world = World(resource_manager, player)

    level = LevelGenerator(level_num)
    tiles = level.load_level()

    # Dibuja el mapa
    world.process_data(tiles)
    
    last_move_left = False
    last_move_right = False

    def paused_game():
        global last_move_left, last_move_right
        paused = True
        pygame.mixer.pause()  # Pausar la música al pausar el juego
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    if event.key == pygame.K_a:
                        last_move_left = True
                    if event.key == pygame.K_d:
                        last_move_right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        last_move_left = False
                    if event.key == pygame.K_d:
                        last_move_right = False
            SCREEN.fill(BLACK)
            title_font = pygame.font.Font("assets/inmortal.ttf", 100)
            ui.draw_text('Pausa', title_font, WHITE, (SCREEN_WIDTH // 2) - 150, (SCREEN_HEIGHT // 2) - 100)
            pygame.display.update()
            clock.tick(15)
        pygame.mixer.unpause()  # Reanudar la música al reanudar el juego


    # dibujar en segundo plano
    def draw_bg():
        SCREEN.fill(BG2)

        # ELEGIR UNA IMAGEN DE FONDO ADECUADA
        if level_num == 1:
            # Mostrar imagen dungeon
            dungeon_img = pygame.image.load(PATH_ASSET_BACKGROUND)
            #scaled_image = pygame.transform.scale(dungeon_img, (COLS * TILE_WIDTH, ROWS * TILE_HEIGHT))
            #width = scaled_image.get_width()
            #for x in range(4):
                #SCREEN.blit(scaled_image, ((x * width) - bg_scroll, 0))

        # Controla el scroll de los tiles
        world.draw(SCREEN, screen_scroll)

        # Muestra barra de salud por encima de los tiles
        health_observer.update_health(player.health)
        title_font = pygame.font.Font("assets/inmortal.ttf", 25)

        ui.draw_text('Vida', title_font, WHITE, 50, 15)
        ui.draw_text('Berries: ' + str(player.points), title_font, WHITE, 50, 80)

    # Creamos instancia Ui para guardar la pantalla
    ui = Ui()

    last_attack_time = pygame.time.get_ticks()

    # Creamos observador de salud
    health_observer = Ui.HealthObserver(30, 45, ui.display_surface, player.health, player.health)
    player.register(health_observer)

    # Variables de movimiento
    move_left = False
    move_right = False

    screen_scroll = 0
    bg_scroll = 0
    SumaTotalScrenScroll = 0
    last_contact_time = 0
    whale_dead = False
    

    # Bucle principal del juego
    run = True
    while run:
        # Establecer la velocidad del juego
        clock.tick(FPS)
        draw_bg()
        # Realiza las animaciones
        player.update(screen_scroll)

        # Restaurar el estado de movimiento después de salir del bucle de pausa
        
        # Muestra enemigo
        #enemy.draw(SCREEN)

        # Muestra pinchos
        # spikes.draw(SCREEN)

        # Se dibuja antes del jugador para que este se vea por delante de la puerta
        world.item_door.update(screen_scroll)
        world.item_door.draw(SCREEN)
        # quiero ver el collision rect de la puerta
        for door in world.item_door:
            pygame.draw.rect(SCREEN, (255, 0, 0), door.collision_rect, 2)


        # Dibujar jugador
        player.draw(SCREEN)

        # Verificar si el enemigo está atacando al pirata
        # enemy.attack(player)ddw

        # dibujar items y pintarlos
        world.item_boxes_Group.update(screen_scroll)
        world.enemy_group.update(screen_scroll)
        world.item_boxes_Group.draw(SCREEN)
        world.spikes_group.update(screen_scroll)
        world.spikes_group.draw(SCREEN)
        
        world.item_boots.draw(SCREEN)                
        world.item_boots.update(screen_scroll)

        world.item_blocks.update(screen_scroll)
    
        if not whale_dead:              
            for enemy in world.enemy_group:
                if isinstance(enemy, Enemies.Enemy.WhaleEnemy) and enemy.health <= 0:
                    whale_dead = True
                    ## aparecen las botas
                    boota = world.item_boots.sprites()[0]               
                    boota.rect.midtop = (boota.rect.midtop[0], boota.rect.midtop[1] / 3)
                    

        for enemy in world.enemy_group:
            enemy.draw(SCREEN)

        screen_scroll = player.move(move_left, move_right, world, bg_scroll)
        bg_scroll -= screen_scroll

        SumaTotalScrenScroll -= screen_scroll

        

        # Actualiza la accion del jugador y enemigos
        if player.attack:
            player.update_action(3)  # 3 -> animacion ataque
            for enemy in world.enemy_group:
                if player.rect.colliderect(enemy.rect):
                    current_time = pygame.time.get_ticks()
                    if current_time - last_attack_time > ATAQUE_COOLDOWN:
                        last_attack_time = current_time
                        enemy.get_Hit(ATAQUE+(player.points*10))
                        enemy.update_action(3)
                        # Reproducir sonido de la espada al atacar
                        espada.play()
                    if enemy.health == 0:
                        enemy.update_action(4)

        elif player.in_air:
            player.update_action(2)  # 2 -> animacion jump
        elif move_left or move_right:
            player.update_action(1)  # 1 -> animacion run
        else:
            player.update_action(0)  # 0 -> animacion idle

        # haz que el enemigo se mueva mas rapido que el jugador
        for enemy in world.enemy_group:
            enemy.ai(player)
        # enemy_group.update(screen_scroll)
        # spikes.update(screen_scroll)

        for spikes in world.spikes_group:
            if player.rect.colliderect(spikes.rect):
                current_time = pygame.time.get_ticks()
                if current_time - last_contact_time > 1:
                    last_contact_time = current_time
                    player.get_Hit(8)


        for block in world.item_blocks:
            block.draw(SCREEN)
            if player.got_sword == True and block.collision_rect.colliderect(player.collision_rect):
                block.do_destroy(SCREEN)
        

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
                if event.type == pygame.K_ESCAPE: # no entiendo este if no seria key 
                    run = False
                if event.key == pygame.K_p:
                    paused_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_SPACE:
                    player.attack = False

        
        for door in world.item_door:
            if player.rect.colliderect(door.rect) and player.got_key:
                door.set_open()  # Establece la puerta como abierta
                if level_num < MAX_LEVELS:
                    world.reset_world()
                    level_num += 1
                    level = LevelGenerator(level_num)
                    tiles = level.load_level()  
                    world.process_data(tiles)
                else:
                    print("INSERTAR INDICADOR DE QUE SE TERMINO EL JUEGO")
                    # Pantalla negra con mensaje o algo asi
            elif not door.is_open():
                door.set_closed()  # Establece la puerta como cerrada

        if player.health <= 0:
            musica.stop()
            # le pasamos level_num a main para que sepa en que nivel murio
            main(level_num)

        pygame.display.update()

    # Salir del juego
    pygame.quit()


if __name__ == "__main__":
    main_menu()
    if menu.game_started:
        main(level_num)