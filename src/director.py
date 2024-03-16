
import pygame

from settings import MUSIC_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_MUSIC_VOLUME



class Director():

    # Implementado patron Singleton, solo puede instanciarse un objeto Director
    _instance = None

    def __new__(clase):
        if clase._instance is None:
            clase._instance = super().__new__(clase)
        return clase._instance


    def __init__(self):
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game")
        pygame.mouse.set_visible(True)
        
        # Pila para almacenar las escenas
        self.stack = []
        
        # Variable para comprobar si la escena a terminado
        self.quit_scene = False
        self.music_playing = False

        self.clock = pygame.time.Clock()

    # Bucle principal de la escena
    def loop(self, scene):
        self.quit_scene = False

        pygame.event.clear()
        
        while not self.quit_scene:
            tiempo_pasado = self.clock.tick(60)
            
            scene.events(pygame.event.get())
    
            scene.update(tiempo_pasado)

            scene.draw(self.screen)

            
            pygame.display.flip()

    # Ejecuta la escena que este en la cima de la pila
    def execute(self):
        while (len(self.stack)>0):
            scene = self.stack[len(self.stack)-1]
            
            self.loop(scene)

    # Salir de una escena
    def exit_scene(self):
        self.quit_scene = True
        
        if (len(self.stack)>0):
            self.stack.pop()

    # Salir del programa, se dejará de ejecutar el bucle principal
    def quit_program(self):
        self.stack = []
        self.quit_scene = True

    # Cambiar de una escena a otra
    def change_scene(self, scene):
        self.exit_scene()
        self.stack.append(scene)

    # Apilar la escena actual y ejecutar otra nueva. No elimina la escena actual
    def stack_scene(self, scene):
        self.quit_scene = True
        self.stack.append(scene)

    # Reproducir música de fondo
    def play_music(self):
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(BACKGROUND_MUSIC_VOLUME)

        self.music_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.music_playing = False

    def unpause_music(self):
        pygame.mixer.music.unpause()
        self.music_playing = True
