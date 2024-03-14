import sys
import pygame
from pygame.locals import *
from settings import *
from escene.Escena import Escena
from world_generation.ResourceManager import ResourceManager
from escene.menu.GUI import GUI


class Pausa(Escena):

    def __init__(self, director):
        super().__init__(director)

        self.listaPantallas = []
        self.listaPantallas.append(GUI.PantallaPausa(self))
        self.mostrarPantallaInicial()


    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    def mostrarPantallaControles(self):
        self.listaPantallas.append(GUI.PantallaControles(self))
        self.pantallaActual += 1
  
    def returnPantalla(self):
            self.listaPantallas.pop()
            self.pantallaActual -= 1

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

            # Se pasa la lista de eventos a la pantalla actual
            self.listaPantallas[self.pantallaActual].eventos(events_list)


    def draw(self, pantalla):
        self.listaPantallas[self.pantallaActual].draw(pantalla)


    def salirPrograma(self):
        pygame.quit()
        sys.exit()

    def return_game(self):
        self.director.unpause_music()
        self.director.exit_scene()



