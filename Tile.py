import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, display, position_x, position_y):
        self.display = display
        self.imagen = pygame.image.load("Imagenes/tiles/0.png")
        self.rect = self.imagen.get_rect()
        self.rect.centerx = position_x +1
        self.rect.centery = position_y

    def draw(self):
        self.display.blit(self.imagen, self.rect)

    def update(self):
        self.draw()