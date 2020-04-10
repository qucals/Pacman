import os
import pygame

VEC_2 = pygame.math.Vector2

# Constants of size of the window
SCREEN_WIDTH = 610
SCREEN_HEIGHT = 670
DISPLAY_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

TOP_BUTTON_BUFFER = 50
MAP_WIDTH = SCREEN_WIDTH - TOP_BUTTON_BUFFER
MAP_HEIGHT = SCREEN_HEIGHT - TOP_BUTTON_BUFFER

CELL_WIDTH = MAP_WIDTH // 28
CELL_HEIGHT = MAP_HEIGHT // 30

MOVING_OBJECT_SIZE = (16, 16)
SPEED_OBJECT = 1

MAIN_FONT = 'arial black'
MAIN_SIZE_FONT = 16

PACMAN_START_POSITION = VEC_2(1, 1)

FPS = 60

# Events
UPDATE_PICTURE_EVENT = pygame.USEREVENT + 1

GAME_NAME = 'Pacman by Bizzi'

COIN_COLOUR = ((255, 255, 255))


def __loading_ghost_pictures(name):
    """ 
        This function is loading ghost pictures from res\ghosts\*
        To the array 'pictures'
    """

    dirpath = os.path.join('res', 'ghosts')

    if name == 'ghost':
        path = os.path.join(dirpath, name + '.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, MOVING_OBJECT_SIZE)
        return image

    postfixes = ['down', 'left',
                 'right', 'up']
    pictures = {}

    for i in range(len(postfixes)):
        path = os.path.join(dirpath, '{name}_{postfix}.png'.format(name=name,
                                                                   postfix=postfixes[i]))
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, MOVING_OBJECT_SIZE)
        pictures[postfixes[i]] = image

    return pictures


def __loading_pacman_pictures():
    name = 'pacman'
    pictures = {}
    dirpath = os.path.join('res', 'pacman')
    postfixes = ['default',
                 'down', 'left',
                 'right', 'up']

    for i in range(len(postfixes)):
        path = os.path.join(dirpath, '{name}_{postfix}.png'.format(name=name,
                                                                   postfix=postfixes[i]))
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, MOVING_OBJECT_SIZE)
        pictures[postfixes[i]] = image

    return pictures


def __loading_maps(count_maps):
    maps_walls = []
    dirpath = os.path.join('res', 'level_walls')

    for i in range(1, count_maps):
        map_walls = {}
        walls = []
        coins = []

        path = os.path.join(dirpath, 'map_{number}.txt'.format(number=i))

        with open(path, mode='r') as file:
            for yidx, line in enumerate(file):
                for xidx, symbol in enumerate(line):
                    if symbol == '1':
                        walls.append(VEC_2(xidx, yidx))
                    elif symbol == 'C':
                        coins.append(VEC_2(xidx, yidx))
        map_walls['walls'] = walls
        map_walls['coins'] = coins

        maps_walls.append(map_walls)

    return maps_walls


# There are all loaded maps
MAPS = [
    os.path.join(os.path.join('res', 'maps'), 'map_1.png'),
    os.path.join(os.path.join('res', 'maps'), 'map_2.png')
]

MAPS_WALLS = __loading_maps(len(MAPS))

GHOSTS_PICTURES = {
    'red': __loading_ghost_pictures('red'),
    'blue': __loading_ghost_pictures('blue'),
    'pink': __loading_ghost_pictures('pink'),
    'orange': __loading_ghost_pictures('orange'),
    'ghost': __loading_ghost_pictures('ghost')
}

PACMAN_PICTURES = __loading_pacman_pictures()

WIN_SOUND = os.path.join(os.path.join('res', 'audio'), 'WIN.mp3')
