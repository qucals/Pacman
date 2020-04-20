import game_object
import constants
import label
import enemy
import resources

import pygame
import time
import threading

WIDTH = constants.CELL_WIDTH
HEIGHT = constants.CELL_HEIGHT
TOP_BUFFER = constants.TOP_BUTTON_BUFFER

VEC_2 = constants.VEC_2


class Pacman(game_object.GameObject):
    def __init__(self, game):
        super().__init__(constants.PACMAN_START_POSITION)

        self.game = game

        self.g_position = self.position

        # current position
        self.c_position = self._get_position_pacman(self.position)

        self.station_pictures = resources.PACMAN_PICTURES_LOADED

        # current station
        self.c_station = 'right'
        self.save_c_station = self.c_station

        # current picture
        self.c_picture = self.station_pictures[self.c_station]

        self.direction = VEC_2(1, 0)
        self.can_move = True

        self.helper_time = 0
        self.count_lifes = 3

        # update pictures of eating
        self.thread_update_picture_eating = threading.Thread(
            target=self._update_picture_eating)
        self.thread_helper_boost = threading.Thread(
            target=self._helper_boost)

        self._start_thread_eating_animation()

    def update(self):
        if self.can_move:
            self.c_position += self.direction * constants.SPEED_PACMAN

        if self.on_coin():
            self.eat_coin()

        if self.on_cherry():
            self.eat_cherry()

        if self.on_ghost():
            self.action_ghost()

        self.can_move = self._can_move()
        self._update_grid()

    def draw(self, screen):
        # Computing movement and display the pacman
        pos = self._get_position_pacman(self.g_position)
        screen.blit(self.c_picture, (int(pos.x), int(pos.y)))

    def on_coin(self):
        if self.game.is_there_coin(self.g_position):
            return True
        return False

    def eat_coin(self):
        self.game.remove_coin(self.g_position)
        self.game.add_score(constants.SCORE_FOR_COIN)

    def on_cherry(self):
        if self.game.is_there_cherry(self.g_position):
            return True
        return False

    def on_ghost(self):
        for object in self.game.movement_objects:
            if type(object) == enemy.Enemy:
                if self.g_position == object.g_position:
                    return True
        return False

    def action_ghost(self):
        if self.is_helper_activated():
            self.eat_ghost()
        else:
            if self.count_lifes >= 2:
                self.count_lifes -= 1
                self.respawn()
            else:
                self.game.game_over = True

    def eat_ghost(self):
        for object in self.game.movement_objects:
            if type(object) == enemy.Enemy:
                if self.g_position == object.g_position:
                    self.game.add_killed_ghost(object)
                    self.game.add_score(constants.SCORE_FOR_GHOST)

    def eat_cherry(self):
        self.game.remove_cherry(self.g_position)
        self.game.add_score(constants.SCORE_FOR_CHERRY)
        self._start_thread_update_time_helper_boost()

    def move(self, direction):
        self.direction = direction
        self._change_station_picture()

    def is_helper_activated(self):
        return self.helper_time > 0

    def respawn(self):
        self.c_position = self._get_position_pacman(
            constants.PACMAN_START_POSITION)
        self._update_grid()

    def _update_grid(self):
        # Grid of movement of the pacman
        self.g_position[0] = (self.c_position[0]
                              - TOP_BUFFER + WIDTH//2) // WIDTH+1
        self.g_position[1] = (self.c_position[1]
                              - TOP_BUFFER + HEIGHT//2) // HEIGHT+1

    def _get_position_pacman(self, pos):
        return VEC_2((pos.x*WIDTH) + TOP_BUFFER//2 + 1,
                     (pos.y*HEIGHT) + TOP_BUFFER//2 + 1)

    def _get_position_grid(self, grid_position):
        return (grid_position[0]*WIDTH + TOP_BUFFER//2,
                grid_position[1]*HEIGHT + TOP_BUFFER//2,
                WIDTH, HEIGHT)

    def _get_pacman_position(self):
        return self.g_position

    def _change_station_picture(self):
        if self.direction.x > 0:
            self.c_station = 'right'
        elif self.direction.x < 0:
            self.c_station = 'left'
        elif self.direction.y > 0:
            self.c_station = 'down'
        elif self.direction.y < 0:
            self.c_station = 'up'
        self.c_picture = self.station_pictures[self.c_station]

    def _start_thread_eating_animation(self):
        self.thread_update_picture_eating.start()

    def _start_thread_update_time_helper_boost(self):
        if self.thread_helper_boost.is_alive():
            self.helper_time += 15
        else:
            self.thread_helper_boost = threading.Thread(
                target=self._helper_boost)
            self.thread_helper_boost.start()

    def _update_picture_eating(self):
        lock = threading.Lock()

        while not self.game.game_over:
            time.sleep(0.15)
            with lock:
                if self.c_station == 'default':
                    self.c_station = self.save_c_station
                else:
                    self.save_c_station = self.c_station
                    self.c_station = 'default'
                self.c_picture = self.station_pictures[self.c_station]

    def _helper_boost(self):
        lock = threading.Lock()

        with lock:
            self.helper_time = 15

        for ghost in self.game.movement_objects:
            with lock:
                if type(ghost) == enemy.Enemy:
                    ghost.can_killed = True

        while self.is_helper_activated():
            if self.game.game_over:
                return

            with lock:
                self.helper_time -= 1
                print(self.helper_time)
            time.sleep(1)

        for ghost in self.game.movement_objects:
            with lock:
                if type(ghost) == enemy.Enemy:
                    ghost.can_killed = False

    def _can_move(self, position=None, direction=None):
        pos = position if position is not None else self.g_position
        direct = direction if direction is not None else self.direction

        if VEC_2(pos + direct) in self.game.map_objects['walls']:
            return False
        return True
