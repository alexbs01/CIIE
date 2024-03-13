import pygame
from escene.Escena import Escena
from GUI import GUI
from settings import *
from escene.levels.Levels import Level1

class Menu(Escena):

    def __init__(self, director):

        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        # Creamos la lista de pantallas
        self.listaPantallas = []

        # Creamos las pantallas que vamos a tener
        # y las metemos en la lista
        # en nuestro caso solo tenemos 1
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
        # Creamos el nivel 1, le pasamos status None porque no tiene datos de otros niveles
        self.director.play_music()
        level = Level1(self.director, None)

        self.director.stack_scene(level)

    # Si al final agregamos menu configuracion sería aqui donde pantallaActual toma otro valor
    # Boton configuración del menu        
    #def mostrarPantallaConfiguracion(self):
        # self.pantallaActual = ...

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    def mostrarPantallaControles(self):
        self.listaPantallas.append(GUI.PantallaControles(self))
        self.pantallaActual += 1
  
    def returnPantalla(self):
            self.listaPantallas.pop()
            self.pantallaActual -= 1