import pygame
import os



# Variables de entorno
GRAVITY = 0.75
TILE_SIZE = 40

# Cargar imagenes
health_box_img = pygame.image.load('assets/items/Health/0.png')
key_box_img = pygame.image.load('assets/items/Keys/0.png')
berries_box_img = pygame.image.load('assets/items/gold/0.png')

item_boxes = {
    'Health': health_box_img,
    'Key': key_box_img,
    'Berries': berries_box_img
}


# Clase pirata
class Pirate(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.jump = False
        self.double_jump = True
        self.in_air = True  # Para saber si el player ya ha saltado
        self.vel_y = 0  # Controla cuanto salta el player
        self.attack = False
        self.health = 100
        self.observers = []

        self.animation_list = []  # Lista de listas
        self.frame_index = 0
        self.action = 0  # Cada animacion trenda un int accion asociado
        self.update_time = pygame.time.get_ticks()

        # Tipos de animaciones
        animation_types = ['Idle', 'Run', 'Jump', 'Attack']

        # Bucle que comprueba que animacion hacer
        for animation in animation_types:
            temp_list = []  # Reseteamos lista temporal

            # Contamos n de ficheros en la carpeta
            n_frames = len(os.listdir(f'assets/player/{animation}'))
            for i in range(n_frames):
                img = pygame.image.load(f'assets/player/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)  # Guardamos en la lista de listas el contenido de la lista temporal

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

    # Dibujar el pirata en la pantalla
    def draw(self):
        from main import screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 4,
                                          self.rect.centery - self.rect.height / 2, self.rect.width / 2,
                                          self.rect.height)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)  # 2 es el grosor del borde

    def move(self, move_left, move_right, tiles):
        # Resetear variables de movimiento
        dx = 0
        dy = 0
        col_tiles = pygame.sprite.spritecollide(self, tiles, False)
        # Asignar movimiento izquierdo y derecho
        if move_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
            for tile in col_tiles:
                if tile.rect.x < self.rect.x:
                    dx = 0

        if move_right:
            dx += self.speed
            self.flip = False
            self.direction = 1
            for tile in col_tiles:
                if tile.rect.x > self.rect.x:
                    dx = 0

        # Salto
        if self.jump == True and self.in_air == False:  # self.in_air a False impide doble salto
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # Aplicamos gravedad
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Actualizar la posición del jugador
        self.rect.x += dx
        self.rect.y += dy

    def check_collision(self, tiles):
        col_tiles = pygame.sprite.spritecollide(self, tiles, False)
        for tile in col_tiles:
            if tile.collision_rect.bottom > self.rect.y and (tile.collision_rect.left > self.rect.x):  # Suelo
                self.vel_y = 0
                self.rect.bottom = tile.rect.top
                self.in_air = False
                self.double_jump = True
                self.rect.y = self.rect.y
            if tile.collision_rect.top < self.rect.y and (tile.collision_rect.left > self.rect.x):  # Techo
                self.vel_y = 0
                self.rect.top = tile.rect.bottom
                self.rect.y = self.rect.y

    # Actualizar la animación
    def update_animation(self):

        ANIMATION_COOLDOWN = 100
        if self.action == 3:  # Si la acción es de ataque reducimos cooldown entre frames
            ANIMATION_COOLDOWN = 10

        # Actualizar imagen de la animación dependiendo del frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Actualizar la animación
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Si la animación ha terminado, reiniciar
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    # Actualiza la accion 
    def update_action(self, new_action, tiles):
        # Comprueba si la acción actual es diferente a la anterior
        self.check_collision(tiles)
        if new_action != self.action:
            self.action = new_action
            # Actualizamos los nuevos valores
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    ############ PATRON OBSERVADOR

    # Funcion de daño
    def get_Hit(self, damage):
        self.health -= damage
        self.notify_observers()

    # Registra el observador en la lista
    def register(self, observer):
        self.observers.append(observer)

    # Notifica a los observadores de los cambios
    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)


############

class CollectBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, scale, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE //  2, y + (TILE_SIZE - self.image.get_height()))
        self.player = player

    def update(self):
        # Confirmar que el pirata coge el item
        if pygame.sprite.collide_rect(self, self.player):
            if self.item_type == 'Health':
                if self.player.health <  100:
                    self.player.health +=  25
                    if self.player.health >  100:
                        self.player.health = 100
            elif self.item_type == 'Key':
                print('Has cogido una llave')
            elif self.item_type == 'Berries':
                print('Has cogido una moneda')
                if self.player.health <  100:
                    self.player.health +=  5
                    if self.player.health >  100:
                        self.player.health = 100

            self.kill()
