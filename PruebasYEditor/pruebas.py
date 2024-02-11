import pygame

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 540
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# Crear la pantalla
screen = pygame.display.set_mode([SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN])
pygame.display.set_caption("Impel Down - Luffy's Adventure")

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Cargar el fondo y el jugador
background = pygame.image.load('./Imagenes/Background/background.jpg').convert()
player_sheet = pygame.image.load('./Imagenes/LuffySheet.png').convert()
player_sheet.set_colorkey((255, 255, 255))

# Definir las dimensiones de cada frame del jugador
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 55

# Definir la posición inicial del jugador
player_static_x = 10
player_static_y = 300

# Definir las animaciones del jugador
# Estos números representan los índices de los frames en la hoja de sprites
player_frames_idle = [0, 1, 2]  # Frames para la animación de estar quieto
player_frames_walk_right = [3, 4, 5]  # Frames para la animación de caminar hacia la derecha
player_frames_walk_left = [6, 7, 8]  # Frames para la animación de caminar hacia la izquierda
current_frame = 0
animation_speed = 0.15  # Velocidad de la animación

# Velocidad de movimiento del jugador
player_speed = 1.5

# Dirección inicial del jugador
player_direction = "left"

# Bucle principal del juego
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Capturar las teclas presionadas
    keys = pygame.key.get_pressed()

    # Actualizar la posición del jugador según las teclas presionadas
    if keys[pygame.K_LEFT]:
        player_static_x -= player_speed
        player_direction = "right"
    elif keys[pygame.K_RIGHT]:
        player_static_y += player_speed
        player_direction = "left"

    # Actualizar la animación del jugador
    if player_direction == "right":
        current_frame = (current_frame + animation_speed) % len(player_frames_walk_right)
        player_frames = player_frames_walk_right
    else:
        current_frame = (current_frame + animation_speed) % len(player_frames_walk_left)
        player_frames = player_frames_walk_left

    # Limpiar la pantalla
    screen.blit(background, [0, 0])

    # Renderizar el jugador en la pantalla
    player_frame = player_frames[int(current_frame)]
    player_clip = pygame.Rect(player_frame * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)  # Crear una superficie transparente
    player_image.blit(player_sheet, (0, 0), player_clip)  # Copiar el frame del jugador a la superficie transparente
    player_image = pygame.transform.flip(player_image, True, False) if player_direction == "left" else player_image
    screen.blit(player_image, (player_static_x, player_static_y))


    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(60)  # Se aumenta la velocidad de fotogramas para hacer el movimiento más fluido

# Salir de Pygame
pygame.quit()
