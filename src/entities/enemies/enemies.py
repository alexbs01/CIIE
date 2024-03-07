import os
import pygame
import random
from settings import SCREEN_WIDTH
from entities.Entities import Entity

class CucumberEnemy(Entity):
    def __init__(self, x, y, speed, resource_manager):
        super().__init__(x, y, speed, resource_manager, 'Cucumber')
        self.damage = 15

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

    def draw(self, screen):

        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width // 4,
                                            self.rect.centery - self.rect.height // 4, self.rect.width / 2,
                                            self.rect.height)
        #pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2) 
        #print('pintar')

        if self.direction == 1:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll
        self.update_animation()
        # self.check_alive()

    def get_Hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            # Quiero que el sprite del enemigo desaparezca
            self.update_action(4)
        self.notify_observers()
        self.move_back()
        print(self.health)

    def move_back(self, distance=20):
        if self.health > 0:
            self.rect.x += (self.direction * distance)
            self.direction *= -1

    def kill(self):  # Mirar como quitarlo de verdad, aqui solo lo escondo
        self.rect.x = SCREEN_WIDTH + 100
        self.rect.y = SCREEN_WIDTH + 100

    def update_health(self, health):
        self.health = health

    def register(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)

class WhaleEnemy(Entity):
    def __init__(self, x, y, speed, resource_manager):
        super().__init__(x, y, speed, resource_manager, 'Whale', first_image_number=1)
        self.health = 20
        self.damage = 15

    def draw(self, screen):

        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width // 4,
                                            self.rect.centery - self.rect.height // 4, self.rect.width / 2,
                                            self.rect.height)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

        if self.direction == 1:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll
        self.update_animation()
        
        # self.check_alive()

    def get_Hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            # Quiero que el sprite del enemigo desaparezca
            self.update_action(4)
        self.notify_observers()
        self.move_back()
        print(self.health)

    def move_back(self, distance=20):
        if self.health > 0:
            self.rect.x += (self.direction * distance)
            self.direction *= -1

    def kill(self):  # Mirar cómo quitarlo de verdad, aquí solo lo escondo
        self.rect.x = SCREEN_WIDTH + 100
        self.rect.y = SCREEN_WIDTH + 100

    def update_health(self, health):
        self.health = health

    def register(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)

class badPirate(Entity):
    
    def __init__(self, x, y, speed, resource_manager):
        super().__init__(x, y, speed, resource_manager, 'Bad_Pirate', first_image_number=1)
        self.health = 150
        self.damage = 20
        self.direction = -1 # Tiene el sprite invertido entonces empieza con direccion -1

    def draw(self, screen):

        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width // 4,
                                            self.rect.centery - self.rect.height // 4, self.rect.width / 2,
                                            self.rect.height)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

        if self.direction == -1:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll
        self.update_animation()
        

    def get_Hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            # Quiero que el sprite del enemigo desaparezca
            self.update_action(4)
        self.notify_observers()
        self.move_back()
        print(self.health)

    def move_back(self, distance=20):
        if self.health > 0:
            self.rect.x += (self.direction * distance)
            self.direction *= -1

    def kill(self):  # Mirar cómo quitarlo de verdad, aquí solo lo escondo
        self.rect.x = SCREEN_WIDTH + 100
        self.rect.y = SCREEN_WIDTH + 100

    def update_health(self, health):
        self.health = health

    def register(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)

class Capitan(Entity):
    
    def __init__(self, x, y, speed, resource_manager):
        super().__init__(x, y, speed, resource_manager, 'Capitan', first_image_number=1)
        self.health = 200
        self.damage = 20
        self.direction = -1 # Tiene el sprite invertido entonces empieza con direccion -1

    def draw(self, screen):

        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width // 4,
                                            self.rect.centery - self.rect.height // 4, self.rect.width / 2,
                                            self.rect.height)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

        if self.direction == -1:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll
        self.update_animation()
        

    def get_Hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            # Quiero que el sprite del enemigo desaparezca
            self.update_action(4)
        self.notify_observers()
        self.move_back()
        print(self.health)

    def move_back(self, distance=20):
        if self.health > 0:
            self.rect.x += (self.direction * distance)
            self.direction *= -1

    def kill(self):  # Mirar cómo quitarlo de verdad, aquí solo lo escondo
        self.rect.x = SCREEN_WIDTH + 100
        self.rect.y = SCREEN_WIDTH + 100

    def update_health(self, health):
        self.health = health

    def register(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = resource_manager
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

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