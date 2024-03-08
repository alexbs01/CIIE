import pygame

RED = (200, 25, 25)
GREEN = (0, 255, 0)
BLACK = (0,0,0)

class Ui:
    
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()


    def draw_text(self,text,font,text_col,x,y):
        img = font.render(text, True, text_col)
        self.display_surface.blit(img, (x,y))

    
    class HealthObserver:

        def __init__(self,x,y, display_surface, health, max_health):
            self.x = x
            self.y = y
            self.display_surface = display_surface
            self.health = health
            self.max_health = max_health


        def update_health(self, new_health):

            # Update con la nueva vida
            self.health = new_health

            pygame.draw.rect(self.display_surface, BLACK, (self.x - 2, self.y - 2, 154, 24))
            pygame.draw.rect(self.display_surface, RED, (self.x, self.y, 150, 20))

            if self.health != 0:
                # Calculo vida linea verde
                ratio = self.health / self.max_health
                pygame.draw.rect(self.display_surface, GREEN, (self.x, self.y, 150 * ratio, 20))


    class PointsObserver:

            def __init__(self,points, max_points):
                self.points = points
                self.max_points = max_points


            def update_points(self, new_points):

                # Update con la cantidad de puntos
                if self.points + new_points !=0:
                    self.points += new_points
                else:
                    self.points = 0
            