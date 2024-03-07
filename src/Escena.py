


class Escena:

    def __init__(self, director):
        self.director = director


    def update(self, *args):
        raise NotImplemented("Ten que implementar o método update.")

    def events(self, *args):
        raise NotImplemented("Ten que implementar o método eventos.")

    def draw(self, screen):
        raise NotImplemented("Ten que implementar o método debuxar.")