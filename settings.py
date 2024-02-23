import pygame

# Variables de entorno

TILE_WIDTH = 32
TILE_HEIGHT = 32

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

GRAVITY = 0.75

ROWS = 20 # Filas mapa 1
COLS = 150 # Columnas mapa 1

SCREEN_THRESH = 200 # Distancia a la que puede llegar el player antes de que la pantalla se mueva
TILE_SIZE = SCREEN_HEIGHT // ROWS


# define colours
BG = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
GREEN = (0, 255, 0)
LINE = (255,0,0)
BLACK = (0,0,0)
