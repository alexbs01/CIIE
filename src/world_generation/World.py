import pygame
from settings import *
from world_generation.ResourceManager import ResourceManager

class World():

    def __init__(self, resource_manager):
        self.obstacle_list = []
        self.resource_manager = resource_manager

    def process_data(self, data):

        self.level_length = len(data[0])

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.resource_manager.load_image("assets/tiles/" + str(tile) + ".png", "assets/tiles/" + str(tile) + ".png")
                    rect = img.get_rect()
                    rect.x = x * TILE_SIZE
                    rect.y = y * TILE_SIZE

                    tile_data = (img, rect) 
                    # Guardamos en una lista los tiles que vayan a ser obstaculos
                    if tile >= 0 and tile <= 9 or tile >= 22 and tile <= 23: #las imagenes 0-8 y 21-23
                        self.obstacle_list.append(tile_data)

        return self.obstacle_list

    def draw(self,screen, screen_scroll):
        for tile in self.obstacle_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])   
    

