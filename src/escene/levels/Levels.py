
from settings import *
from escene.levels.LevelStructure import Level
from items.Interactives import Interactive_obj

class Level1(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status, PATH_LEVEL_1)

        
    def notify(self,player):

        if player.health <= 0:
            #dead = Final(self.director, 0, self.player.points)
            self.director.stack_scene(Level1(self.director, self.getterAndSetter))
            #self.director.stack_scene(dead)

        if player.got_key and Interactive_obj.Door.open:
            level = Level2(self.director, self.getterAndSetter)
            self.director.stack_scene(level)
            
            
            # añadirlo a la pila

class Level2(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status, PATH_LEVEL_2)

    def notify(self,player):

        if player.health <= 0:
            #dead = Final(self.director, 0, self.player.points)
            self.director.stack_scene(Level2(self.director, self.getterAndSetter))
            #self.director.stack_scene(dead)

        if player.got_key and Interactive_obj.Door.open:
            level = Level3(self.director, self.getterAndSetter)
            self.director.stack_scene(level)
            
            
            # añadirlo a la pila

class Level3(Level):

    def __init__(self, director, player_status):
        super().__init__(director, player_status,PATH_LEVEL_3)

    def notify(self,player):

        if player.health <= 0:
            #dead = Final(self.director, 0, self.player.points)
            self.director.stack_scene(Level3(self.director, self.getterAndSetter))
            #self.director.stack_scene(dead)

        if player.got_key and Interactive_obj.Door.open:
            level = Level2(self.director, self.getterAndSetter)
            self.director.stack_scene(level)
            
            
            # añadirlo a la pila