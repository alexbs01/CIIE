import pygame
import os
from settings import *

class Pirate(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction =  1
        self.flip = False
        self.jump = False
        self.max_jumps = 2
        self.jumps = 0
        self.in_air = True
        self.vel_y =  0
        self.attack = False
        self.health =  100
        self.observers = []

        self.animation_list = []
        self.frame_index =  0
        self.action =  0
        self.update_time = pygame.time.get_ticks()
        self.resource_manager = resource_manager

        animation_types = ['Idle', 'Run', 'Jump', 'Attack']

        for animation in animation_types:
            temp_list = []
            n_frames = len(os.listdir(f'assets/player/{animation}'))
            for i in range(n_frames):
                img_path = f'assets/player/{animation}/{i}.png'
                img = self.resource_manager.load_image(img_path, img_path)
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

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
        print(col_tiles)
        if move_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
            for tile in col_tiles:
                if tile.collision_rect.x < self.collision_rect.x:
                    dx = 0

        if move_right:
            dx += self.speed
            self.flip = False
            self.direction = 1
            for tile in col_tiles:
                if tile.collision_rect.x > self.collision_rect.x:
                    dx = 0


        # Salto
        if self.jumps < self.max_jumps and self.jump:  # self.in_air a False impide doble salto
            self.in_air == False
            self.vel_y = -11
            self.jump = False
            self.in_air = True
            self.jumps += 1

        # Aplicamos gravedad
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Actualizar la posición del jugador
        self.rect.x += dx
        self.rect.y += dy - 1

    def check_collision(self, tiles):
        col_tiles = []
        for tile in tiles:
            if self.collision_rect.colliderect(tile.collision_rect):
                col_tiles.append(tile)

        for tile in col_tiles:
            if tile.collision_rect.bottom > self.rect.y:  # Suelo
                self.vel_y = 0
                self.rect.bottom = tile.rect.top
                self.in_air = False
                self.jumps = 0
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
        # Actualizar la imagen del jugador
            
            
        

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
        if self.health < 0:
            self.health = 0
        self.notify_observers()

    # Registra el observador en la lista
    def register(self, observer):
        self.observers.append(observer)

    # Notifica a los observadores de los cambios
    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)


############
            

    def move_back(self, distance=20):
        # Mover hacia atrás
        self.rect.x -= distance  # Disminuir la coordenada x para mover hacia atrás

