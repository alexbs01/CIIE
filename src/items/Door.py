import os
import pygame
from settings import *

class Door(pygame.sprite.Sprite):

    def __init__(self, x, y, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.resource_manager = resource_manager
        self.action = 0
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

 # Tipos de animaciones
        animation_types = ['Closed', 'Opening', 'Closing']

        # Bucle que comprueba que animacion hacer
        for animation in animation_types:
            temp_list = []  # Reseteamos lista temporal

            # Contamos n de ficheros en la carpeta
            n_frames = len(os.listdir(f'assets/Door/{animation}'))
            for i in range(n_frames):
                img_path = f'assets/Door/{animation}/{i}.png'
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



    def draw(self, screen):

        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width // 4,
                        self.rect.centery - self.rect.height // 4, self.rect.width / 2,
                        self.rect.height)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

        screen.blit(self.image, self.rect)

    def update_animation(self):
        ANIMATION_COOLDOWN = 250

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


    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll
        self.update_animation()


    