import os
import pygame
import random
from settings import SCREEN_WIDTH


class Enemy:
    class CucumberEnemy(pygame.sprite.Sprite):
        def __init__(self, x, y, speed, resource_manager):
            pygame.sprite.Sprite.__init__(self)
            self.move_direction = 1
            self.original_x = x
            self.original_y = y
            self.observers = []
            self.health = 100
            self.speed = speed
            self.direction = 1
            self.resource_manager = resource_manager
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()
            self.last_attack_time = 0

            self.move_distance = 20  # Número de píxeles para moverse aleatoriamente
            self.random_move_speed = 0.5  # Velocidad de movimiento aleatorio más lenta

            # Tipos de animaciones
            animation_types = ['Idle', 'Run', 'Attack', 'Hit', 'DeathGround']

            # Bucle que comprueba que animacion hacer
            for animation in animation_types:
                temp_list = []  # Reseteamos lista temporal

                # Contamos n de ficheros en la carpeta
                n_frames = len(os.listdir(f'assets/enemies/Cucumber/{animation}'))
                for i in range(n_frames):
                    img_path = f'assets/enemies/Cucumber/{animation}/{i}.png'
                    img = self.resource_manager.load_image(img_path, img_path)
                    if img is not None:  # Asegurarse de que la imagen se ha cargado correctamente
                        temp_list.append(img)
                    else:
                        print(f"No se pudo cargar la imagen: {img_path}")
                self.animation_list.append(temp_list)

            # Asegurarse de que la imagen se ha cargado correctamente
            if self.animation_list[self.action]:
                self.image = self.animation_list[self.action][self.frame_index]
                self.rect = self.image.get_rect()
            else:
                self.image = None
                self.rect = pygame.Rect(x, y, 0, 0)

            self.rect.x = x
            self.rect.y = y
            self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        def move(self):
            if self.health > 0:
                if random.randint(0, 100) < 10:
                    self.move_direction *= -1
                self.rect.x += self.move_direction * self.speed
                # Actualizar la animación que se gire a la izquierda o derecha
                if self.move_direction == 1:
                    self.update_action(1)
                else:
                    self.update_action(1)

        def attack(self, pirate):
            # Ataque aleatorio basado en el tiempo
            if random.randint(0,
                              100) < 5 and pygame.time.get_ticks() - self.last_attack_time > 2000:  # 5% de probabilidad de atacar y cada  2 segundos
                if self.collision_rect.colliderect(pirate.collision_rect):
                    pirate.get_Hit(15)  # Ahora el daño es  15
                    self.last_attack_time = pygame.time.get_ticks()
                    self.update_action(2)

        # quiero hacer una ia que mueva al enemigo 10 pixeles a la derecha y 10 a la izquierda, y establecer un ranngo de observacion de 100

        def ai(self, pirate):
            if self.health > 0:
                # Si el enemigo esta cerca del pirata, atacar
                if self.collision_rect.colliderect(pirate.collision_rect):
                    self.attack(pirate)
                else:
                    self.move()

        def update_animation(self):
            ANIMATION_COOLDOWN = 60
            if self.action == 2:  # Si la acción es de ataque reducimos cooldown entre frames
                ANIMATION_COOLDOWN = 10
            if self.action == 4:  # Si la acción es de muerte, no se mueve
                ANIMATION_COOLDOWN = 500
            # Actualizar imagen de la animación dependiendo del frame
            self.image = self.animation_list[self.action][self.frame_index]
            # Actualizar la animación
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            # Si la animación ha terminado, reiniciar
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

        def update_action(self, new_action):
            # Comprueba si la acción actual es diferente a la anterior
            if new_action != self.action:
                self.action = new_action
                # Actualizamos los nuevos valores
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def draw(self, screen):

            self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width // 4,
                                              self.rect.centery - self.rect.height // 4, self.rect.width / 2,
                                              self.rect.height)
            pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

            if self.move_direction == 1:
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


