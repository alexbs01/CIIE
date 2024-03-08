import pygame
from settings import *
from Escena import Escena
from items.Collectables import Collectables
from entities.enemies import enemies
from entities.Ui import Ui
from items.Interactives import Interactive_obj

class Level(Escena):

    def __init__(self, director, player_status):
        Escena.__init__(self, director)
        self.obstacle_list = []
        self.bg_list = []
       
       # Grupos de Sprites
        self.item_boxes_Group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.spikes_group = pygame.sprite.Group()
        self.item_boots = pygame.sprite.Group()
        self.item_door = pygame.sprite.Group()
        self.item_blocks = pygame.sprite.Group()

        self.player = None
        # CREAR METODO set_status en clase pirate, que reciba un status 
        # y haga self.health = status.health y self.points = status.points
        # creo que hay que crear clase status
        self.player.set_status = player_status


        #Crea un objecto de tipo UI 
        self.ui = Ui()
        health_observer = Ui.HealthObserver(30, 45, self.ui.display_surface, self.player.health, self.player.health)
        self.player.register(health_observer)

        # Crea un objeto de tipo UI para las berries
        berries_observer = Ui.PointsObserver(self.player.points, MAX_POINTS)
        self.player.register(berries_observer)

        # Crear la musica de fondo  
        pygame.mixer.Sound("./assets/Music/pirates.mp3")
        pygame.mixer.music.play(loops=-1)

        def process_data(self, data):
            self.level_length = len(data[0])

            # Diccionario de Entidades asociadas a su valor de tile
            tile_actions = {
                11: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Sword', x * TILE_WIDTH, y * TILE_HEIGHT, 0.25, self.player)),  # Objeto recogible: Espada
                14: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Key', x * TILE_WIDTH, y * TILE_HEIGHT, 0.25, self.player)),  # Objeto recogible: Llave
                17: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Berries', x * TILE_WIDTH, y * TILE_HEIGHT, 1.25, self.player)),  # Objeto recogible: Moneda
                18: lambda x, y: self.item_boots.add(Collectables.Collectables('Boots', x * TILE_WIDTH, y * TILE_HEIGHT * 3, 2.25, self.player)),  # Objeto recogible: Botas
                19: lambda x, y: self.item_boxes_Group.add(Collectables.Collectables('Health', x * TILE_WIDTH, y * TILE_HEIGHT, 1.25, self.player)),  # Objeto recogible: Salud
                13: lambda x, y: self.enemy_group.add(enemies.Capitan(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Capitán
                15: lambda x, y: self.enemy_group.add(enemies.badPirate(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Pirata malo
                16: lambda x, y: self.enemy_group.add(enemies.CucumberEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Cucumber
                20: lambda x, y: self.spikes_group.add(enemies.Spike(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Obstáculo: Pinchos
                21: lambda x, y: self.enemy_group.add(enemies.WhaleEnemy(x * TILE_WIDTH, y * TILE_HEIGHT, 1, self.resource_manager)),  # Enemigo: Ballena
                12: lambda x, y: (self.item_blocks.add(enemies.Interactives.Interactive_obj.Block(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)), self.obstacle_list.append((img, rect))),  # Bloque interactivo
                24: lambda x, y: self.item_door.add(enemies.Interactives.Interactive_obj.Door(x * TILE_WIDTH, y * TILE_HEIGHT, self.resource_manager)),  # Objeto interactivo: Puerta
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
        
        def events(self, events_list):
            for event in events_list:
                if event.type == pygame.QUIT:
                    self.director.quit_program()
            # Presionar teclas para mover al jugador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_w:
                    self.player.jump = True
                if event.key == pygame.K_SPACE:
                    self.player.attack = True
                if event.type == pygame.K_ESCAPE: # no entiendo este if no seria key 
                    run = False
                if event.key == pygame.K_p:
                    pass
                    #pause = Pause(self.director)
                    #self.director.stack_scene(pause)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_SPACE:
                    self.player.attack = False
        
        def draw (self, data):

            screen.fill(BG2)
            # Controla el scroll de los tiles
            world.draw(SCREEN, screen_scroll)

            process_data(data)
            # Muestra barra de salud por encima de los tiles
            health_observer.update_health(self.player.health)
            title_font = pygame.font.Font("assets/inmortal.ttf", 25)

            Ui.draw_text('Vida', title_font, WHITE, 50, 15)
            Ui.draw_text('Berries: ' + str(self.player.points), title_font, WHITE, 50, 80)

        def update(self,screen_scroll):
            # Actualiza el jugador
            self.player.update()
            self.enemy_group.update()
            self.spikes_group.update()
            self.item_boxes_Group.update()
            self.item_boots.update()
            self.item_door.update()
            self.item_blocks.update()


class Level1(Level):
    def __init__(self, director, player_status):
        super().__init__(director, player_status)

        self.csv_path1 = PATH_LEVEL_1
        
    def notify(self,player):

        if player.health <= 0:
            #dead = Final(self.director, 0, self.player.points)
            self.director.stack_scene(Level1(self.director, self.getterAndSetter))
            #self.director.stack_scene(dead)

        if player.got_key and Interactive_obj.Door.open:
            level = Level2(self.director, self.getterAndSetter)
            self.director.stack_scene(level)
            
            
            # añadirlo a la pila
    

class Level2(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status)

        self.csv_path1 = PATH_LEVEL_2

    def notify(self,player):

        if player.health <= 0:
            #dead = Final(self.director, 0, self.player.points)
            self.director.stack_scene(Level2(self.director, self.getterAndSetter))
            #self.director.stack_scene(dead)

        if player.got_key and Interactive_obj.Door.open:
            level = Level3(self.director, self.getterAndSetter)
            self.director.stack_scene(level)
            
            
            # añadirlo a la pila


class Level3(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status)

        self.csv_path1 = PATH_LEVEL_3

    def notify(self,player):

        if player.health <= 0:
            #dead = Final(self.director, 0, self.player.points)
            self.director.stack_scene(Level3(self.director, self.getterAndSetter))
            #self.director.stack_scene(dead)

        if player.got_key and Interactive_obj.Door.open:
            level = Level2(self.director, self.getterAndSetter)
            self.director.stack_scene(level)
            
            
            # añadirlo a la pila

        

        
            




