import pygame
from pathlib import Path

# Editor de niveles
PATH_ASSET_BACKGROUND = Path("assets/Background/dungeon.jpeg")
PATH_ASSETS_TILES = Path("assets/tiles")
PATH_ASSET_SAVE_BTN = Path("assets/save_btn.png")
PATH_ASSET_LOAD_BTN = Path("assets/menu/load_btn.png")
PATH_LEVEL = Path("levels")
PATH_LEVEL_1 = Path("levels/level1_data.csv")
PATH_LEVEL_2 = Path("levels/level2_data.csv")
PATH_LEVEL_3 = Path("levels/level3_data.csv")

PATH_BG_MENU = Path("assets/menu/2523.jpg")
PATH_PLAY_BOTTON = Path("assets/menu/Play Rect.png")
PATH_CONFIG_BOTTON = Path("assets/menu/Options Rect.png")
PATH_EXIT_BOTTON = Path("assets/menu/Quit Rect.png")


INITIAL_LEVEL = 1
MAX_LEVELS = 3
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
BACKGROUND_MUSIC_VOLUME = 0.05
EFFECTS_VOLUME = 0.1

ROWS = 20 # Filas mapa 1
COLS = 150 # Columnas mapa 1

SCREEN_THRESH = 200 # Distancia a la que puede llegar el player antes de que la pantalla se mueva
TILE_SIZE = SCREEN_HEIGHT // ROWS

MAX_POINTS = 100 # Máximo de berries que puede juntar

# define colours
BG = (82, 82, 82)
BG2 = (24,20,37)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
GREEN = (0, 255, 0)
LINE = (255,0,0)
BLACK = (0,0,0)
COLOR_TEXT_MENU = (182, 143, 64)
