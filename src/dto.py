from settings import MAX_HEALTH

class PlayerDTO(object):
    def __init__(self, player, level):
        
        if level == 1:
            if (player.health > 0):
                self.vida = player.health
                self.puntos = player.points
                self.boots = player.got_boots
                self.sword = False

            else:
                self.vida = MAX_HEALTH
                self.puntos = player.points // 2
                self.boots = False
                self.sword = False

        else:
            if (player.health > 0):
                self.vida = player.health
                self.puntos = player.points
                self.boots = True
                self.sword = player.got_sword
            else:
                self.vida = MAX_HEALTH
                self.puntos = player.points // 2
                self.sword = False
                self.boots = True

    # getters
    def get_vida(self):
        return self.vida

    def get_puntos(self):
        return self.puntos
    
    def get_boots(self):
        return self.boots
    
    def get_sword(self):
        return self.sword

    # setters
    def set_vida(self, vida):
        self.vida = vida

    def set_puntos(self, puntos):
        self.puntos = puntos

    def set_boots(self, boots):
        self.boots = boots

    def set_sword(self, sword):
        self.sword = sword