import sys
import pygame

from world_generation.ResourceManager import ResourceManager
from escene.Escena import Escena
from pygame.locals import *
from settings import *

class Pausa(Escena):

    def __init__(self, director):
        Escena.__init__(self, director)

        self.title_font = pygame.font.Font("assets/inmortal.ttf", 100)
        self.title = self.title_font.render('PAUSA', True, (237, 82, 47))
        self.title_rect = self.title.get_rect()

    def update(self, *args):
        return

    def events(self, events_list):
        for event in events_list:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_p:
                    self.return_game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self, screen):
        
        screen.fill(BLACK)
        self.title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        screen.blit(self.title, self.title_rect)

    def exit_program(self):
        pygame.quit()
        sys.exit()

    def return_game(self):
        self.director.exit_scene()