import pygame
from entities.observer.Observer import Observer
from settings import *

RED = (200, 25, 25)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

class Ui():
    
    def __init__(self, display_surface):
        self.display_surface = display_surface


    def draw_text(self,text,font,text_col,x,y):
        img = font.render(text, True, text_col)
        self.display_surface.blit(img, (x,y))

    
    class HealthObserver(Observer):

        def __init__(self,x,y, display_surface, health):
            self.x = x
            self.y = y
            self.health = health
            self.max_health = MAX_HEALTH
            self.display_surface = display_surface


        def notify(self, new_health):

            # Update con la nueva vida
            self.health = new_health

            pygame.draw.rect(self.display_surface, BLACK, (self.x - 2, self.y - 2, 154, 24))
            pygame.draw.rect(self.display_surface, RED, (self.x, self.y, 150, 20))

            if self.health != 0:
                # Calculo vida linea verde
                ratio = self.health / self.max_health
                pygame.draw.rect(self.display_surface, GREEN, (self.x, self.y, 150 * ratio, 20))


    class PointsObserver(Observer):

        def __init__(self,points):
            self.points = points
            self.max_points = MAX_POINTS


        def notify(self, new_points):

            # Update con la cantidad de puntos
            if self.points < MAX_POINTS:
                if self.points + new_points !=0:
                    self.points += new_points
                else:
                    self.points = 0
    
    class KeyObserver(Observer):
        
        def __init__(self, display_surface):
            self.key = 0
            self.display_surface = display_surface
            self.key_img = pygame.image.load(PATH_ASSET_KEY)  # Cargar la imagen del icono de la llave
            self.key_img = pygame.transform.scale(self.key_img, (int(self.key_img.get_width() * 0.15), int(self.key_img.get_height() * 0.15)))
            self.font = pygame.font.Font("assets/inmortal.ttf", 25)  # Definir la fuente para el texto

        def notify(self, got_key):

            if got_key:
                self.key = 1

            # Dibujar el icono de la llave
            self.display_surface.blit(self.key_img, (50, 120))
            # Mostrar la cantidad de llaves
            img = self.font.render(": "+str(self.key), True, WHITE)
            self.display_surface.blit(img, (90, 120))


    class SwordObserver(Observer):
        
        def __init__(self, display_surface):
            self.sword = 0
            self.display_surface = display_surface
            self.sword_img = pygame.image.load(PATH_ASSET_SWORD)  # Cargar la imagen del icono de la llave
            self.sword_img = pygame.transform.scale(self.sword_img, (int(self.sword_img.get_width() * 0.15), int(self.sword_img.get_height() * 0.15)))
            self.font = pygame.font.Font("assets/inmortal.ttf", 25)  # Definir la fuente para el texto

        def notify(self, got_sword):

            if got_sword:
                self.sword = 1

                # Dibujar el icono de la llave
                self.display_surface.blit(self.sword_img, (50, 150))
                # Mostrar la cantidad de llaves
                img = self.font.render(": "+str(self.sword), True, WHITE)
                self.display_surface.blit(img, (90, 150))


    class EnemyHealthObserver(Observer):

        def __init__(self, enemy_sprite, display_surface, max_health):
            self.enemy_sprite = enemy_sprite
            self.max_health = max_health
            self.display_surface = display_surface
            self.font = pygame.font.Font(None, 16)  # Reducir el tamaño de la fuente para el texto

        def notify(self, new_health):
            # Update con la nueva vida
            self.enemy_sprite.health = new_health
            self.draw_health_bar()

        def draw_health_bar(self):
            # Posición de la barra de salud sobre la cabeza del enemigo
            x = self.enemy_sprite.rect.centerx - 30  # Centrar la barra de vida sobre la cabeza del enemigo
            y = self.enemy_sprite.rect.y - 12  # Ajustar la posición y

            if self.enemy_sprite.health > 0:  # Verificar si la vida del enemigo es mayor que cero
                # Dibuja el fondo de la barra de salud (rectángulo negro) más estrecho y menos alto
                pygame.draw.rect(self.display_surface, BLACK, (x - 2, y - 2, 62, 10))  # Ancho dividido por 2 (124/2 = 62)
                # Dibuja el rectángulo rojo que representa la vida máxima
                pygame.draw.rect(self.display_surface, RED, (x, y, 60, 8))  # Ancho dividido por 2 (120/2 = 60)

                if self.enemy_sprite.health > 0:
                    # Calcula la relación de la vida actual con la vida máxima
                    ratio = self.enemy_sprite.health / self.max_health
                    # Dibuja el rectángulo verde que representa la vida actual
                    pygame.draw.rect(self.display_surface, GREEN, (x, y, 60 * ratio, 8))  # Ancho dividido por 2 (120/2 = 60)






