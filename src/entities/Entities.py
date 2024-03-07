import pygame
import os
import random

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, resource_manager, enemy, first_image_number=0): # Cucumber
        pygame.sprite.Sprite.__init__(self)
        self.original_x = x
        self.original_y = y
        self.step_count = 0
        self.max_steps = 120
        self.observers = []
        self.health = 100
        self.damage = 10
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
            self.collision_rect.x += self.speed * self.direction
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

    def move_back(self, distance=20):
        if self.health > 0:
            self.rect.x += (self.direction * distance)
            self.direction *= -1
    
    def ai(self, pirate):
        if self.health > 0:
            # Si el enemigo esta colisionando con el pirata, atacar
            if self.collision_rect.colliderect(pirate.collision_rect):
                self.attack(pirate, self.damage)
            # Si el enemigo no esta cerca del pirata, moverse
            else:
                self.move()

    def notify_observers(self):
        for observer in self.observers:
            observer.update_health(self.health)

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
    
    def attack(self, pirate, damage):
        # Ataque aleatorio basado en el tiempo
        if random.randint(0,
                            100) < 5 and pygame.time.get_ticks() - self.last_attack_time > 2000:  # 5% de probabilidad de atacar y cada  2 segundos
            if self.collision_rect.colliderect(pirate.collision_rect):
                pirate.get_Hit(damage)
                self.last_attack_time = pygame.time.get_ticks()
                self.update_action(2)
    
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
    
    def draw(self, screen, direction=1):
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width // 4,
                                            self.rect.centery - self.rect.height // 4,
                                            self.rect.width / 2,
                                            self.rect.height)
        #pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2) 

        if self.direction == direction:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update_health(self, health):
        self.health = health
        
    def register(self, observer):
        self.observers.append(observer)
