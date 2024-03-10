import pygame
from settings import *
from Escena import Escena
from items.Collectables import Collectables
from entities.enemies import enemies
from entities.Ui import Ui
from entities.pirate import Pirate
from items.Interactives import Interactive_obj
import csv
from world_generation.ResourceManager import ResourceManager
from PausaMenu import Pausa


class Level(Escena):

    def __init__(self, director, player_status, csv):

        Escena.__init__(self, director)

        self.csv = csv
        self.player = None

        self.resource_manager = ResourceManager()

        # Grupos de Sprites
        self.item_boxes_Group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.spikes_group = pygame.sprite.Group()
        self.item_boots = pygame.sprite.Group()
        self.item_door = pygame.sprite.Group()
        self.item_blocks = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.obstacle_list = [] # Lista para tiles con colisiones
        self.bg_list = [] # Lista para tiles de decoracion

        self.load_level()

        #self.init_observers()

        self.player.set_stats_dto(player_status)

        # Crear la musica de fondo  


    def load_level(self):

        tiles = []

        with open(self.csv, newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=',')

            for row in range(ROWS):
                r = [-1] * COLS
                tiles.append(r)

            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    tiles[x][y] = int(tile)

        level_length = len(tiles[0])

        # Diccionario de Entidades asociadas a su valor de tile
        tile_actions = {
            23: lambda x, y: self.set_player(Pirate('pirate', x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),
            11: lambda x, y: self.item_boxes_Group.add(Collectables('Sword', x * TILE_WIDTH, y * TILE_HEIGHT, self.player)),  # Objeto recogible: Espada
            14: lambda x, y: self.item_boxes_Group.add(Collectables('Key', x * TILE_WIDTH, y * TILE_HEIGHT, self.player)),  # Objeto recogible: Llave
            17: lambda x, y: self.item_boxes_Group.add(Collectables('Berries', x * TILE_WIDTH, y * TILE_HEIGHT, self.player)),  # Objeto recogible: Moneda
            18: lambda x, y: self.item_boots.add(Collectables('Boots', x * TILE_WIDTH, y * TILE_HEIGHT * 3, self.player)),  # Objeto recogible: Botas
            19: lambda x, y: self.item_boxes_Group.add(Collectables('Health', x * TILE_WIDTH, y * TILE_HEIGHT, self.player)),  # Objeto recogible: Salud
            13: lambda x, y: self.enemy_group.add(enemies.Capitan(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Capitán
            15: lambda x, y: self.enemy_group.add(enemies.badPirate(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Pirata malo
            16: lambda x, y: self.enemy_group.add(enemies.CucumberEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Cucumber
            20: lambda x, y: self.spikes_group.add(enemies.Spike(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Obstáculo: Pinchos
            21: lambda x, y: self.enemy_group.add(enemies.WhaleEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Ballena
            12: lambda x, y: (self.item_blocks.add(Interactive_obj.Block(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)), self.obstacle_list.append((img, rect))),  # Bloque interactivo
            24: lambda x, y: self.item_door.add(Interactive_obj.Door(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Objeto interactivo: Puerta
        }


        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img_path = "assets/tiles/" + str(tile) + ".png"
                    img = pygame.image.load(img_path)
                    rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))

                    if tile in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24):
                        tile_actions[tile](x, y)
                    # Tiles que tendrán colisiones
                    elif 0 <= tile <= 9 or 22 <= tile <= 23 or tile == 36 or 41 <= tile <= 49:
                        self.obstacle_list.append((img, rect))
                    # Tiles que estarán de fondo, decorativos
                    elif 25 <= tile <= 35 or 37 <= tile <= 39:
                        self.bg_list.append((img, rect))


    def set_player(self, player):
        self.player = player

    def events(self, events_list):
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                # Si la tecla es Escape
                if event.key == pygame.K_ESCAPE:
                    # Se sale del programa
                    self.director.quit_program()
                if event.key == pygame.K_p:
                    pause = Pausa(self.director)
                    self.director.stack_scene(pause)

            if event.type == pygame.QUIT:
                self.director.quit_program()

    
    
    def draw (self, screen):

        screen.fill(BG2)

        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])

        for tile in self.bg_list:
            screen.blit(tile[0], tile[1])

        self.item_blocks.draw(screen)
        self.item_boots.draw(screen)
        self.item_door.draw(screen)
        self.spikes_group.draw(screen)
        self.item_boxes_Group.draw(screen)
        # Se pinta en este orden para que el jugador quede por delante de los objetos 
        # anteriores, pero detras de los enemigos

        self.player.draw(screen)
        self.enemy_group.draw(screen)



        # Muestra barra de salud por encima de los tiles
        title_font = pygame.font.Font("assets/inmortal.ttf", 25)

        #Ui.draw_text('Vida', title_font, WHITE, 50, 15)
        #Ui.draw_text('Berries: ' + str(self.player.points), title_font, WHITE, 50, 80)

    def update(self, time, screen_scroll, bg_scroll):

        for tile in self.obstacle_list:
            tile[1].x += screen_scroll

        for tile in self.bg_list:
            tile[1].x += screen_scroll

        # Actualiza el jugador
        self.player.update(screen_scroll,self.obstacle_list, bg_scroll)
        self.enemy_group.update(screen_scroll)
        self.spikes_group.update(screen_scroll)
        self.item_boxes_Group.update(screen_scroll)
        self.item_boots.update(screen_scroll)
        self.item_door.update(screen_scroll)
        self.item_blocks.update(screen_scroll)
