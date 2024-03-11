import os
import pygame
import random
from settings import *
from entities.Entities import Entity

class CucumberEnemy(Entity):
    def __init__(self, x, y, resource_manager):
        super().__init__(x, y, resource_manager, 'Cucumber')
        self.health = CUCUMBER_HEALTH
        self.damage = CUCUMBER_DAMAGE
        self.speed = CUCUMBER_SPEED
        self.attack_cooldown = CUCUMBER_ATTACK_COOLDOWN
        self.probability_to_hit = CUCUMBER_PROBABILITY_TO_HIT
        

    def move(self):
        if self.health > 0:
            self.rect.x += self.speed * self.direction
            self.step_count += abs(self.speed)  # Actualizar el contador de pasos

            # Verificar si el enemigo ha alcanzado el límite de pasos
            if self.step_count >= self.max_steps:
                # Cambiar la dirección del movimiento
                self.direction *= -1
                # Reiniciar el contador de pasos
                self.step_count = 0

            # Actualizar la animación según la dirección del movimiento
            if self.direction == 1:
                self.update_action(1)
            else:
                self.update_action(1)

class WhaleEnemy(Entity):
    def __init__(self, x, y, resource_manager):
        super().__init__(x, y, resource_manager, 'Whale', first_image_number=1)
        self.health = WHALE_HEALTH
        self.damage = WHALE_DAMAGE
        self.speed = WHALE_SPEED
        self.attack_cooldown = WHALE_ATTACK_COOLDOWN
        self.probability_to_hit = WHALE_PROBABILITY_TO_HIT

class badPirate(Entity):
    
    def __init__(self, x, y, resource_manager):
        super().__init__(x, y, resource_manager, 'Bad_Pirate', first_image_number=1)
        self.health = BAD_PIRATE_HEALTH
        self.damage = BAD_PIRATE_DAMAGE
        self.speed = BAD_PIRATE_SPEED
        self.direction = -1 # Tiene el sprite invertido entonces empieza con direccion -1
        self.attack_cooldown = BAD_PIRATE_ATTACK_COOLDOWN
        self.probability_to_hit = BAD_PIRATE_PROBABILITY_TO_HIT

    def draw(self, screen):
        return super().draw(screen, -1)

class Capitan(Entity):
    
    def __init__(self, x, y, resource_manager):
        super().__init__(x, y, resource_manager, 'Capitan', first_image_number=1)
        self.health = CAPITAN_HEALTH
        self.damage = CAPITAN_DAMAGE
        self.speed = CAPITAN_SPEED
        self.direction = -1
        self.attack_cooldown = CAPITAN_ATTACK_COOLDOWN
        self.probability_to_hit = CAPITAN_PROBABILITY_TO_HIT

    def draw(self, screen):
        return super().draw(screen, -1)

class Marine(Entity):
    def __init__(self, x, y, resource_manager):
        super().__init__(x, y, resource_manager, 'Marine', first_image_number=1, scale=MARINE_SCALE)
        self.health = MARINE_HEALTH
        self.damage = MARINE_DAMAGE
        self.speed = MARINE_SPEED
        self.direction = -1
        self.attack_cooldown = MARINE_ATTACK_COOLDOWN
        self.probability_to_hit = MARINE_PROBABILITY_TO_HIT
        self.scale = MARINE_SCALE

    def draw(self, screen):
        return super().draw(screen, -1)

class MarineBoss(Entity):
    def __init__(self, x, y, resource_manager):
        super().__init__(x, y, resource_manager, 'MarineBoss', first_image_number=0, scale=MARINE_BOSS_SCALE)
        self.health = MARINE_BOSS_HEALTH
        self.damage = MARINE_BOSS_DAMAGE 
        self.speed = MARINE_BOSS_SPEED
        self.direction = -1
        self.attack_cooldown = MARINE_BOSS_ATTACK_COOLDOWN
        self.probability_to_hit = MARINE_BOSS_PROBABILITY_TO_HIT
        self.scale = MARINE_BOSS_SCALE

    def draw(self, screen):
        return super().draw(screen, -1)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = resource_manager
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.last_contact_time = 0

        # Cargar imágenes de los spikes
        for i in range(4):  # Iterar desde  0 hasta  3
            img_path = f'assets/enemies/spikes/{i}.png'
            img = pygame.image.load(img_path)  # Cargar la imagen directamente
            if img is not None:
                self.animation_list.append(img)
            else:
                print(f"No se pudo cargar la imagen: {img_path}")

        # Asegurarse de que la imagen se ha cargado correctamente
        if self.animation_list:
            self.image = self.animation_list[self.frame_index]
            self.rect = self.image.get_rect()
        else:
            self.image = None
            self.rect = pygame.Rect(x, y, 0, 0)

        self.rect.x = x
        self.rect.y = y
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.observers = []

    def draw(self, screen):
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 2,
                                            self.rect.centery - self.rect.height / 2, self.rect.width,
                                            self.rect.height)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)
        screen.blit(self.image, self.rect)

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll
        self.update_animation()

    def update_animation(self):
        ANIMATION_SPEED = 100  # Velocidad de cambio de imagen en milisegundos
        # Actualizar la animación
        if pygame.time.get_ticks() - self.update_time > ANIMATION_SPEED:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
            self.image = self.animation_list[self.frame_index]