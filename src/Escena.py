

# Clase abstracta
class Escena:

    def __init__(self, director):
        # Referencia a director para poder llamar a sus métodos
        self.director = director


    # Métodos de cada escena; definiciones abstractas
    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")
    
    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")
    
    def draw(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")