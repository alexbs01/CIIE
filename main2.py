import pygame
import button

# Inicializar Pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# Crear la pantalla
screen = pygame.display.set_mode([SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN])
pygame.display.set_caption("Impel Down - Luffy's Adventure")

# Variables del juego
ROWS = 20
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS

TILE_TYPES = 21

current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load images
dungeon_img = pygame.image.load('Imagenes/Background/dungeon3.png').convert_alpha()
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Imagenes/tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Definir colores
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)


# funcion que dibuja el fondo
def draw_bg():
    screen.fill(GREEN)
    width = dungeon_img.get_width()
    for x in range(4):
        screen.blit(dungeon_img, ((x * width) - scroll, 0))


## Crear botones
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
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

    # Dibujar tiles panel
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
    if scroll_right:
        scroll += 5 * scroll_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Capturar las teclas presionadas
        if event.type == pygame.KEYDOWN:
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
