import pygame
from world_generation.ResourceManager import ResourceManager
from settings import *

class GUI():
    # Cargamos los recursos con el resource manager
    resource_manager = ResourceManager()

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
            pass        
        
        def accion(self):
            pass        

    class Boton(ElementoGUI):
        def __init__(self, pantalla, img, posicion, scale):
            # Se carga la imagen del boton
            self.imagen = img
            self.imagen = pygame.transform.scale(self.imagen, scale)
            # Se llama al método de la clase padre con el rectángulo
            GUI.ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
            # Se coloca el rectangulo en su posicion
            self.establecerPosicion(posicion)

        def draw(self, pantalla):
            pantalla.blit(self.imagen, self.rect)

        def check_for_input(self, position):
            return self.rect.collidepoint(position)


    class BotonJugar(Boton):
        def __init__(self, pantalla):
            # carga la imagen con el recurso manager
            self.img = GUI.resource_manager.load_resource("play_boton", PATH_PLAY_BOTTON, "image")
            super().__init__(pantalla, self.img,(220, 250), (350, 70))

        def accion(self):
            self.pantalla.menu.ejecutarJuego()

    class BotonControles(Boton):
        def __init__(self, pantalla):
            self.img = GUI.resource_manager.load_resource("controles_boton", PATH_CONTROLS_BOTTON, "image")
            super().__init__(pantalla, self.img, (220, 400), (350, 70))

        def accion(self):
            self.pantalla.menu.mostrarPantallaControles()

    class BotonSalir(Boton):
        def __init__(self, pantalla):
            self.img = GUI.resource_manager.load_resource("exit_boton", PATH_EXIT_BOTTON, "image")
            super().__init__(pantalla, self.img, (220, 550), (350, 70))

        def accion(self):
            self.pantalla.menu.salirPrograma()

    class BotonReturn(Boton):
        def __init__(self, pantalla):
            self.img = GUI.resource_manager.load_resource("return_boton", PATH_BACK_BOTTON, "image")
            super().__init__(pantalla, self.img, (365, 600), (self.img.get_width(), self.img.get_height()))

        def accion(self):
            self.pantalla.menu.returnPantalla()    

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
            font = GUI.resource_manager.load_resource("title_font", "assets/inmortal.ttf", "font", 50)
            GUI.TextoGUI.__init__(self, pantalla, font, COLOR_TEXT_MENU, 'MENU', (310, 100))

        def action(self):
            pass

    class TextoJugar(TextoGUI):
        def __init__(self, pantalla):
            font = GUI.resource_manager.load_resource("play_font", "assets/inmortal.ttf", "font", 45)
            GUI.TextoGUI.__init__(self, pantalla, font, (0,0,0), 'Play', (350, 250))


        def accion(self):
            self.pantalla.menu.ejecutarJuego()


    class ControlesBotonText(TextoGUI):
        def __init__(self, pantalla):
            font = GUI.resource_manager.load_resource("controles_font", "assets/inmortal.ttf", "font", 45)
            GUI.TextoGUI.__init__(self, pantalla, font, (0,0,0), 'Controles', (300, 400))
            
        def accion(self):
            self.pantalla.menu.mostrarPantallaControles()
            
    class ControlesText(TextoGUI):
        def __init__(self, pantalla, texto, posicion, font_size = 25):
            font = GUI.resource_manager.load_resource("controles_font2", "assets/inmortal.ttf", "font", font_size)
            GUI.TextoGUI.__init__(self, pantalla, font, (255,255,255), texto, posicion)

        def action(self):
            pass

        

    class TextoSalir(TextoGUI):
        def __init__(self, pantalla):
            # La fuente la debería cargar el estor de recursos
            font = GUI.resource_manager.load_resource("exit_font", "assets/inmortal.ttf", "font", 45)
            GUI.TextoGUI.__init__(self, pantalla, font, (0,0,0), 'Salir', (350, 550))

        def accion(self):
            self.pantalla.menu.salirPrograma()


    class PantallaGUI:
        def __init__(self, menu):
            self.menu = menu
            # Se carga la imagen de fondo
            self.image = GUI.resource_manager.load_resource("bg_menu", PATH_BG_MENU, "image")
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
            controles_text = GUI.ControlesBotonText(self)

            # Créase o botón e añádese á lista
            play_boton = GUI.BotonJugar(self)
            controles_boton = GUI.BotonControles(self)
            exit_boton = GUI.BotonSalir(self)
            

            # Añadir elementos a la lista

            self.Elementos_GUI.append(play_boton)
            self.Elementos_GUI.append(controles_boton)
            self.Elementos_GUI.append(exit_boton)

            self.Elementos_GUI.append(play_text)
            self.Elementos_GUI.append(exit_text)
            self.Elementos_GUI.append(title_text)
            self.Elementos_GUI.append(controles_text)
            


    class PantallaControles(PantallaGUI):

        def __init__(self, menu):
            GUI.PantallaGUI.__init__(self, menu)
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.image.fill((0, 0, 0)) # Fondo negro
                
            # Crear texto explicativo de los controles
            controles = [
                "Controles:",
                "",
                "W: Saltar",
                "A: Moverse a la izquierda",
                "D: Moverse a la derecha",
                "ESPACIO: Atacar",
                "P: Pausar",
                "",
                "Items:"
            ]
                
            y_position = SCREEN_HEIGHT // 10  # Mover más arriba
            for text in controles:
                texto_controles = GUI.ControlesText(self, text, (SCREEN_WIDTH // 8, y_position))
                self.Elementos_GUI.append(texto_controles)
                y_position += 45  # Ajustar la posición vertical para el siguiente texto

            
            # Añadir imágenes y textos explicativos de las habilidades
            sword_img = GUI.resource_manager.load_resource("sword_icon", PATH_ASSET_SWORD, "image")

            sword_imgBoton = GUI.Boton(self, sword_img, (SCREEN_WIDTH // 8, y_position), (int(sword_img.get_width() * 0.85), int(sword_img.get_height() * 0.85)))
            sword_text = GUI.ControlesText(self, "Sirve para romper bloques", ((SCREEN_WIDTH // 8) + 40, y_position))

            block_img = GUI.resource_manager.load_resource("block_icon", "assets/tiles/12.png", "image")
            block_imgBoton = GUI.Boton(self, block_img, ((SCREEN_WIDTH // 8) + 360, y_position), (int(block_img.get_width() * 0.85), int(block_img.get_height() * 0.85)))

            y_position += 45  # Ajustar la posición vertical para el siguiente texto

            boots_img = GUI.resource_manager.load_resource("boots_icon", PATH_ASSET_BOOTS, "image")
            boots_imgBoton = GUI.Boton(self, boots_img, ((SCREEN_WIDTH // 8), y_position), (int(boots_img.get_width() * 1.75), int(boots_img.get_height() * 1.75)))
            boots_text = GUI.ControlesText(self, "Permite hacer doble salto pulsando W dos veces", ((SCREEN_WIDTH // 8) + 40, y_position))

            y_position += 45  # Ajustar la posición vertical para el siguiente texto

            key_img = GUI.resource_manager.load_resource("key_icon", PATH_ASSET_KEY, "image")
            key_imgBoton = GUI.Boton(self, key_img, ((SCREEN_WIDTH // 8), y_position), (int(key_img.get_width() * 0.15), int(key_img.get_height() * 0.15)))
            key_text = GUI.ControlesText(self, "Permite abrir la puerta y pasar de nivel", ((SCREEN_WIDTH // 8) + 40, y_position))


            self.Elementos_GUI.extend([sword_imgBoton, sword_text, block_imgBoton, boots_imgBoton, boots_text, key_imgBoton, key_text])


            # Añadir botón para volver al menú
            volver_boton = GUI.BotonReturn(self)
            self.Elementos_GUI.append(volver_boton)


            







        
    
