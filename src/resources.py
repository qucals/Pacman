import pygame
import os
import constants


def __loading_ghosts_pictures():
    """ 
        This function is loading ghost pictures from res\ghosts\*
        To the array 'pictures'
    """
    dict_ghosts_pictures = {}
    postfixes = [
        'down', 'left',
        'right', 'up'
    ]

    dirpath = os.path.join('res', 'ghosts')

    ghost_image_path = os.path.join(dirpath, 'ghost.png')
    ghost_image = pygame.image.load(ghost_image_path)
    ghost_image = pygame.transform.scale(
        ghost_image, constants.    SIMPLE_OBJECT_SIZE)

    for name in constants.GHOST_NAMES:
        pictures = {}

        for i in range(len(postfixes)):
            path = os.path.join(dirpath, '{name}_{postfix}.png'.format(
                name=name, postfix=postfixes[i]))
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, constants.SIMPLE_OBJECT_SIZE)
            pictures[postfixes[i]] = image

        pictures['ghost'] = ghost_image
        dict_ghosts_pictures[name] = pictures

    return dict_ghosts_pictures


def __loading_pacman_pictures():
    """ 
        This function is loading pacman pictures from res\pacman\*
        To the array 'pictures'
    """

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
        image = pygame.transform.scale(image, constants.SIMPLE_OBJECT_SIZE)
        pictures[postfixes[i]] = image

    return pictures


def __loading_maps_objects(count_maps):
    """ 
        This function is loading maps objects from res\maps\*
        To the dict 'maps_objects'
    """

    maps_objects = []
    dirpath = os.path.join('res', 'level_walls')

    for i in range(1, count_maps):
        map_objects = {}

        walls = []
        coins = []
        cherries = []
        spawn_ghosts = []

        path = os.path.join(dirpath, 'map_{number}.txt'.format(number=i))

        with open(path, mode='r') as file:
            for yidx, line in enumerate(file):
                for xidx, symbol in enumerate(line):
                    if symbol == '1':
                        walls.append(constants.VEC_2(xidx, yidx))
                    elif symbol == 'C':
                        coins.append(constants.VEC_2(xidx, yidx))
                    elif symbol == 'H':
                        cherries.append(constants.VEC_2(xidx, yidx))
                    elif symbol in ['2', '3', '4', '5']:
                        spawn_ghosts.append(constants.VEC_2(xidx, yidx))

        map_objects['walls'] = walls
        map_objects['coins'] = coins
        map_objects['cherries'] = cherries
        map_objects['spawn_ghosts'] = spawn_ghosts

        maps_objects.append(map_objects)

    return maps_objects


def loading_map_objects(number):
    map_objects = {}
    dirpath = os.path.join('res', 'level_walls')
    path = os.path.join(dirpath, 'map_{number}.txt'.format(number=number))

    walls = []
    coins = []
    cherries = []
    spawn_ghosts = []

    with open(path, mode='r') as file:
        for yidx, line in enumerate(file):
            for xidx, symbol in enumerate(line):
                if symbol == '1':
                    walls.append(constants.VEC_2(xidx, yidx))
                elif symbol == 'C':
                    coins.append(constants.VEC_2(xidx, yidx))
                elif symbol == 'H':
                    cherries.append(constants.VEC_2(xidx, yidx))
                elif symbol in ['2', '3', '4', '5']:
                    spawn_ghosts.append(constants.VEC_2(xidx, yidx))

    map_objects['walls'] = walls
    map_objects['coins'] = coins
    map_objects['cherries'] = cherries
    map_objects['spawn_ghosts'] = spawn_ghosts

    return map_objects


def __loading_maps():
    maps = []

    for map_path in constants.MAPS_PATHS:
        got_picture = pygame.image.load(map_path)
        got_picture = pygame.transform.scale(got_picture,
                                             constants.MAP_SIZE)
        maps.append(got_picture)

    return maps


def __loading_cherry_picture():
    path_picture = constants.CHERRY_PICTURE_PATH
    got_picture = pygame.image.load(path_picture)
    got_picture = pygame.transform.scale(got_picture,
                                         constants.SIMPLE_OBJECT_SIZE)
    return got_picture


GHOSTS_PICTURES_LOADED = __loading_ghosts_pictures()
PACMAN_PICTURES_LOADED = __loading_pacman_pictures()
MAPS_PICTURES_LOADED = __loading_maps()
CHERRY_PICTURE_LOADED = __loading_cherry_picture()

# TODO: Create lazy load
# MAPS_OBJECTS = __loading_maps_objects(constants.COUNT_MAPS)
