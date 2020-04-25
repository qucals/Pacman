import os
import pygame

GAME_NAME = 'Niggaman from opensource code for python'
FPS = 60

# Pygame event about a sound has ended
SONG_END = pygame.USEREVENT + 1

VEC_2 = pygame.math.Vector2

# Constants of size of the window
SCREEN_WIDTH = 610
SCREEN_HEIGHT = 670
DISPLAY_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Constants of the map's size
TOP_BUTTON_BUFFER = 50
MAP_WIDTH = SCREEN_WIDTH - TOP_BUTTON_BUFFER
MAP_HEIGHT = SCREEN_HEIGHT - TOP_BUTTON_BUFFER
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)

# Constants of several the text's positions
TEXT_SCORE_POSITION = VEC_2(150, 16)
TEXT_PACMAN_POSITION = VEC_2(440, 16)
TEXT_HELPER_TIME_POSITION = VEC_2(SCREEN_WIDTH//2, 658)

PICTURE_PACMAN_LIFE_POSITION = VEC_2(50, 648)

# The size of a cell in the map
ROW = 30
COL = 28

CELL_WIDTH = MAP_WIDTH // COL
CELL_HEIGHT = MAP_HEIGHT // ROW

SIMPLE_OBJECT_SIZE = (16, 16)

SPEED_PACMAN = 1
SIMPLE_SPEED_GHOST = 1
FAST_SPEED_GHOST = 1.5

MAIN_FONT = 'arial black'
MAIN_SIZE_FONT = 16

PACMAN_START_POSITION_X = 14
PACMAN_START_POSITION_Y = 5
PACMAN_START_POSITION = VEC_2(PACMAN_START_POSITION_X, PACMAN_START_POSITION_Y)

GHOST_NAMES = [
    'red',
    'blue',
    'pink',
    'orange',
]

MAPS_PATHS = [
    os.path.join(os.path.join('res', 'maps'), 'map_1.png'),
    os.path.join(os.path.join('res', 'maps'), 'map_2.png')
]

CHERRY_PICTURE_PATH = os.path.join(
    os.path.join('res', 'helpers'), 'cherry.png')

IMAGE_MENU_PATH = os.path.join(os.path.join(
    'res', 'images'), 'background_menu.png')

SECRET_SOUND_PATH = os.path.join(os.path.join('res', 'audio'), 'secret.mp3')
ENTER_SOUND_PATH = os.path.join(os.path.join('res', 'audio'), 'enter.mp3')
MENU_SOUND_PATH = os.path.join(os.path.join('res', 'audio'), 'menu.mp3')
PLAYING_SOUND_PATH = os.path.join(os.path.join('res', 'audio'), 'playing.mp3')
FIRST_DEATH_SOUND_PATH = os.path.join(
    os.path.join('res', 'audio'), 'first_death.mp3')
SECOND_DEATH_SOUND_PATH = os.path.join(
    os.path.join('res', 'audio'), 'second_death.mp3')
THIRD_DEATH_SOUND_PATH = os.path.join(
    os.path.join('res', 'audio'), 'third_death.mp3')

COIN_COLOUR = ((255, 255, 255))

BACKGROUND_MAP_COLOUR = ((0, 0, 0))

DEFAULT_TEXT_COLOUR = ((255, 255, 255))
SELECTED_TEXT_COLOUR = ((255, 255, 0))
PAUSE_TEXT_COLOUR = ((255, 0, 0))

COUNT_MAPS = len(MAPS_PATHS)

SCORE_FOR_COIN = 10
SCORE_FOR_CHERRY = 100
SCORE_FOR_GHOST = 200

TRIGGER_WIN_SOUND = 2280
