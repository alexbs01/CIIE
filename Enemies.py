import os

import pygame

from settings import SCREEN_WIDTH


class CucumberEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction =   1
        self.resource_manager = resource_manager
        self.animation_list = []
        self.frame_index =   0
        self.action =   0
        self.update_time = pygame.time.get_ticks()

        # Tipos de animaciones
        animation_types = ['Idle', 'Run', 'Attack']

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
            self.rect = pygame.Rect(x, y,   0,   0)

        self.rect.x = x
        self.rect.y = y
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    # Resto de los métodos de la clase CucumberEnemy...

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <  0 or self.rect.x + self.rect.width > SCREEN_WIDTH:
            self.direction *= -1

    def attack(self, pirate):
        if self.collision_rect.colliderect(pirate.collision_rect):
            pirate.get_Hit(10)  # Asume que el daño es  10

    def update_animation(self):
        ANIMATION_COOLDOWN =  100
        if self.action ==  2:  # Si la acción es de ataque reducimos cooldown entre frames
            ANIMATION_COOLDOWN =  10

        # Actualizar imagen de la animación dependiendo del frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Actualizar la animación
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=  1
        # Si la animación ha terminado, reiniciar
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index =  0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255,  0,  0), self.collision_rect,  2)
