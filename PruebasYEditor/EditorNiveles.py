import pygame
import csv

from button import Button

# Inicializar Pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 540
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# Crear la pantalla
screen = pygame.display.set_mode([SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN])
pygame.display.set_caption("Impel Down - Luffy's Adventure")

# Variables del juego
ROWS = 20
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

TILE_TYPES = 23

level = 1
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load images
dungeon_img = pygame.image.load('../assets/Background.png').convert_alpha()
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'../assets/tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('../assets/save_btn.png').convert_alpha()
load_img = pygame.image.load('../assets/menu/load_btn.png').convert_alpha()
# Definir colores
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# Definir fuente
font = pygame.font.SysFont('Futura', 30)

# crear lista de tiles vacía
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0


# funcion para escribir texto en la pantalla
def draw_text(text, font, text_col, x, y):  # x,y son las coordenadas de la esquina superior izquierda
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# funcion que dibuja el fondo
def draw_bg():
    screen.fill(GREEN)
    width = dungeon_img.get_width()
    for x in range(4):
        screen.blit(dungeon_img, ((x * width) - scroll, 0))


# funcion que dibuja  el mundo de tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


## Crear botones
save_button = Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(SCREEN_WIDTH + (50 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 5:
        button_row += 1
        button_col = 0

run = True


# dibujar grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0),
                         (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE),
                         (SCREEN_WIDTH, c * TILE_SIZE))


while run:

    clock.tick(FPS)
    # Dibujar el fondo
    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + 10)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + 40)

    # guardar y cargar datos
    if save_button.draw(screen):
        with open(f'../levels/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        with open(f'../levels/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # Elección de tiles
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # Seleccionar el tile actual
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll del fondo
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # añadir tiles a la pantalla del juego
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Capturar las teclas presionadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1

            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

    # Actualizar la pantalla
    pygame.display.update()

pygame.quit()
