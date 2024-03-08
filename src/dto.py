class PlayerDTO(object):
    def __init__(self, player):
        self.vida = player.health
        self.puntos = player.points

    # getters
    def get_vida(self):
        return self.vida

    def get_puntos(self):
        return self.puntos

    # setters
    def set_vida(self, vida):
        self.vida = vida

    def set_puntos(self, puntos):
        self.puntos = puntos