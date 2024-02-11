import pygame


# Clase pirata
class Pirate(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Imagenes/player/idle_right/1.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    # Dibujar el pirata en la pantalla
    def draw(self):
        from main import screen
        screen.blit(self.image, self.rect)
