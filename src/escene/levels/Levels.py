
from settings import *
from escene.levels.LevelStructure import Level
from items.Interactives import Interactive_obj
from dto import PlayerDTO
from escene.Escena import Escena

class Level1(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status, PATH_LEVEL_1)
        
        
    def run(self,player):
        super().run(player)

        player_status = PlayerDTO(player,1)

        if player.health <= 0:
            self.director.stop_music() # Al morir paramos la musica
            self.director.play_music(MUSIC_PATH) # Y la volvemos a reproducir para empezar el nivel
            self.director.change_scene(Level1(self.director, player_status))


        for door in self.item_door:
            if player.rect.colliderect(door.rect) and player.got_key:
                next_lvl = door.set_open()  # Establece la puerta como abierta
            elif not door.is_open():
                next_lvl = door.set_closed()  # Establece la puerta como cerrada

        if next_lvl:
            self.director.change_scene(Level2(self.director, player_status))
            # cambia de escena

class Level2(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status, PATH_LEVEL_2)

    def run(self,player):

        super().run(player)

        player_status = PlayerDTO(player,2)

        if player.health <= 0:
            self.director.stop_music()
            self.director.play_music(MUSIC_PATH)

            self.director.change_scene(Level2(self.director, player_status))
            # cambia de escena

        for door in self.item_door:
            if player.rect.colliderect(door.rect) and player.got_key:
                next_lvl = door.set_open()  # Establece la puerta como abierta
            elif not door.is_open():
                next_lvl = door.set_closed()  # Establece la puerta como cerrada

        if next_lvl:
            self.director.change_scene(Level3(self.director, player_status))
            # cambia de escena


class Level3(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status,PATH_LEVEL_3)

    def run(self,player):

        super().run(player)

        player_status = PlayerDTO(player,3)

        if player.health <= 0:
            self.director.stop_music()
            self.director.play_music(MUSIC_PATH)

            self.director.change_scene(Level3(self.director, player_status))
            # cambia de escena

        for door in self.item_door:
            if player.rect.colliderect(door.rect) and player.got_key:
                next_lvl = door.set_open()  # Establece la puerta como abierta
            elif not door.is_open():
                next_lvl = door.set_closed()  # Establece la puerta como cerrada

        if next_lvl:
            self.director.stop_music()
            self.director.change_scene(Final(self.director, player.get_points()))
            # cambia de escena

class Final(Escena):

    def __init__(self, director, puntos_finales):
        Escena.__init__(self, director)
        self.puntos_finales = puntos_finales

    def update(self, *args):
        pass
    
    def events(self, lista_eventos):
        for evento in lista_eventos:
        # Si se quiere salir, se le indica al director
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.quit_program()
    
    def draw(self, screen):
        screen.fill(BG2)
        
        # Código para dibujar el mensaje de "FIN"
        fin_font = pygame.font.Font("assets/inmortal.ttf", 100)  # Fuente y tamaño del mensaje de "FIN"
        fin_text = fin_font.render("FIN", True, WHITE)  # Renderiza el texto "FIN" en blanco
        fin_rect = fin_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Centra el texto en la pantalla
        screen.blit(fin_text, fin_rect)  # Dibuja el texto en la pantalla
        
        # Código para dibujar la puntuación
        score_font = pygame.font.Font("assets/inmortal.ttf", 50)  # Fuente y tamaño para la puntuación
        score_text = score_font.render("Puntuacion: " + str(self.puntos_finales), True, WHITE)  # Renderiza el texto de la puntuación
        score_rect = score_text.get_rect(midtop=(SCREEN_WIDTH // 2, fin_rect.bottom + 20))  # Posiciona la puntuación debajo del mensaje de "FIN"
        screen.blit(score_text, score_rect)  # Dibuja la puntuación en la pantalla