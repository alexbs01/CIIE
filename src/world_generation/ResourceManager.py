import pygame


class ResourceManager:
    def __init__(self):
        self.resources = {}

    def load_image(self, name, path):
        if name not in self.resources:
            try:
                image = pygame.image.load(path)
                self.resources[name] = image
            except pygame.error:
                print(f"No se pudo cargar la imagen: {path}")
                raise SystemExit
        return self.resources[name]

    def get_image(self, name):
        return self.resources.get(name)
