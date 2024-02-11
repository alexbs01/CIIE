import pygame


# Clase pirata
class Pirate(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        
        self.animation_list = [] #Lista de listas
        self.frame_index = 0
        self.action = 0 #Cada animacion es una accion
        self.update_time = pygame.time.get_ticks()

        temp_list = [] # Lista temporal
        # Carga la animacion idle_right
        for i in range(1,6):
            img = pygame.image.load(f'Imagenes/player/idle_right/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list) # Guardamos en la lista de listas el contenido de la lista temporal

        temp_list = []
        # Carga la animacion run_right
        for i in range(1,7):
            img = pygame.image.load(f'Imagenes/player/run_right/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)


        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    # Dibujar el pirata en la pantalla
    def draw(self):
        from main import screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

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

        # Actualizar la posición del jugador
        self.rect.x += dx
        self.rect.y += dy

    # Actualizar la animación
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
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
    def update_action(self, new_action):
        # Comprueba si la acción actual es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
            # Actualizamos los nuevos valores
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

