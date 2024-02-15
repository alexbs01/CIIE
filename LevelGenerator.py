import pygame
import Tile
import csv

class LevelGenerator:
    def __init__(self, csv):
        self.csv = csv
        self.tiles = []
        self.load_level()
    
    def load_level(self):
        with open(self.csv, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.tiles.append(row)
        print(self.tiles)
        return self.tiles

    def create_level(self):
        from main import screen
        from Tile import Tile
        initial_x = 0
        initial_y = 0
        tiles = []
        for row in self.tiles:
            for tile in row:
                if tile != "-1":
                    tiles.append(Tile(screen, initial_x, initial_y, tile))
                initial_x += 32
            initial_y += 32
            initial_x = 0
        return tiles