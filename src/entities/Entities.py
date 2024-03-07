import pygame

class Entity:
    def __init__(self, x, y, speed, resource_manager): # Cucumber
        pygame.sprite.Sprite.__init__(self)
        self.original_x = x
        self.original_y = y
        self.step_count = 0
        self.max_steps = 120
        self.observers = []
        self.health = 100
        self.speed = speed
        self.direction = 1
        self.resource_manager = resource_manager
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.last_attack_time = 0

        self.move_distance = 20  # Número de píxeles para moverse aleatoriamente
        self.random_move_speed = 0.5  # Velocidad de movimiento aleatorio más lenta

        # Tipos de animaciones
        animation_types = ['Idle', 'Run', 'Attack', 'Hit', 'DeathGround']

        # Bucle que comprueba que animacion hacer
        for animation in animation_types:
            temp_list = []  # Reseteamos lista temporal

            # Contamos n de ficheros en la carpeta
            n_frames = len(os.listdir(f'assets/enemies/Cucumber/{animation}'))
            for i in range(n_frames):
                img_path = f'assets/enemies/Cucumber/{animation}/{i}.png'
                img = self.resource_manager.load_image(img_path, img_path)
                if img is not None:  # Asegurarse de que la imagen se ha cargado correctamente
                    temp_list.append(img)
                else:
                    print(f"No se pudo cargar la imagen: {img_path}")
            self.animation_list.append(temp_list)

        # Asegurarse de que la imagen se ha cargado correctamente
        if self.animation_list[self.action]:
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
        else:
            self.image = None
            self.rect = pygame.Rect(x, y, 0, 0)

        self.rect.x = x
        self.rect.y = y
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        
    def __init__(self, x, y, speed, resource_manager): # Whale
        pygame.sprite.Sprite.__init__(self)
        self.original_x = x
        self.original_y = y
        self.observers = []
        self.health = 10
        self.step_count = 0
        self.max_steps = 120
        self.speed = speed
        self.direction = 1
        self.resource_manager = resource_manager
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.last_attack_time = 0

        self.move_distance = 20  # Número de píxeles para moverse aleatoriamente
        self.random_move_speed = 0.5  # Velocidad de movimiento aleatorio más lenta

        # Tipos de animaciones
        animation_types = ['Idle', 'Run', 'Attack', 'Hit', 'DeathGround']

        # Bucle que comprueba qué animación hacer
        for animation in animation_types:
            temp_list = []  # Reseteamos lista temporal

            # Contamos n de ficheros en la carpeta
            n_frames = len(os.listdir(f'assets/enemies/Whale/{animation}'))
            for i in range(1, n_frames + 1):  # Empieza desde 1 en lugar de 0
                img_path = f'assets/enemies/Whale/{animation}/{i}.png'
                img = self.resource_manager.load_image(img_path, img_path)
                if img is not None:  # Asegurarse de que la imagen se ha cargado correctamente
                    temp_list.append(img)
                else:
                    print(f"No se pudo cargar la imagen: {img_path}")
            self.animation_list.append(temp_list)

        # Asegurarse de que la imagen se ha cargado correctamente
        if self.animation_list[self.action]:
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
        else:
            self.image = None
            self.rect = pygame.Rect(x, y, 0, 0)

        self.rect.x = x
        self.rect.y = y
        self.collision_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)