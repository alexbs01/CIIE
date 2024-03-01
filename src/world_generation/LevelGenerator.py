import pygame
import world_generation.Tile
import csv
from settings import *

class LevelGenerator:
    def __init__(self, csv):
        self.csv = csv
        self.tiles = []
    
    def load_level(self):

        with open(self.csv, newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=',')

            for row in range(ROWS):
                r = [-1] * COLS
                self.tiles.append(r)

            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.tiles[x][y] = int(tile)
        return self.tiles

