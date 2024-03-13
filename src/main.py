import pygame
from settings import *
from director import Director
from escene.menu.Menu import Menu

def main():

    # Inicializamos la libreria de pygame
    pygame.init()

    # Creamos el director
    director = Director()

    # Creamos la escena con la pantalla inicial
    escena = Menu(director)

    # Le decimos al director que apile esta escena
    director.stack_scene(escena)

    # Y ejecutamos el juego
    director.execute()

    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()


if __name__ == "__main__":
    main()