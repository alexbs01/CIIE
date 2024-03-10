import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
from escene.Escena import Escena
class Pause(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        SCREEN.fill(BLACK)
        title_font = pygame.font.Font("assets/inmortal.ttf", 100)
        pygame.display.update()
        clock.tick(15)
        

    def update(self, *args):
        return

    def events(self, *args):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    if event.key == pygame.K_a:
                        last_move_left = True
                    if event.key == pygame.K_d:
                        last_move_right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        last_move_left = False
                    if event.key == pygame.K_d:
                        last_move_right = False

    def draw(self):
        ui.draw_text('Pausa', title_font, WHITE, (SCREEN_WIDTH // 2) - 150, (SCREEN_HEIGHT // 2) - 100)

    def exit_program(self):
        pygame.quit()
        sys.exit()

    def return_game(self):
        self.director.exit_scene()