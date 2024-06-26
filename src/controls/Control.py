#Clase usada para prácticas

class Control():
    def __init__(self):
        self.up_key = None
        self.down_key = None
        self.left_key = None
        self.right_key = None
        self.attack_key = None


    # Estos metodos toman los eventos y/o la enumeración de teclas/botones 
    # presionados para determinar si se intentó llevar a cabo una de las siguientes
    # opciones de movimiento/accion.

    def up(self, keys):
        pass 

    def down(self, keys):
        pass

    def left(self, keys):
        pass

    def right(self, keys):
        pass

    def attack(self, keys):
        pass

    def pause(self, keys):
        pass

    def select(self, keys):
        pass

    # Metodos que asignan a una tecla/boton una accion concreta

    def set_up(self, key):
        self.up_key = key

    def set_down(self, key):
        self.down_key = key

    def set_left(self, key):
        self.left_key = key

    def set_right(self, key):
        self.right_key = key

    def set_attack(self, key):
        self.attack_key = key

    def set_select(self, key):
        self.select_key = key