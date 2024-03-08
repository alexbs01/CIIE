import pygame
from entities.enemies.enemies import CucumberEnemy, Spike, Capitan, badPirate, WhaleEnemy
from items import Collectables as Collectables
from settings import *
from items import Interactives as Interactives

class World():

    def __init__(self, resource_manager, player):
        self.obstacle_list = []
        self.bg_list = []
        self.resource_manager = resource_manager
        self.player = player
        
        # Grupos de Sprites
        self.item_boxes_Group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.spikes_group = pygame.sprite.Group()
        self.item_boots = pygame.sprite.Group()
        self.item_door = pygame.sprite.Group()
        self.item_blocks = pygame.sprite.Group()

    # Funcion que procesara la matriz de tiles y creará los objetos necesarios
    def process_data(self, data):
        self.level_length = len(data[0])

        # Diccionario de Entidades asociadas a su valor de tile
        tile_actions = {
            11: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Sword', x * TILE_WIDTH, y * TILE_HEIGHT, 0.25, self.player)),  # Objeto recogible: Espada
            14: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Key', x * TILE_WIDTH, y * TILE_HEIGHT, 0.25, self.player)),  # Objeto recogible: Llave
            17: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Berries', x * TILE_WIDTH, y * TILE_HEIGHT, 1.25, self.player)),  # Objeto recogible: Moneda
            18: lambda x, y: self.item_boots.add(Collectables.Collectables('Boots', x * TILE_WIDTH, y * TILE_HEIGHT * 3, 2.25, self.player)),  # Objeto recogible: Botas
            19: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Health', x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.player)),  # Objeto recogible: Salud
            13: lambda x, y: self.enemy_group.add(Capitan(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Capitán
            15: lambda x, y: self.enemy_group.add(badPirate(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Pirata malo
            16: lambda x, y: self.enemy_group.add(CucumberEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Cucumber
            20: lambda x, y: self.spikes_group.add(Spike(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Obstáculo: Pinchos
            21: lambda x, y: self.enemy_group.add(WhaleEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Ballena
            12: lambda x, y: (self.item_blocks.add(Interactives.Interactive_obj.Block(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)), self.obstacle_list.append((img, rect))),  # Bloque interactivo
            24: lambda x, y: self.item_door.add(Interactives.Interactive_obj.Door(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Objeto interactivo: Puerta
        }


        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img_path = "assets/tiles/" + str(tile) + ".png"
                    img = self.resource_manager.load_image(img_path, img_path)
                    rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))

                    if tile in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24):
                        tile_actions[tile](x, y)
                    # Tiles que tendrán colisiones
                    elif 0 <= tile <= 9 or 22 <= tile <= 23 or tile == 36 or 41 <= tile <= 49:
                        self.obstacle_list.append((img, rect))
                    # Tiles que estarán de fondo, decorativos
                    elif 25 <= tile <= 35 or 37 <= tile <= 39:
                        self.bg_list.append((img, rect))

    def draw(self,screen, screen_scroll):
        # Dibujamos los tiles que serán obstaculos y los de bg
        for tile in self.obstacle_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])

        for tile in self.bg_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])   

    def reset_world(self, level_num):
        self.item_boxes_Group.empty()
        self.enemy_group.empty()
        self.spikes_group.empty()
        self.item_boots.empty()
        self.item_door.empty()
        self.item_blocks.empty()

        self.obstacle_list.clear()
        self.bg_list.clear()
        
        self.player.got_key = False
        # CAMBIAR LA X E Y DEL PIRATA AL ENTRAR EN EL NUEVO MAPA
        # tiene que empezar abajo a la derecha sin importar donde abra la puerta
        if level_num == 2:
        # resetear la posicion del jugador
            self.player.rect.x = 200
            self.player.rect.y = 600
        else:
            self.player.rect.x = 250
            self.player.rect.y = 600

    


