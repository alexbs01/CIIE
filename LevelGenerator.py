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