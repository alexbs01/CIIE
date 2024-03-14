import pygame
import csv

class ResourceManager:
    def __init__(self):
        self.resources = {}

    def load_resource(self, name, path, resource_type, font_size = None):
        if name not in self.resources:
            try:
                if resource_type == "image":
                    resource = pygame.image.load(path)
                elif resource_type == "font":
                    if font_size is not None:
                        resource = pygame.font.Font(path, font_size)
                    else:
                        resource = pygame.font.Font(path, 45)
                elif resource_type == "sound":
                    resource = pygame.mixer.Sound(path)
                elif resource_type == "csv":  # Agregar soporte para cargar archivos CSV
                    with open(path, newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        data = []
                        for row in reader:
                            data.append(row)
                    resource = data
                else:
                    raise ValueError("Tipo de recurso no válido")
                
                self.resources[name] = resource
            except pygame.error:
                print(f"No se pudo cargar el recurso {resource_type}: {path}")
                raise SystemExit
        return self.resources[name]

    def get_resource(self, name):
        return self.resources.get(name)
