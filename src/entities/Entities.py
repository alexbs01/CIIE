import pygame
import os

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, resource_manager, enemy, first_image_number=0): # Cucumber
        pygame.sprite.Sprite.__init__(self)
        self.original_x = x
        self.original_y = y
        self.step_count = 0
        self.max_steps = 120
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
            n_frames = len(os.listdir(f'assets/enemies/{enemy}/{animation}'))
            for i in range(first_image_number, n_frames):
                img_path = f'assets/enemies/{enemy}/{animation}/{i}.png'
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