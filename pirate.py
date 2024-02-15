import pygame
import os

# Variables de entorno
GRAVITY = 0.75

# Clase pirata
class Pirate(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.jump = False
        self.double_jump = True
        self.in_air = True # Para saber si el player ya ha saltado
        self.vel_y = 0 # Controla cuanto salta el player
        self.attack = False
        
        self.animation_list = [] #Lista de listas
        self.frame_index = 0
        self.action = 0 #Cada animacion trenda un int accion asociado
        self.update_time = pygame.time.get_ticks()

        # Tipos de animaciones
        animation_types = ['Idle','Run','Jump','Attack']

        # Bucle que comprueba que animacion hacer
        for animation in animation_types:
            temp_list = [] # Reseteamos lista temporal

            # Contamos n de ficheros en la carpeta
            n_frames = len(os.listdir(f'assets/player/{animation}'))
            for i in range(n_frames):
                img = pygame.image.load(f'assets/player/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list) # Guardamos en la lista de listas el contenido de la lista temporal

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 4 , self.rect.centery - self.rect.height / 2, self.rect.width / 2, self.rect.height)

    # Dibujar el pirata en la pantalla
    def draw(self):
        from main import screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)  # 2 es el grosor del borde

    def move(self, move_left, move_right):
        # Resetear variables de movimiento
        dx = 0
        dy = 0
        # Asignar movimiento izquierdo y derecho
        if move_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1

        if move_right:
            dx += self.speed
            self.flip = False
            self.direction = 1

        # Salto
        if self.jump == True and self.in_air == False: #self.in_air a False impide doble salto
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # Aplicamos gravedad
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Actualizar la posición del jugador
        self.rect.x += dx
        self.rect.y += dy


    
    def check_collision(self, tiles):
        col_tiles = pygame.sprite.spritecollide(self, tiles, False)
        for tile in col_tiles:
            if tile.rect.y > self.rect.y: # Suelo
                self.vel_y = 0
                self.rect.bottom = tile.rect.top
                self.in_air = False
                self.double_jump = True
                self.rect.y = self.rect.y
            if tile.rect.y < self.rect.y: # Techo
                self.vel_y = 0
                self.rect.top = tile.rect.bottom
                self.rect.y = self.rect.y

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

    # Actualiza la accion 
    def update_action(self, new_action, tiles):
        # Comprueba si la acción actual es diferente a la anterior
        self.check_collision(tiles)
        if new_action != self.action:
            self.action = new_action
            # Actualizamos los nuevos valores
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


