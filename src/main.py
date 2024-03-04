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


def main():
    # Reproducir el sonido de fondo en un bucle continuo
    musica.play(-1)  # El argumento -1 indica que el sonido se reproduce en un bucle infinito

    # En tu juego principal
    resource_manager = ResourceManager()

    # Guarda la posición inicial del pirata
    initial_player_x = 200
    initial_player_y = 600

    # Creamos jugador y enemigo
    player = pirate.Pirate('pirate', initial_player_x, initial_player_y, 1, 6, resource_manager)
    spikes = Enemies.Enemy.Spike(640, 545, resource_manager)
    world = World(resource_manager)

    level0 = LevelGenerator(PATH_LEVEL_3)
    tiles = level0.load_level()

    # Dibuja el mapa
    world.process_data(tiles)

    # Grupos de Sprites
    item_boxes_Group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    spikes_group = pygame.sprite.Group()
    item_boots = pygame.sprite.Group()
    item_door = pygame.sprite.Group()
    item_blocks = pygame.sprite.Group()

    # Creamos objetos recogibles
    for row_index, row in enumerate(tiles):
        for col_index, column in enumerate(row):
            if column == 19:
                item_box = Collectables.Collectables('Health', col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 1.25,
                                                     player)
                item_boxes_Group.add(item_box)
            elif column == 16:
                enemy = Enemies.Enemy.CucumberEnemy(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 1,
                                                    resource_manager)
                enemy_group.add(enemy)
            elif column == 13:
                enemy = Enemies.Enemy.Capitan(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 1,
                                                    resource_manager)
                enemy_group.add(enemy)
            elif column == 15:
                enemy = Enemies.Enemy.badPirate(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 1,
                                                    resource_manager)
                enemy_group.add(enemy)
            elif column == 20:
                spike = Enemies.Enemy.Spike(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, resource_manager)
                spikes_group.add(spike)
            elif column == 21:
                enemy = Enemies.Enemy.WhaleEnemy(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 1,
                                                    resource_manager)
                enemy_group.add(enemy)
            elif column == 17:
                item_box = Collectables.Collectables('Berries', col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 1.25, player)
                item_boxes_Group.add(item_box)
            elif column == 18:
                item_bota = Collectables.Collectables('Boots', col_index * TILE_WIDTH , row_index * TILE_HEIGHT * 3, 2.25, player)
                item_boots.add(item_bota) 
            elif column == 14:
                item_box = Collectables.Collectables('Key', col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 0.25, player)
                item_boxes_Group.add(item_box)
            elif column == 24:
                door = Interactives.Interactive_obj.Door(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, resource_manager)
                item_door.add(door)
            elif column == 12:
                block = Interactives.Interactive_obj.Block(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, resource_manager)
                item_blocks.add(block)
            elif column == 11:
                item_box = Collectables.Collectables('Sword', col_index * TILE_WIDTH, row_index * TILE_HEIGHT, 0.25, player)
                item_boxes_Group.add(item_box)

    
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

        # Controla el scroll de los tiles
        world.draw(SCREEN, screen_scroll)

        # Muestra barra de salud por encima de los tiles
        health_observer.update_health(player.health)
        title_font = pygame.font.Font("assets/inmortal.ttf", 25)

        ui.draw_text('Vida', title_font, WHITE, 50, 15)
        ui.draw_text('Berries: ' + str(player.points), title_font, WHITE, 50, 80)

        # # Mostrar imagen dungeon
        # width = dungeon_img.get_width()
        # for x in range(4):
        #     SCREEN.blit(dungeon_img, ((x * width) - bg_scroll, 0))

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
        item_door.update(screen_scroll)
        item_door.draw(SCREEN)
        # quiero ver el collision rect de la puerta
        for door in item_door:
            pygame.draw.rect(SCREEN, (255, 0, 0), door.collision_rect, 2)


        # Dibujar jugador
        player.draw(SCREEN)

        # Verificar si el enemigo está atacando al pirata
        # enemy.attack(player)ddw

        # dibujar items y pintarlos
        item_boxes_Group.update(screen_scroll)
        enemy_group.update(screen_scroll)
        item_boxes_Group.draw(SCREEN)
        spikes_group.update(screen_scroll)
        spikes_group.draw(SCREEN)
        
        item_boots.draw(SCREEN)                
        item_boots.update(screen_scroll)

        item_blocks.update(screen_scroll)
    
        if not whale_dead:              
            for enemy in enemy_group:
                if isinstance(enemy, Enemies.Enemy.WhaleEnemy) and enemy.health <= 0:
                    whale_dead = True
                    ## aparecen las botas
                    boota = item_boots.sprites()[0]               
                    boota.rect.midtop = (boota.rect.midtop[0], boota.rect.midtop[1] / 3)
                    

        for enemy in enemy_group:
            enemy.draw(SCREEN)

        screen_scroll = player.move(move_left, move_right, world, bg_scroll)
        bg_scroll -= screen_scroll

        SumaTotalScrenScroll -= screen_scroll

        

        # Actualiza la accion del jugador y enemigos
        if player.attack:
            player.update_action(3)  # 3 -> animacion ataque
            for enemy in enemy_group:
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
        for enemy in enemy_group:
            enemy.ai(player)
        # enemy_group.update(screen_scroll)
        # spikes.update(screen_scroll)

        for spikes in spikes_group:
            if player.rect.colliderect(spikes.rect):
                current_time = pygame.time.get_ticks()
                if current_time - last_contact_time > 1:
                    last_contact_time = current_time
                    player.get_Hit(8)


        for door in item_door:
            if player.rect.colliderect(door.rect) and player.got_key:
                door.set_open()  # Establece la puerta como abierta
                player.got_key = False
            elif not door.is_open():
                door.set_closed()  # Establece la puerta como cerrada

        for block in item_blocks:
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

        if player.health <= 0:
            musica.stop()
            main()

        pygame.display.update()

    # Salir del juego
    pygame.quit()


if __name__ == "__main__":
    main_menu()
    if menu.game_started:
        main()