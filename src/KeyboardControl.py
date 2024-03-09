import pygame
from Control import Control


class KeyboardControl(Control):
    def __init__(self):
        super().__init__()

        # Asignamos cada accion con su tecla
        self.up_key = pygame.K_w
        self.down_key = pygame.K_s
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d
        self.attack_key = pygame.K_SPACE
        self.select_key = pygame.K_RETURN

    # Estos métodos permiten verificar si una tecla específica está siendo presionada

    def up(self, keys):
        return keys[self.up_key]

    def down(self, keys):
        return keys[self.down_key]

    def left(self, keys):
        return keys[self.left_key]
    
    def right(self, keys):
        return keys[self.right_key]
    
    def attack(self, keys):
        return keys[self.attack_key]

    def select(self, keys):
        return keys[self.select_key]