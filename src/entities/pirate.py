from random import random

import pygame
import os
from settings import *
from Observer import Observer
from KeyboardControl import KeyboardControl

class Pirate(pygame.sprite.Sprite, Observer):
    def __init__(self, char_type, x, y, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = PLAYER_SPEED
        self.direction =  1
        self.flip = False
        self.jump = False
        self.max_jumps = PLAYER_MAX_JUMPS
        self.jumps = 0
        self.in_air = True
        self.vel_y =  0
        self.attack = False
        self.health =  PLAYER_HEALTH
        self.observers = []
        self.damage = PLAYER_DAMAGE
        self.points = 0
        self.scale = PLAYER_SCALE

        self.animation_list = []
        self.frame_index =  0
        self.action =  0
        self.update_time = pygame.time.get_ticks()
        self.resource_manager = resource_manager

        self.got_key = False
        self.got_sword = False
        
        self.control = KeyboardControl()

        animation_types = ['Idle', 'Run', 'Jump', 'Attack', 'Hit']

        for animation in animation_types:
            temp_list = []
            n_frames = len(os.listdir(f'assets/player/{animation}'))
            for i in range(n_frames):
                img_path = f'assets/player/{animation}/{i}.png'
                img = self.resource_manager.load_image(img_path, img_path)
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 4,
                                          self.rect.centery - self.rect.height / 2, self.rect.width / 2,
                                          self.rect.height)


    # Dibujar el pirata en la pantalla
    def draw(self, screen):

        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 4,
                                          self.rect.centery - self.rect.height / 2, self.rect.width / 2,
                                          self.rect.height)
        
        
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)  # 2 es el grosor del borde

    def move(self, obstacle_list, bg_scroll):

        screen_scroll = 0
        # Resetear variables de movimiento
        dx = 0
        dy = 0
        
        keys = pygame.key.get_pressed() 


        if self.control.left(keys):
            dx -= self.speed
            self.flip = True
            self.direction = -1


        if self.control.right(keys):
            dx += self.speed
            self.flip = False
            self.direction = 1


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

        # Comprobamos las colisiones del pirata
        dx,dy = self.check_collision(dx, dy, obstacle_list)

        # Mira que no pueda pasar mas alla de la pantalla
        if self.collision_rect.left + dx < 0 or self.collision_rect.right + dx > SCREEN_WIDTH:
            dx = 0
        

        # Actualizar la posición del jugador
        self.rect.x += dx
        self.rect.y += dy

        # Hace el scroll de la pantalla                                     # Tamaño del nivel en pixeles
        if self.rect.right > SCREEN_WIDTH - SCREEN_THRESH and bg_scroll < (150 * TILE_SIZE) - SCREEN_WIDTH:
            self.rect.x -= dx
            screen_scroll = -dx
        elif self.rect.left < SCREEN_THRESH and bg_scroll > abs(dx):
            self.rect.x -= dx
            screen_scroll = -dx
        else:
            screen_scroll = 0

        return screen_scroll


    def check_collision(self, dx, dy, obstacle_list):
        for tile in obstacle_list:
            if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width, self.collision_rect.height):
                dx = 0
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    self.jumps = 0
                    dy = tile[1].top - self.collision_rect.bottom
        return dx,dy

    def update(self, screen_scroll, obstacle_list, bg_scroll):
        self.screen_scroll = self.move(obstacle_list, bg_scroll)
        bg_scroll -= screen_scroll
        
        self.update_animation()

        self.rect.x += screen_scroll
        self.rect.x -= screen_scroll
        

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
    def update_action(self, new_action):
        # Comprueba si la acción actual es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
            # Actualizamos los nuevos valores
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    ############ PATRON OBSERVADOR

    def attack(self, enemy):
        # quiero que el ataque tenga un cooldown y que cada ataque haga un daño de 20
        if self.collision_rect.colliderect(enemy.collision_rect):
            enemy.get_Hit(self.damage + self.points)
            print(self.damage + self.points)
            print("Ataque")
            print(self.points)


    # Funcion de daño
    def get_Hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.notify_observers()
        print("Daño")


    # Registra el observador en la lista
    def register(self, observer):
        self.observers.append(observer)

    # Notifica a los observadores de los cambios
    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)

    def set_stats_dto(self, dto):
        if dto is not None:
            if dto.get_vida() > 0:
                self.health = dto.get_vida()
                self.points = dto.get_puntos() 
            else: # En caso de haber muerto
                self.vida = self.max_health
                self.puntos = 0

    def move_back(self, distance=20):
        # Mover hacia atrás
        self.rect.x -= distance  # Disminuir la coordenada x para mover hacia atrás
    
    # Creame un getter y setter del estado del pirata
    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health
    
    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def get_jumps(self):
        return self.max_jumps
    
    def set_jumps(self, jumps):
        self.max_jumps = jumps

        


