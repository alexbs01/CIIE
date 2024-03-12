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
        

    class Boton(ElementoGUI):
        def __init__(self, pantalla, img, posicion):
            # Se carga la imagen del boton
            self.imagen = img
            self.imagen = pygame.transform.scale(self.imagen, (350, 70))
            # Se llama al método de la clase padre con el rectángulo
            GUI.ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
            # Se coloca el rectangulo en su posicion
            self.establecerPosicion(posicion)

        def draw(self, pantalla):
            pantalla.blit(self.imagen, self.rect)

        def check_for_input(self, position):
            return self.rect.collidepoint(position)

        def change_color(self, position):
            pass

    class BotonJugar(Boton):
        def __init__(self, pantalla):
            self.img = pygame.image.load(PATH_PLAY_BOTTON)
            super().__init__(pantalla, self.img, (220, 250))

        def accion(self):
            self.pantalla.menu.ejecutarJuego()

    class BotonControles(Boton):
        def __init__(self, pantalla):
            self.img = pygame.image.load(PATH_CONFIG_BOTTON)
            super().__init__(pantalla, self.img, (220, 400))

        def accion(self):
            pass

    class BotonSalir(Boton):
        def __init__(self, pantalla):
            self.img = pygame.image.load(PATH_EXIT_BOTTON)
            super().__init__(pantalla, self.img, (220, 550))

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
            GUI.TextoGUI.__init__(self, pantalla, font, COLOR_TEXT_MENU, 'MENU', (320, 100))

    class TextoJugar(TextoGUI):
        def __init__(self, pantalla):
            font = pygame.font.Font("assets/inmortal.ttf", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, (0,0,0), 'Play', (350, 250))


        def accion(self):
            self.pantalla.menu.ejecutarJuego()


    class ControlesText(TextoGUI):
        def __init__(self, pantalla):
            font = pygame.font.Font("assets/inmortal.ttf", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, (0,0,0), 'Controles', (300, 400))
            
        def accion(self):
            self.pantalla.menu.mostrarPantallaControles()
            

    class TextoSalir(TextoGUI):
        def __init__(self, pantalla):
            # La fuente la debería cargar el estor de recursos
            font = pygame.font.Font("assets/inmortal.ttf", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, (0,0,0), 'Salir', (350, 550))

        def accion(self):
            self.pantalla.menu.salirPrograma()


    class PantallaGUI:
        def __init__(self, menu):
            self.menu = menu
            # Se carga la imagen de fondo
            self.image = pygame.image.load(PATH_BG_MENU)
            self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # Se tiene una lista de elementos GUI
            self.Elementos_GUI = []

        def eventos(self, lista_eventos):

            for evento in lista_eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.elementoClic = None
                    for elemento in self.Elementos_GUI:
                        if elemento.posicionEnElemento(evento.pos):
                            self.elementoClic = elemento

            if evento.type == pygame.MOUSEBUTTONUP:
                for elemento in self.Elementos_GUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()
            


        def draw(self, screen):
            screen.blit(self.image, self.image.get_rect())
            # Despois debúxanse os botóns
            for element in self.Elementos_GUI:
                element.draw(screen)

    class PantallaInicial(PantallaGUI):
        def __init__(self, menu):
            GUI.PantallaGUI.__init__(self, menu)

            # Créase o texto e añádese á lista
            play_text = GUI.TextoJugar(self)
            exit_text = GUI.TextoSalir(self)
            title_text = GUI.TitleText(self)
            controles_text = GUI.ControlesText(self)

            # Créase o botón e añádese á lista
            play_boton = GUI.BotonJugar(self)
            controles_boton = GUI.BotonControles(self)
            exit_boton = GUI.BotonSalir(self)
            

            # Añadir elementos a la lista
            self.Elementos_GUI.append(play_text)
            self.Elementos_GUI.append(exit_text)
            self.Elementos_GUI.append(title_text)
            self.Elementos_GUI.append(controles_text)
            
            self.Elementos_GUI.append(play_boton)
            self.Elementos_GUI.append(controles_boton)
            self.Elementos_GUI.append(exit_boton)


            # Método para mostrar la pantalla de controles
            def mostrarControles():
                menu.mostrarPantallaControles()

            # Enlace de acción del botón para mostrar la pantalla de controles
            controles_boton.accion = mostrarControles


            #Tamén creamos unha lista cos elementos que queremos que sexan interactivos
            #self.GUI_interactive_elements.append(play_text)
            #self.GUI_interactive_elements.append(config_text)
            #self.GUI_interactive_elements.append(exit_text)
            #self.selected = self.GUI_interactive_elements[0]
            #self.selected.select(self)



          
    class PantallaControles(PantallaGUI):
        def __init__(self, menu):
            GUI.PantallaGUI.__init__(self, menu)
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.image.fill((0, 0, 0)) # Fondo negro
            
            # Crear texto explicativo de los controles
            controles = [
                "Controles:",
                "W: Saltar",
                "A: Moverse a la izquierda",
                "D: Moverse a la derecha",
                "ESPACIO: Atacar",
                "P: Pausar"
            ]
            
            y_position = SCREEN_HEIGHT // 4 # Mover más arriba
            for text in controles:
                self.texto_controles = GUI.TextoGUI(self, pygame.font.Font("assets/inmortal.ttf", 30), (255, 255, 255), 
                                                    text, (SCREEN_WIDTH // 4, y_position)) # Mover más a la izquierda
                self.Elementos_GUI.append(self.texto_controles)
                if text == "Controles:":  # Si es el título "Controles", agregamos un espacio adicional
                    y_position += 30  # Incrementamos la posición vertical
                y_position += 30  # Ajustar la posición vertical para el siguiente texto

            # Añadir botón para volver al menú
            volver_boton = GUI.Boton(self, pygame.image.load(PATH_BACK_BOTTON), (220, 600)) # Ajustar la posición del botón
            volver_boton.accion = self.volverMenu
            self.Elementos_GUI.append(volver_boton)
            
        def volverMenu(self):
            self.menu.mostrarPantallaInicial()







        
    
