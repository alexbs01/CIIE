import pygame
from Escena import Escena
from GUI import GUI
from world_generation.ResourceManager import ResourceManager
from settings import *

class Menu2(Escena):

    def __init__(self, director):

        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director)

        # Creamos la lista de pantallas
        self.listaPantallas = []

        # Creamos las pantallas que vamos a tener
        # y las metemos en la lista
        self.listaPantallas.append(GUI.PantallaInicial(self))

        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()


    def update(self, *args):
        return
    
    def events(self, lista_eventos):

        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
        # Si se quiere salir, se le indica al director
        
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.quit_program()

            # Se pasa la lista de eventos a la pantalla actual
            self.listaPantallas[self.pantallaActual].eventos(lista_eventos)


    def draw(self, pantalla):
        self.listaPantallas[self.pantallaActual].draw(pantalla)
        
    #--------------------------------------
    # Metodos propios del menu

    # Boton salir del programa del menu
    def salirPrograma(self):
        self.director.quit_program()

    # Boton play del menu
    def ejecutarJuego(self):
        escena = Escena(self.director)
        self.director.stack_scene(escena)

    # Boton configuración del menu        
    #def mostrarPantallaConfiguracion(self):
        # self.pantallaActual = ...

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0