import pygame
from pathlib import Path

# Editor de niveles
PATH_ASSET_BACKGROUND = Path("assets/Background.png")
PATH_ASSETS_TILES = Path("assets/tiles")
PATH_ASSET_SAVE_BTN = Path("assets/save_btn.png")
PATH_ASSET_LOAD_BTN = Path("assets/menu/load_btn.png")
PATH_LEVEL = Path("levels")

# Variables de entorno
TILE_WIDTH = 32
TILE_HEIGHT = 32

ATAQUE = 20
ATAQUE_COOLDOWN = 500


# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

GRAVITY = 0.75
FPS = 60

# AUDIO
BACKGROUND_MUSIC_VOLUME = 0.15

ROWS = 20 # Filas mapa 1
COLS = 150 # Columnas mapa 1

SCREEN_THRESH = 200 # Distancia a la que puede llegar el player antes de que la pantalla se mueva
TILE_SIZE = SCREEN_HEIGHT // ROWS


# define colours
BG = (82, 82, 82)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
GREEN = (0, 255, 0)
LINE = (255,0,0)
BLACK = (0,0,0)