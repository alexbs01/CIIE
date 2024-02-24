import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, display, position_x, position_y, tile):
        super().__init__()
        self.display = display
        self.image = pygame.image.load("assets/tiles/" + str(tile) + ".png")
        self.rect = self.image.get_rect()
        self.rect.centerx = position_x
        self.rect.centery = position_y
        
        # Ver las colisiones
        self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 2, self.rect.centery - self.rect.height / 2, self.rect.width, self.rect.height)

    def draw(self):
        # Dibujar la imagen del tile
        self.display.blit(self.image, self.rect)



        # Dibujar el rectángulo de colisión (en color rojo)
        pygame.draw.rect(self.display, (255, 0, 0), self.collision_rect, 2)  # 2 es el grosor del borde

    def update(self):
        self.draw()
