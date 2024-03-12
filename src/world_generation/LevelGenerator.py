import pygame
from settings import *
from pathlib import Path

class LevelGenerator:
    def __init__(self, level_num, resource_manager):
        self.csv_path = f"levels/level{level_num}_data.csv"
        self.resource_manager = resource_manager
        self.tiles = []

    def load_level(self):
        try:
            csv_data = self.resource_manager.load_resource(f"level{level_num}_data", self.csv_path, "csv")
            for row in range(ROWS):
                r = [-1] * COLS
                self.tiles.append(r)

            for x, row in enumerate(csv_data):
                for y, tile in enumerate(row):
                    self.tiles[x][y] = int(tile)
            return self.tiles
        except Exception as e:
            print(f"Error al cargar el nivel: {e}")
            return None
