import pygame
import game_object


class Label(game_object.GameObject):
    def __init__(self, position, text, font_name, size, 
                 colour, handler_update=None, screen=None):
        super().__init__(position)

        self.text = text
        self.font_name = font_name
        self.size = size
        self.colour = colour

        self.update = super().update if handler_update is None else handler_update

    def draw(self, screen):
        font = pygame.font.SysFont(self.font_name, self.size)
        text = font.render(self.text, False, self.colour)

        screen.blit(text, [self.x, self.y])
