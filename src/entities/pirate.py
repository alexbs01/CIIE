from random import random

import pygame
import os
from settings import *
from entities.observer.Subject import Subject
from controls.KeyboardControl import KeyboardControl

class Pirate(pygame.sprite.Sprite, Subject):
    def __init__(self, char_type, x, y, resource_manager):

        pygame.sprite.Sprite.__init__(self)
        Subject.__init__(self)
        self.char_type = char_type # Variable para indicar el nombre de la entidad
        self.speed = PLAYER_SPEED # Variable que designa la velocidad del jugador
        self.direction = 1 # Variable que indica en que direccion está mirando 1 der, -1 izq
        self.flip = False # Variable para hacer flip al sprite
        self.jump = False # Variable que indica si está saltando
        self.max_jumps = PLAYER_MAX_JUMPS # Variable que usaremos para el doble salto
        self.jumps = 0 # Variable que usaremos para el doble salto
        self.in_air = True # Variable que comprueba si el judador está en el aire
        self.vel_y = 0 # Variable para controlar la velocidad en el eje y
        self.attack = False # Variable para comprobar si el jugador está atacando
        self.health = PLAYER_HEALTH # Salud del jugador
        self.observers = [] # Observadores del jugador
        self.damage = PLAYER_DAMAGE # Daño base que hace el jugador al atacar
        self.points = 0 # Puntos que tiene el jugador
        self.scale = PLAYER_SCALE # Escala del sprite
        self.last_attack_time = 0 # Variable para comprobar cuando fue la ultima vez que atacó, cooldown

        self.move_left = False # Variable para mov a la izq
        self.move_right = False # Variable para mov a la der

        self.animation_list = [] # Lista de listas con las animaciones posibles
        self.frame_index = 0 # Controlara que frames enseñar
        self.action = 0 # Controla que accion está ejecutando el jugador
        self.update_time = pygame.time.get_ticks() # Nos ayudara en la fluidez de la animacion
        self.resource_manager = resource_manager # Resource manager

        self.got_key = False # Controla si se tiene la llave
        self.got_sword = False # Controla si se tiene la espada
        self.got_boots = False # Controla si se tienen las botas

        self.control = KeyboardControl() # Se usó para pruebas

        animation_types = ['Idle', 'Run', 'Jump', 'Attack', 'Hit'] # Tipos de animacion
        
        for animation in animation_types:
            temp_list = [] # Creamos una lista temporal
            n_frames = len(os.listdir(f'assets/player/{animation}')) # Guarda cuantos frames tiene cada animacion
            for i in range(n_frames):
                img_path = f'assets/player/{animation}/{i}.png'
                img = self.resource_manager.load_resource(img_path, img_path, "image")
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                temp_list.append(img) # Vamos guardando en la lista cada imagen de la animacion
            self.animation_list.append(temp_list) # Guardamos en la lista de animaciones las listas de cada animacion

        self.image = self.animation_list[self.action][self.frame_index] #Carga la imagen en funcion de la accion y el indice
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 4,
                                          self.rect.centery - self.rect.height / 2, self.rect.width / 2,
                                          self.rect.height) # Hitbox personalizada


    # Dibujar el pirata en la pantalla
    def draw(self, screen):

        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
        # Se va actualizando la hitbox
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 4,
                                          self.rect.centery - self.rect.height / 2, self.rect.width / 2,
                                          self.rect.height)
        
        

    def update(self, screen_scroll, bg_scroll):
        bg_scroll -= screen_scroll
        
        self.update_animation()

        self.rect.x += screen_scroll
        self.rect.x -= screen_scroll
        

    # Actualizar la animación
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        animation_cooldown = 100

        if self.action == 3:  # Si la acción es de ataque reducimos cooldown entre frames
            animation_cooldown = 15
            self.last_attack_time = current_time

        # Actualizar imagen de la animación dependiendo del frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Actualizar la animación
        if current_time - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Si la animación ha terminado, reiniciar
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            if self.action == 3:
                self.action = 0
                self.attack = False

        # Actualizar la imagen del jugador
        


    # Actualiza la accion 
    def update_action(self, new_action):
        # Comprueba si la acción actual es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
            # Actualizamos los nuevos valores
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    
    # Funcion de daño al jugador
    def get_Hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.set_health(self.health)


    # Funcion de ataque que al final solo se uso en prácticas
    def attack(self, enemy):
        # quiero que el ataque tenga un cooldown y que cada ataque haga un daño de 20
        if self.collision_rect.colliderect(enemy.collision_rect):
            enemy.get_Hit(self.damage + self.points)
            print(self.damage + self.points)
            print("Ataque")
            print(self.points)

    # Funcion para cargar los datos del jugador al iniciarlo en cada nivel
    def set_stats_dto(self, dto):
        if dto is not None:
            if dto.get_vida() > 0:
                self.health = dto.get_vida()
                self.points = dto.get_puntos()
                self.max_jumps = dto.get_jumps() 
                self.got_sword = dto.get_sword()
                self.got_boots = dto.get_boots()
            else: # En caso de haber muerto
                self.vida = self.max_health
                self.puntos = 0
                self.max_jumps = dto.get_jumps() 
                self.got_sword = dto.get_sword()
                self.got_boots = dto.get_boots()


    # Funcion que movia hacia atras el personaje, usada en prácticas solo
    def move_back(self, distance=20):
        # Mover hacia atrás
        self.rect.x -= distance  # Disminuir la coordenada x para mover hacia atrás
    
    # Getters y setters
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

        


