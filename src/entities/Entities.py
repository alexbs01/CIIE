import pygame
import os
import random
from entities.observer.Subject import Subject
# Clase para los enemigos del juego 
class Entity(pygame.sprite.Sprite, Subject):
    def __init__(self, x, y, resource_manager, enemy, first_image_number=0, scale=1): # Cucumber
        pygame.sprite.Sprite.__init__(self)
        Subject.__init__(self)
        self.original_x = x
        self.original_y = y
        self.step_count = 0
        self.max_steps = random.randint(60, 120)
        self.speed = 1
        self.resource_manager = resource_manager
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.last_attack_time = 0
        self.attack_cooldown = 2000
        self.attack_animation_cooldown = 100
        self.probability_to_hit = 5
        self.scale = scale
        self.orientacion = self.get_direction()

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
                img = self.resource_manager.load_resource(f'{enemy}_{animation}_{i}', img_path, "image")  # Corrección aquí
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
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
            self.collision_rect.x += self.speed * self.orientacion
            self.rect.x += self.speed * self.orientacion
            self.step_count += abs(self.speed)  # Actualizar el contador de pasos

            # Verificar si el enemigo ha alcanzado el límite de pasos
            if self.step_count >= self.max_steps:
                # Cambiar la dirección del movimiento
                self.orientacion *= -1
                # Reiniciar el contador de pasos
                self.step_count = 0


            self.update_action(1)


    
    def ai(self, pirate):
        if self.health > 0:
            # Si el enemigo esta colisionando con el pirata, atacar
            if self.collision_rect.colliderect(pirate.collision_rect):
                self.attack(pirate, self.damage)
            # Si el enemigo no esta cerca del pirata, moverse
            else:
                self.move()


    def get_Hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            # Quiero que el sprite del enemigo desaparezca
            self.update_action(4)

    
    def attack(self, pirate, damage):
        # Ataque aleatorio basado en el tiempo
        if random.randint(0,
                            100) < self.probability_to_hit and pygame.time.get_ticks() - self.last_attack_time > self.attack_cooldown:  # 5% de probabilidad de atacar y cada  2 segundos
            if self.collision_rect.colliderect(pirate.collision_rect):
                pirate.get_Hit(damage)
                self.last_attack_time = pygame.time.get_ticks()
                self.update_action(2)
    
    def update_animation(self):
        animation_cooldown = 60
        if self.action == 2:  # Si la acción es de ataque reducimos cooldown entre frames
            animation_cooldown = self.attack_animation_cooldown
        if self.action == 4:  # Si la acción es de muerte, no se mueve
            animation_cooldown = 500
        # Actualizar imagen de la animación dependiendo del frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Actualizar la animación
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
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
                                            self.rect.centery - self.rect.height // 4,
                                            self.rect.width / 2,
                                            self.rect.height)
        #pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2) 

        
        if self.orientacion != self.get_direction():
            screen.blit(self.image, self.rect)
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)


    def set_health(self, health):
        self.health = health
        self.notify_observers(self.health)
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll
        self.update_animation()

    def get_direction(self, direction):
        pass