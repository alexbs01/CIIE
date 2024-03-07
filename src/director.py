
import pygame

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT





class Director():

    def __init__(self):
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        pygame.display.set_caption("Game")
        pygame.mouse.set_visible(False)
        
        self.stack = []
        
        self.quit_scene = False
        self.clock = pygame.time.Clock()

    def loop(self, scene):
        self.quit_scene = False

        
        pygame.event.clear()
        
        
        while not self.quit_scene:
            tiempo_pasado = self.clock.tick(60)
            
            scene.events(pygame.event.get())
            
            scene.update(tiempo_pasado)
            
            scene.draw(self.screen)
            pygame.display.flip()

    def execute(self):
        while (len(self.stack)>0):
            scene = self.stack[len(self.stack)-1]
            
            self.loop(scene)

    def exit_scene(self):
        self.quit_scene = True
        
        if (len(self.stack)>0):
            self.stack.pop()

    def quit_program(self):
        self.stack = []
        self.quit_scene = True

    def change_scene(self, scene):
        self.exit_scene()
        self.stack.append(scene)

    def stack_scene(self, scene):
        self.quit_scene = True
        self.stack.append(scene)