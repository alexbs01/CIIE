import pygame
from world_generation.ResourceManager import ResourceManager
from settings import *

class GUI():

    class ElementoGUI:
   
        def __init__(self, pantalla, rectangulo):
            self.pantalla = pantalla
            self.rect = rectangulo

        # Se situan en la pantalla el boton
        def establecerPosicion(self, posicion):
            (posicionx, posiciony) = posicion
            self.rect.left = posicionx
            self.rect.bottom = posiciony

        # Indica si se ha hecho click en el boton
        def posicionEnElemento(self, posicion):
            (posicionx, posiciony) = posicion
            if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
                    return True
            else:
                return False
            

        # Metodos abstractos
        def draw(self):
            raise NotImplemented("Tiene que implementar el metodo dibujar.")
        
        def accion(self):
            raise NotImplemented("Tiene que implementar el metodo accion.")
        

    class Boton:
        def __init__(self, pantalla, nombreImagen, posicion):
            # Se carga la imagen del boton
            self.imagen = pygame.image.load(nombreImagen)
            self.imagen = pygame.transform.scale(self.imagen, (20, 20))
            
            # Se llama al método de la clase padre con el rectángulo
            self.rect = self.imagen.get_rect()
            self.rect.topleft = posicion

            self.pantalla = pantalla

        def draw(self, pantalla):
            pantalla.blit(self.imagen, self.rect)

        def check_for_input(self, position):
            if self.rect.collidepoint(position):
                return True
            return False

        def change_color(self, position):
            pass

    class BotonJugar(Boton):
        def __init__(self, pantalla):
            super().__init__(pantalla, 'boton_verde.png', (580, 530))

        def accion(self):
            self.pantalla.menu.ejecutarJuego()

    class BotonSalir(Boton):
        def __init__(self, pantalla):
            super().__init__(pantalla, 'boton_rojo.png', (580, 560))

        def accion(self):
            self.pantalla.menu.salirPrograma()

    class TextoGUI(ElementoGUI):
        def __init__(self, pantalla, fuente, color, texto, posicion):
            # Se crea la imagen del texto
            self.imagen = fuente.render(texto, True, color)
            # Se llama al método de la clase padre con el rectángulo
            GUI.ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
            # Se coloca el rectangulo en su posicion
            self.establecerPosicion(posicion)

        def draw(self, pantalla):
            pantalla.blit(self.imagen, self.rect)


    class TitleText(TextoGUI):
        def __init__(self, pantalla):
            font = pygame.font.Font("assets/inmortal.ttf", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, COLOR_TEXT_MENU, 'MENU', (260, 250))

    class TextoJugar(TextoGUI):
        def __init__(self, pantalla):
            # La fuente la debería cargar el estor de recursos
            font = pygame.font.Font("assets/inmortal.ttf", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, (0, 0, 0), 'Play', (400, 250))

        def accion(self):
            self.pantalla.menu.ejecutarJuego()

    class TextoSalir(TextoGUI):
        def __init__(self, pantalla):
            # La fuente la debería cargar el estor de recursos
            font = pygame.font.Font("assets/inmortal.ttf", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, COLOR_TEXT_MENU, 'Salir', (400, 550))

        def accion(self):
            self.pantalla.menu.salirPrograma()


    class ConfigText(TextoGUI):
        def __init__(self, pantalla):
            font = pygame.font.Font("assets/inmortal.ttf", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, COLOR_TEXT_MENU, 'Configuración', (400, 400))
            
    class PantallaGUI:
        def __init__(self, menu):
            self.menu = menu
            # Se carga la imagen de fondo
            self.image = pygame.image.load(PATH_BG_MENU)
            self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # Se tiene una lista de elementos GUI
            self.elementosGUI = []

        def eventos(self, lista_eventos):

            for evento in lista_eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.elementoClic = None
                    for elemento in self.elementosGUI:
                        if elemento.posicionEnElemento(evento.pos):
                            self.elementoClic = elemento

            if evento.type == pygame.MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()

        def draw(self, screen):
            # Primeiro debúxase a imaxe de fondo
            screen.blit(self.image, self.image.get_rect())
            # Despois debúxanse os botóns
            #for element in self.GUI_elements:
            #    element.draw(screen)

    class PantallaInicial(PantallaGUI):

        def __init__(self, menu):
            GUI.PantallaGUI.__init__(self, menu)

            # Créase o texto e añádese á lista
            play_text = GUI.TextoJugar(self)
            exit_text = GUI.TextoSalir(self)
            title_text = GUI.TitleText(self)
            config_text = GUI.ConfigText(self)
            #self.GUI_elements.append(title_text)
            #self.GUI_elements.append(play_text)
            #self.GUI_elements.append(config_text)
            #self.GUI_elements.append(exit_text)

            #Tamén creamos unha lista cos elementos que queremos que sexan interactivos
            #self.GUI_interactive_elements.append(play_text)
            #self.GUI_interactive_elements.append(config_text)
            #self.GUI_interactive_elements.append(exit_text)
            #self.selected = self.GUI_interactive_elements[0]
            #self.selected.select(self)

        
    
