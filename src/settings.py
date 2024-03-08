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


# PLAYER
ATAQUE_COOLDOWN = 500
PLAYER_MAX_JUMPS = 1
PLAYER_DAMAGE = 20
PLAYER_HEALTH = 100
PLAYER_SCALE = 1
PLAYER_SPEED = 6

# ENEMIES
## CUCUMBER
CUCUMBER_DAMAGE = 15
CUCUMBER_SPEED = 1

## WHALE
WHALE_HEALTH = 200
WHALE_DAMAGE = 20
WHALE_SPEED = 1

## BAD PIRATE
BAD_PIRATE_HEALTH = 150
BAD_PIRATE_DAMAGE = 20
BAD_PIRATE_SPEED = 1

## CAPITAN
CAPITAN_HEALTH = 200
CAPITAN_DAMAGE = 20
CAPITAN_SPEED = 1

# COLLECTABLES
## HEALTH
PATH_ASSET_HEALTH = Path("assets/items/Health/0.png")
HEALTH_AMOUNT = 25
HEALTH_SCALE = 1

## KEY
PATH_ASSET_KEY = Path("assets/items/Keys/0.png")
KEY_SCALE = 0.25

## BERRIES
PATH_ASSET_BERRIES = Path("assets/items/gold/0.png")
POINTS_AMOUNT = 1
BERRIES_SCALE = 1.25

## BOOTS
PATH_ASSET_BOOTS = Path("assets/items/boots/0.png")
BOOTS_SCALE = 2.25

## SWORD
PATH_ASSET_SWORD = Path("assets/items/sword/0.png")
SWORD_SCALE = 1.5

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
