import game_object
import constants
import label

import pygame
import time
import threading

from pygame.locals import USEREVENT

WIDTH = constants.CELL_WIDTH
HEIGHT = constants.CELL_HEIGHT
TOP_BUFFER = constants.TOP_BUTTON_BUFFER


class Pacman(game_object.GameObject):
    def __init__(self, position, game):
        self.game = game

        self.position = position
        self.g_position = self.position

        # current position
        self.c_position = constants.VEC_2((self.position.x *
                                           WIDTH)
                                          + TOP_BUFFER // 2,
                                          (self.position.y *
                                           HEIGHT)
                                          + TOP_BUFFER // 2)

        self.station_pictures = constants.PACMAN_PICTURES

        # current station
        self.c_station = 'right'
        self.save_c_station = self.c_station

        # current picture
        self.c_picture = self.station_pictures[self.c_station]
        self.direction = constants.VEC_2(constants.SPEED_OBJECT, 0)
        self.stored_direction = None

        self.able_to_move = True

        # update pictures of eating
        self.thread_update_picture_eating = threading.Thread(
            target=self._update_picture_eating)
        self._init_threading()

    def update(self):
        if self.able_to_move:
            self.c_position += self.direction * constants.SPEED_OBJECT

        if self._can_move():
            if not self.stored_direction is None:
                self.direction = self.stored_direction

        if self.on_coin():
            self.eat_coin()

        self.able_to_move = self._able_to_move()
        self.update_grid()

    def update_grid(self):
        # Grid of movement of the pacman
        self.g_position[0] = (self.c_position[0] -
                              TOP_BUFFER + WIDTH // 2) // WIDTH + 1
        self.g_position[1] = (self.c_position[1] -
                              TOP_BUFFER + HEIGHT // 2) // HEIGHT + 1

    def draw(self, screen):
        RED = ((255, 0, 0))

        # Computing movement and display the pacman
        pos = self.compute_position_pacman(self.g_position)
        screen.blit(self.c_picture, (int(pos.x), int(pos.y)))

        # Rendering rect
        pygame.draw.rect(
            screen, RED, self.compute_grid_position(self.g_position), 1)

    def compute_position_pacman(self, pos):
        return constants.VEC_2((pos.x * WIDTH) + TOP_BUFFER // 2 + 1,
                               (pos.y * HEIGHT) + TOP_BUFFER // 2 + 1)

    def compute_grid_position(self, grid_position):
        return (grid_position[0] * WIDTH + TOP_BUFFER // 2,
                grid_position[1] * HEIGHT + TOP_BUFFER // 2,
                WIDTH, HEIGHT)

    def on_coin(self):
        my_position = self.g_position
        if my_position in self.game.map_objects['coins']:
            return True
        return False

    def eat_coin(self):
        my_position = self.g_position
        index = self.game.map_objects['coins'].index(my_position)
        del self.game.map_objects['coins'][index]
        self.game.scores += 1

    def move(self, direction):
        self.direction = direction
        self._change_station_picture()

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

    def _init_threading(self):
        self.thread_update_picture_eating.start()

    def _update_picture_eating(self):
        lock = threading.Lock()

        while True:
            time.sleep(0.15)
            with lock:
                if self.c_station == 'default':
                    self.c_station = self.save_c_station
                else:
                    self.save_c_station = self.c_station
                    self.c_station = 'default'
                self.c_picture = self.station_pictures[self.c_station]

                if self.game.game_over:
                    return

    def _able_to_move(self):
        for wall in self.game.map_objects['walls']:
            if constants.VEC_2(self.g_position + self.direction) == wall:
                return False
        return True

    def _can_move(self):
        if int(self.c_position.x + TOP_BUFFER // 2) % WIDTH == 0:
            if self.direction.x != 0:
                return True
        if int(self.c_position.y + TOP_BUFFER // 2) % HEIGHT == 0:
            if self.direction.y != 0:
                return True
