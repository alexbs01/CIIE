import pygame
from settings import *

# Cargar imagenes
health_box_img = pygame.image.load('assets/items/Health/0.png')
key_box_img = pygame.image.load('assets/items/Keys/0.png')
berries_box_img = pygame.image.load('assets/items/gold/0.png')

item_boxes = {
    'Health': health_box_img,
    'Key': key_box_img,
    'Berries': berries_box_img
}

class Collectables(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, scale, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE //  2, y + (TILE_SIZE - self.image.get_height()))
        self.player = player

    def update(self):
        # Confirmar que el pirata coge el item
        if pygame.sprite.collide_rect(self, self.player):
            if self.item_type == 'Health':
                if self.player.health <  100:
                    self.player.health +=  25
                    if self.player.health >  100:
                        self.player.health = 100
            elif self.item_type == 'Key':
                print('Has cogido una llave')
            elif self.item_type == 'Berries':
                print('Has cogido una moneda')
                if self.player.health <  100:
                    self.player.health +=  5
                    if self.player.health >  100:
                        self.player.health = 100

            self.kill()