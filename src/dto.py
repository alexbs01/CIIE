from settings import MAX_HEALTH

class PlayerDTO(object):
        
    def __init__(self, player, level):
        if player.health > 0:
            self.vida = player.health
            self.puntos = player.points
            self.max_jumps = 2 if level != 1 or player.got_boots else 1
            self.sword = player.got_sword if level >= 2 else False
        else:
            self.vida = MAX_HEALTH
            self.puntos = player.points // 2
            self.max_jumps = 2 if level != 1 else 1
            self.sword = False

    # getters
    def get_vida(self):
        return self.vida

    def get_puntos(self):
        return self.puntos
    
    def get_jumps(self):
        return self.max_jumps
    
    def get_sword(self):
        return self.sword

    # setters
    def set_vida(self, vida):
        self.vida = vida

    def set_puntos(self, puntos):
        self.puntos = puntos

    def set_jumps(self, jumps):
        self.max_jumps = jumps

    def set_sword(self, sword):
        self.sword = sword