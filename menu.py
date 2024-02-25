import pygame
import sys
from button import Button
import settings

pygame.init()

# Cambio de nombre para mejorar la claridad
SCREEN_SIZE = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Menu")

BACKGROUND_IMAGE = pygame.image.load("assets/2523.jpg")
game_started = False


def get_font(size):  # Devuelve la fuente Press-Start-2P en el tamaño deseado
    return pygame.font.Font("assets/inmortal.ttf", size)


def main_menu():
    global game_started
    while True:
        SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

        MOUSE_POSITION = pygame.mouse.get_pos()

        MENU_TITLE_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_TITLE_RECT = MENU_TITLE_TEXT.get_rect(center=(400, 50))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), position=(400, 250),
                             text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), position=(400, 400),
                                text_input="OPTIONS", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), position=(400, 550),
                             text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TITLE_TEXT, MENU_TITLE_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.change_color(MOUSE_POSITION)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MOUSE_POSITION):
                    game_started = True  # Indica que se debe iniciar el juego
                    break  # Sal del bucle del menú
                # El resto del código para manejar otros botones...

        if game_started:
            break  # Sal del bucle del menú si se debe iniciar el juego

        pygame.display.update()


main_menu()