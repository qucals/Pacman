import pygame
import game_object
import constants


class Label(game_object.GameObject):
    def __init__(self, position, text, font_name, size,
                 colour, handler_update=None, screen=None):
        super().__init__(position)

        self.text = text
        self.font_name = font_name
        self.size = size
        self.colour = colour

        self.update = super().update if handler_update is None else handler_update

        self._font = pygame.font.SysFont(self.font_name, self.size)
        self._text_rendered = self._font.render(self.text, False, self.colour)

    def draw(self, screen):
        text_size = self.get_text_size()

        x = self.position.x - text_size.x//2
        y = self.position.y - text_size.y//2

        screen.blit(self._text_rendered, [x, y])

    def get_text_size(self):
        text_size = self._text_rendered.get_size()

        return constants.VEC_2(text_size[0], text_size[1])
