import pygame
from settings import *
from escene.Escena import Escena
from items.Collectables import Collectables
from entities.enemies import enemies
from entities.Ui import Ui
from entities.pirate import Pirate
from items.Interactives import Interactive_obj
import csv
from world_generation.ResourceManager import ResourceManager
from escene.pause.PausaMenu import Pausa


class Level(Escena):

    def __init__(self, director, player_status, csv):

        Escena.__init__(self, director)

        self.csv = csv # Variable con el mapa en formato csv
        self.player = None # Variable para el jugador
        self.screen_scroll = 0
        self.bg_scroll = 0
        self.resource_manager = ResourceManager()

        # Guardamos la superficie superficie
        self.display_surface = pygame.display.get_surface()

        # Grupos de Sprites
        self.item_boxes_Group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.spikes_group = pygame.sprite.Group()
        self.item_door = pygame.sprite.Group()
        self.item_blocks = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.obstacle_list = [] # Lista para tiles con colisiones
        self.bg_list = [] # Lista para tiles de decoracion

        self.load_level() # Cargamos el nivel

        self.player.set_stats_dto(player_status) # Cargamos el status del pirata
        self.ui_instance = Ui(self.display_surface)

        # Creamos los observadores del nivel
        self.health_observer = None
        self.points_observer = None
        self.key_observer = None
        self.sword_observer = None
        self.boots_observer = None

        self.init_observers()

        # Observadores para vida enemigos
        self.enemy_observers = []
        for enemy in self.enemy_group:
            health_observer = self.ui_instance.EnemyHealthObserver(enemy, self.display_surface, enemy.health)
            self.enemy_observers.append(health_observer)
            enemy.add_observer(health_observer)

        # Registrar observadores en el jugador
        self.player.add_observer(self.health_observer)
        self.player.add_observer(self.points_observer)
        self.player.add_observer(self.key_observer)
        self.player.add_observer(self.sword_observer)
        self.player.add_observer(self.boots_observer)


        # Creamos el sonido de la espada
        self.espada = self.resource_manager.get_resource("espadaSound")
        if self.espada is None:
            self.espada = self.resource_manager.load_resource("espadaSound", "./assets/Music/Espada.ogg", "sound")
        self.espada.set_volume(EFFECTS_VOLUME)

    def load_level(self):

        tiles = [] # Variable con los numeros de las posiciones de la matriz

        with open(self.csv, newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=',')

            for row in range(ROWS):
                r = [-1] * COLS
                tiles.append(r)

            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    tiles[x][y] = int(tile)

        # Diccionario de Entidades asociadas a su valor de tile
        tile_actions = {
            23: lambda x, y: self.set_player(Pirate('pirate', x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),
            11: lambda x, y: self.item_boxes_Group.add(Collectables('Sword', x * TILE_WIDTH, y * TILE_HEIGHT, False)),  # Objeto recogible: Espada
            14: lambda x, y: self.item_boxes_Group.add(Collectables('Key', x * TILE_WIDTH, y * TILE_HEIGHT, False if self.csv == PATH_LEVEL_3 else True)),  # Objeto recogible: Llave
            17: lambda x, y: self.item_boxes_Group.add(Collectables('Berries', x * TILE_WIDTH, y * TILE_HEIGHT, True)),  # Objeto recogible: Moneda
            18: lambda x, y: self.item_boxes_Group.add(Collectables('Boots', x * TILE_WIDTH, y * TILE_HEIGHT, False)),  # Objeto recogible: Botas
            19: lambda x, y: self.item_boxes_Group.add(Collectables('Health', x * TILE_WIDTH, y * TILE_HEIGHT, True)),  # Objeto recogible: Salud
            13: lambda x, y: self.enemy_group.add(enemies.Capitan(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Capitán
            15: lambda x, y: self.enemy_group.add(enemies.badPirate(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Pirata malo
            16: lambda x, y: self.enemy_group.add(enemies.CucumberEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Cucumber
            20: lambda x, y: self.spikes_group.add(enemies.Spike(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Obstáculo: Pinchos
            21: lambda x, y: self.enemy_group.add(enemies.WhaleEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Ballena
            49: lambda x, y: self.enemy_group.add(enemies.Marine(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Jefe de marines
            50: lambda x, y: self.enemy_group.add(enemies.MarineBoss(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Enemigo: Jefe de marines
            12: lambda x, y: (self.item_blocks.add(Interactive_obj.Block(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)), self.obstacle_list.append((img, rect, tile_id))),  # Bloque interactivo
            24: lambda x, y: self.item_door.add(Interactive_obj.Door(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Objeto interactivo: Puerta
        }


        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img_path = "assets/tiles/" + str(tile) + ".png"
                    img = pygame.image.load(img_path)
                    rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                    tile_id = tile
                    if tile in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 49, 50):
                        tile_actions[tile](x, y)
                    # Tiles que tendrán colisiones
                    elif 0 <= tile <= 9 or 22 <= tile <= 23 or tile == 36 or 41 <= tile <= 49:
                        self.obstacle_list.append((img, rect, tile_id))
                    # Tiles que estarán de fondo, decorativos
                    elif 25 <= tile <= 35 or 37 <= tile <= 39:
                        self.bg_list.append((img, rect, tile_id))


    def set_player(self, player):
        self.player = player

    # Inicializa los observadores
    def init_observers(self):
        self.health_observer = self.ui_instance.HealthObserver(30, 45, self.display_surface, self.player.health)
        self.points_observer = self.ui_instance.PointsObserver(self.player.points)
        self.key_observer = self.ui_instance.KeyObserver(self.display_surface)
        self.sword_observer = self.ui_instance.SwordObserver(self.display_surface)
        self.boots_observer = self.ui_instance.BootsObserver(self.display_surface)



    def events(self, events_list):
        current_time = pygame.time.get_ticks()
        #print(current_time)
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.move_left = True
                if event.key == pygame.K_d:
                    self.player.move_right = True
                if event.key == pygame.K_w:
                    self.player.jump = True
                # Se realizará un cooldown para no poder atacar seguido
                if event.key == pygame.K_SPACE and current_time - self.player.last_attack_time > ATAQUE_COOLDOWN:
                    self.player.last_attack_time = current_time
                    self.player.attack = True
                    self.espada.play(1)
                   
                # Si la tecla es Escape
                if event.key == pygame.K_ESCAPE:
                    # Se sale del programa
                    self.director.quit_program()
                if event.key == pygame.K_p:
                    self.director.pause_music()
                    pause = Pausa(self.director)
                    self.director.stack_scene(pause)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.move_left = False
                if event.key == pygame.K_d:
                    self.player.move_right = False
                if event.key == pygame.K_SPACE:
                    self.player.attack = False

            if event.type == pygame.QUIT:
                self.director.quit_program()

    
    
    def draw (self, screen):

        screen.fill(BG2)

        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])

        for tile in self.bg_list:
            screen.blit(tile[0], tile[1])

        self.item_blocks.draw(screen)
        self.item_door.draw(screen)
        self.spikes_group.draw(screen)
        # Se pinta en este orden para que el jugador quede por delante de los objetos 
        # anteriores, pero detras de los enemigos

        self.player.draw(screen)
        for enemy in self.enemy_group:
            enemy.draw(screen)

        for item in self.item_boxes_Group:
            item.draw(screen)

        for observer, enemy in zip(self.enemy_observers, self.enemy_group):
            observer.notify(enemy.health)

        # Muestra barra de salud por encima de los tiles
        title_font = self.resource_manager.get_resource("fuentePrincipal")
        if title_font is None:
            title_font = self.resource_manager.load_resource("fuentePrincipal","assets/inmortal.ttf","font",25)


        self.health_observer.notify(self.player.health)
        self.key_observer.notify(self.player.got_key)
        self.sword_observer.notify(self.player.got_sword)
        self.boots_observer.notify(self.player.got_boots)
        self.points_observer.notify(self.player.points)
        self.ui_instance.draw_text('Vida', title_font, WHITE, 50, 15)
        self.ui_instance.draw_text('Berries: ' + str(self.player.points), title_font, WHITE, 50, 80)
        self.ui_instance.draw_text('Items:', title_font, WHITE, 50, 110)


    def update(self, time):

        # Implementa el scroll en los tiles que no son Objetos
        for tile in self.obstacle_list:
            tile[1].x += self.screen_scroll

        for tile in self.bg_list:
            tile[1].x += self.screen_scroll

        # Actualiza las acciones del jugador 
        if self.player.attack:
            self.player.update_action(3)  # 3 -> animacion ataque
            for enemy in self.enemy_group:
                if self.player.rect.colliderect(enemy.rect): # Si el jugador colisiona con algun enemigo
                    current_time = pygame.time.get_ticks()
                    if current_time - enemy.last_attack_time > ATAQUE_COOLDOWN:
                        enemy.last_attack_time = current_time
                        enemy.get_Hit(self.player.damage+(self.player.points*10))
                        enemy.update_action(3)
                    if enemy.health == 0:
                        enemy.update_action(4)

        elif self.player.in_air:
            self.player.update_action(2)  # 2 -> animacion jump
        elif self.player.move_left or self.player.move_right:
            self.player.update_action(1)  # 1 -> animacion run
        else:
            self.player.update_action(0)  # 0 -> animacion idle 

        # Hacemos que el pirata se mueva       
        self.move()

        # Actualizamos el valor del scroll
        self.bg_scroll -= self.screen_scroll

        # Hacemos que los enemigos ataquen y se muevan
        for enemy in self.enemy_group:
            enemy.ai(self.player)

        for spikes in self.spikes_group:
            if self.player.rect.colliderect(spikes.rect):
                current_time = pygame.time.get_ticks()
                if current_time - spikes.last_contact_time > 0:
                    spikes.last_contact_time = current_time
                    self.player.get_Hit(SPIKE_DAMAGE)

                  
        self.player.update(self.screen_scroll, self.bg_scroll)
        self.enemy_group.update(self.screen_scroll)
        self.spikes_group.update(self.screen_scroll)
        self.item_boxes_Group.update(self.screen_scroll, self.player)
        self.item_door.update(self.screen_scroll)
        self.item_blocks.update(self.screen_scroll)



    def check_collision(self, dx, dy):
        for tile in self.obstacle_list:
            if tile[2] == 12:  # Verifica si el tile es un bloque (id = 12)
                if self.player.got_sword and self.player.attack and self.player.direction == 1:  # Verifica si el jugador tiene la espada
                    if tile[1].colliderect(self.player.rect):
                        # Busca el bloque en el grupo de bloques para eliminarlo
                        for block in self.item_blocks:
                            if block.rect == tile[1]: # Comprueba que sus rect sean iguales
                                block.kill()
                                self.obstacle_list.remove(tile)  # Elimina el bloque de la lista
                else:
                    if tile[1].colliderect(self.player.collision_rect.x + dx, self.player.collision_rect.y, self.player.collision_rect.width, self.player.collision_rect.height):
                        dx = 0
                    if tile[1].colliderect(self.player.collision_rect.x, self.player.collision_rect.y + dy, self.player.collision_rect.width, self.player.collision_rect.height):
                        if self.player.vel_y < 0:
                            self.player.vel_y = 0
                            dy = tile[1].bottom - self.player.collision_rect.top
                        elif self.player.vel_y >= 0:
                            self.player.vel_y = 0
                            self.player.in_air = False
                            self.player.jumps = 0
                            dy = tile[1].top - self.player.collision_rect.bottom
            else:  # Lógica para los tiles que no son del tipo 12
                if tile[1].colliderect(self.player.collision_rect.x + dx, self.player.collision_rect.y, self.player.collision_rect.width, self.player.collision_rect.height):
                    dx = 0
                if tile[1].colliderect(self.player.collision_rect.x, self.player.collision_rect.y + dy, self.player.collision_rect.width, self.player.collision_rect.height):
                    if self.player.vel_y < 0:
                        self.player.vel_y = 0
                        dy = tile[1].bottom - self.player.collision_rect.top
                    elif self.player.vel_y >= 0:
                        self.player.vel_y = 0
                        self.player.in_air = False
                        self.player.jumps = 0
                        dy = tile[1].top - self.player.collision_rect.bottom
        return dx, dy
    
    def move(self):

            # Resetear variables de movimiento
            dx = 0
            dy = 0

            if self.player.move_left:
                dx -= self.player.speed
                self.player.flip = True
                self.player.direction = -1


            if self.player.move_right:
                dx += self.player.speed
                self.player.flip = False
                self.player.direction = 1


            # Salto
            if self.player.jumps < self.player.max_jumps and self.player.jump:  # self.in_air a False impide doble salto
                self.player.in_air == False
                self.player.vel_y = -11
                self.player.jump = False
                self.player.in_air = True
                self.player.jumps += 1

            # Aplicamos gravedad
            self.player.vel_y += GRAVITY
            if self.player.vel_y > 10:
                self.player.vel_y = 10
            dy += self.player.vel_y

            # Comprobamos las colisiones del pirata
            dx,dy = self.check_collision(dx, dy)

            # Mira que no pueda pasar mas alla de la pantalla
            if self.player.collision_rect.left + dx < 0 or self.player.collision_rect.right + dx > SCREEN_WIDTH:
                dx = 0


            # Actualizar la posición del jugador
            self.player.rect.x += dx
            self.player.rect.y += dy

            # Hace el scroll de la pantalla                                     # Tamaño del nivel en pixeles
            if self.player.rect.right > SCREEN_WIDTH - SCREEN_THRESH and self.bg_scroll < (150 * TILE_SIZE) - SCREEN_WIDTH:
                self.player.rect.x -= dx
                self.screen_scroll = -dx
            elif self.player.rect.left < SCREEN_THRESH and self.bg_scroll > abs(dx):
                self.player.rect.x -= dx
                self.screen_scroll = -dx
            else:
                self.screen_scroll = 0

