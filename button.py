class Button():
    def __init__(self, image, position, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text_surface = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text_surface
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text_surface.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def change_color(self, position):
        if self.rect.collidepoint(position):
            self.text_surface = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text_surface = self.font.render(self.text_input, True, self.base_color)
