import pygame
import sys

import constants
import label
import pacman
import enemy
import resources

from collections import defaultdict

WIDTH = constants.CELL_WIDTH
HEIGHT = constants.CELL_HEIGHT
TOP_BUFFER = constants.TOP_BUTTON_BUFFER

MAP_WIDTH = constants.MAP_WIDTH
MAP_HEIGHT = constants.MAP_HEIGHT

SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT

VEC_2 = constants.VEC_2


class Game(object):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        # Current level
        self.number_level = 0
        self.map_picture = resources.MAPS_PICTURES_LOADED[self.number_level]

        self.map_objects = resources.loading_map_objects(self.number_level + 1)
        self.cherry_picture = resources.CHERRY_PICTURE_LOADED

        # FPS configuration
        self.clock = pygame.time.Clock()

        # boolean constants
        self.game_over = False
        self.game_pause = False

        # set default values
        self.movement_objects = []
        self.scores = 0

        self.killed_ghosts = []

        self._init_movement_objects()

    def run(self):
        if self.game_pause:
            self.game_pause = False

        while not self.game_over and not self.game_pause:
            if len(self.killed_ghosts) > 0:
                self._update_info_killed_ghosts()

            self.check_win()

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()

            self.clock.tick(constants.FPS)

    def check_win(self):
        if self.scores == 288 and not self.launch_sound:
            self.launch_sound = True
            pygame.mixer.music.load(constants.WIN_SOUND_PATH)
            pygame.mixer.music.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.move(VEC_2(
                        0, -1))
                elif event.key == pygame.K_DOWN:
                    self.pacman.move(VEC_2(
                        0, constants.SPEED_PACMAN))
                elif event.key == pygame.K_RIGHT:
                    self.pacman.move(VEC_2(
                        constants.SPEED_PACMAN, 0))
                elif event.key == pygame.K_LEFT:
                    self.pacman.move(
                        VEC_2(-1, 0))
                elif event.key == pygame.K_ESCAPE:
                    self.game_pause = True

    def update(self):
        self._update_movement_objects()

    def draw(self):
        self._draw_map()
        self._draw_coins()
        self._draw_cherries()
        self._draw_movement_objects()
        self._draw_text()
        self._draw_lifes_pacman()

    def quit_game(self):
        self.game_over = True

    def _init_movement_objects(self):
        self.pacman = pacman.Pacman(self)
        self.movement_objects.append(self.pacman)

        for index, ghost_name in enumerate(constants.GHOST_NAMES):
            self.movement_objects.append(enemy.Enemy(
                ghost_name, self.map_objects['spawn_ghosts'][index], self))

    def add_score(self, score):
        self.scores += score

    def add_killed_ghost(self, ghost):
        self.killed_ghosts.append([ghost, 500])
        self.movement_objects.remove(ghost)

    def remove_cherry(self, position):
        try:
            self.map_objects['cherries'].remove(position)
        except Exception:
            pass

    def remove_coin(self, position):
        try:
            self.map_objects['coins'].remove(position)
        except Exception:
            pass

    def is_there_coin(self, position):
        return position in self.map_objects['coins']

    def is_there_cherry(self, position):
        return position in self.map_objects['cherries']

    def _draw_coins(self):
        for coin in self.map_objects['coins']:
            pygame.draw.circle(self.screen, constants.COIN_COLOUR,
                               (int(coin.x*WIDTH) + WIDTH//2 + TOP_BUFFER//2,
                                int(coin.y*HEIGHT) + HEIGHT // 2 + TOP_BUFFER
                                // 2), 2)

    def _draw_cherries(self):
        for cherry in self.map_objects['cherries']:
            self.screen.blit(self.cherry_picture,
                             (int(cherry.x*WIDTH) + TOP_BUFFER//2 + 2,
                              int(cherry.y*HEIGHT) + TOP_BUFFER//2 + 2))

    def _draw_movement_objects(self):
        for object in self.movement_objects:
            object.draw(self.screen)

    def _draw_text(self):
        text_score = 'CURRENT SCORE: {score}'.format(score=self.scores)
        text_position = 'POSITION: {position}'.format(
            position=self.pacman._get_pacman_position())

        # * Скорее лучше будет не повторять инциализацию, а добавить метод изменения текста
        score = label.Label(constants.TEXT_SCORE_POSITION, text_score,
                            constants.MAIN_FONT, constants.MAIN_SIZE_FONT,
                            constants.DEFAULT_TEXT_COLOUR)
        position = label.Label(constants.TEXT_PACMAN_POSITION, text_position,
                               constants.MAIN_FONT, constants.MAIN_SIZE_FONT, constants.DEFAULT_TEXT_COLOUR)

        score.draw(self.screen)
        position.draw(self.screen)

        if self.pacman.is_helper_activated():
            helper_time_text = 'TIME CHERRY: {time}'.format(
                time=self.pacman.helper_time)
            helper_time = label.Label(
                constants.TEXT_HELPER_TIME_POSITION, helper_time_text,
                constants.MAIN_FONT, constants.MAIN_SIZE_FONT,
                constants.DEFAULT_TEXT_COLOUR)

            helper_time.draw(self.screen)

    def _draw_map(self):
        self.screen.fill([0, 0, 0])
        self.screen.blit(self.map_picture, (TOP_BUFFER//2,
                                            TOP_BUFFER//2))

    def _draw_lifes_pacman(self):
        picture_pacman = resources.PACMAN_PICTURES_LOADED['right']
        space = 0

        for _ in range(self.pacman.count_lifes):
            position = constants.PICTURE_PACMAN_LIFE_POSITION + VEC_2(space, 0)
            self.screen.blit(picture_pacman, position)
            space += 30

    def _update_movement_objects(self):
        for object in self.movement_objects:
            object.update()

    def _update_info_killed_ghosts(self):
        removing_ghosts = []

        for index, ghost in enumerate(self.killed_ghosts):
            if ghost[1] > 0:
                ghost[1] -= 1
            else:
                self._respawn_killed_ghost(ghost[0])
                removing_ghosts.append(index)

        removing_ghosts.sort(reverse=True)

        for ghost_index in removing_ghosts:
            del self.killed_ghosts[ghost_index]

    def _respawn_killed_ghost(self, ghost):
        ghost.respawn()
        self.movement_objects.append(ghost)
