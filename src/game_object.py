import constants
from pygame.rect import Rect


class GameObject:
    """ This is abstact class of any game's object  """

    def __init__(self, position):
        if type(position) == constants.VEC_2:
            # Because if we give this value forward it will be change like other variables that 'copy' it
            # It happens because of architecture of python
            _copy = constants.VEC_2(position.x, position.y)

            self.position = _copy
        else:
            raise ValueError

    def draw(self, screen):
        pass

    def update(self):
        pass
