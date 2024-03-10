# Clase para el patron observador

class Observer():
        
    def __init__(self, display_surface):
        self.display_surface = display_surface

    def notify(self, *args):
        pass
    