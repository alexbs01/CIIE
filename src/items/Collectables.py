import pygame
from settings import *

# Load images
health_box_img = pygame.image.load(PATH_ASSET_HEALTH)
key_box_img = pygame.image.load(PATH_ASSET_KEY)
berries_box_img = pygame.image.load(PATH_ASSET_BERRIES)
boots_box_img = pygame.image.load(PATH_ASSET_BOOTS)
sword_box_img = pygame.image.load(PATH_ASSET_SWORD)

item_boxes = {
    'Health': health_box_img,
    'Key': key_box_img,
    'Berries': berries_box_img,
    'Boots': boots_box_img,
    'Sword': sword_box_img
}

item_scales = {
    'Health': HEALTH_SCALE,
    'Key': KEY_SCALE,
    'Berries': BERRIES_SCALE,
    'Boots': BOOTS_SCALE,
    'Sword': SWORD_SCALE
}

class Collectables(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.scale = item_scales[self.item_type]
        self.image = item_boxes[self.item_type]
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE //  2, y + (TILE_SIZE - self.image.get_height()))
        self.player = player

    def update(self,screen_scroll):
        self.rect.x += screen_scroll
        # Confirmar que el pirata coge el item

        
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        