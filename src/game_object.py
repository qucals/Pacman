from pygame.rect import Rect


class GameObject:
    """ This is abstact class of any game's object  """

    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]

    def draw(self, screen):
        pass

    def update(self):
        pass
