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
        img = pygame.image.load('Imagenes/player/idle_right/1.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
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
