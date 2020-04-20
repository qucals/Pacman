import pygame
import random
import numpy
import math

import constants
import game_object
import resources

WIDTH = constants.CELL_WIDTH
HEIGHT = constants.CELL_HEIGHT
TOP_BUFFER = constants.TOP_BUTTON_BUFFER

ROW = constants.ROW
COL = constants.COL

VEC_2 = constants.VEC_2


class Enemy(game_object.GameObject):
    def __init__(self, name, position, game):
        super().__init__(position)

        self.game = game
        self.name = name

        # Save start position for the case when enemy is killed and then come to life again
        self.start_position = position

        # grid position
        self.g_position = self.position

        # current position
        self.c_position = self._get_position_ghost(self.position)

        self.station_pictures = resources.GHOSTS_PICTURES_LOADED[name]

        self.can_killed = False

        # current station
        self.c_station = 'right'
        self.save_c_station = self.c_station

        # current picture
        self.c_picture = self.station_pictures[self.c_station]

        self.direction = VEC_2(1, 0)
        self.can_move = True

        self.speed = self._set_speed()

        # What the ghost is doing now
        self.action = self._set_action()

    def update(self):
        self.check_state_trace()

        if self.can_move:
            self.c_position += self.direction * self.speed

        self.move()

        self.can_move = self._can_move()
        self._update_grid()

    def draw(self, screen):
        # Computing movement and display the pacman
        pos = self._get_position_ghost(self.g_position)
        screen.blit(self.c_picture, (int(pos.x), int(pos.y)))

    def move(self):
        if self.action == 'pursuit':
            self.direction = self._get_next_direction()
        elif self.action == 'wandering':
            self.direction = self._get_random_direction()
        elif self.action == 'escaping':
            self.direction = self._get_escape_direction()

        self._change_station_picture()

    def check_state_trace(self):
        if self.can_killed and self.action == 'pursuit':
            self.action = 'wandering'
            return
        elif self.action == 'pursuit':
            return

        p_position = self.game.pacman._get_pacman_position()

        if p_position.x == self.g_position.x:
            if p_position.y > self.g_position.y:
                start = self.g_position.y
                stop = p_position.y
            else:
                start = p_position.y
                stop = self.position.y

            for i in range(int(start), int(stop)):
                if VEC_2(p_position.x, i) in self.game.map_objects['walls']:
                    return

            self.action = 'pursuit'

        elif p_position.y == self.g_position.y:
            if p_position.x > self.g_position.x:
                start = self.g_position.x
                stop = p_position.x
            else:
                start = p_position.x
                stop = self.position.x

            for i in range(int(start), int(stop)):
                if VEC_2(i, p_position.y) in self.game.map_objects['walls']:
                    return

            self.action = 'pursuit'

    def respawn(self):
        self.g_position = self.start_position
        self.c_position = self._get_position_ghost(self.start_position)
        self.can_killed = False

    def _update_grid(self):
        self.g_position[0] = (self.c_position[0]
                              - TOP_BUFFER + WIDTH//2) // WIDTH+1
        self.g_position[1] = (self.c_position[1]
                              - TOP_BUFFER + HEIGHT//2) // HEIGHT+1

    def _get_trace_direction(self):
        return self._compute_trace(True)

    def _get_escape_direction(self):
        return self._compute_trace(False)

    def _get_random_direction(self):
        if not random.randint(0, 100) < 5:
            if self._can_move(direction=self.direction):
                return self.direction

        prospective_direction = [VEC_2(1, 0), VEC_2(-1, 0),
                                 VEC_2(0, 1), VEC_2(0, -1)]
        numpy.random.shuffle(prospective_direction)

        for direction in prospective_direction:
            if self._can_move(direction=direction):
                return direction

    def _get_position_ghost(self, pos):
        return VEC_2((pos.x*WIDTH) + TOP_BUFFER//2 + 1,
                     (pos.y*HEIGHT) + TOP_BUFFER//2 + 1)

    def _get_position_grid(self, grid_position):
        return (grid_position[0]*WIDTH + TOP_BUFFER//2,
                grid_position[1]*HEIGHT + TOP_BUFFER//2,
                WIDTH, HEIGHT)

    def _set_action(self):
        if self.name in ['orange', 'blue']:
            return 'pursuit'
        else:
            return 'wandering'

    def _set_speed(self):
        if self.name in ['orange', 'blue']:
            return 1
        else:
            return 0.5

    def _change_station_picture(self):
        if self.can_killed:
            self.c_station = 'ghost'
        elif self.direction.x > 0:
            self.c_station = 'right'
        elif self.direction.x < 0:
            self.c_station = 'left'
        elif self.direction.y > 0:
            self.c_station = 'down'
        elif self.direction.y < 0:
            self.c_station = 'up'
        self.c_picture = self.station_pictures[self.c_station]

    def _get_next_direction(self):
        copy_current_position = VEC_2(self.g_position.x, self.g_position.y)
        pacman_position = self.game.pacman._get_pacman_position()
        copy_pacman_position = VEC_2(pacman_position.x, pacman_position.y)

        path = self.BFS(copy_current_position, copy_pacman_position)

        if type(path) == dict:
            return path['Direction']
        else:
            return self.direction

    def BFS(self, position, target):
        grid = [[0 for x in range(constants.COL)]
                for x in range(constants.ROW)]

        for cell in self.game.map_objects['walls']:
            if cell.x < constants.COL and cell.y < constants.ROW:
                grid[int(cell.y)][int(cell.x)] = 1

        queue = [position]
        path = []
        visited = []

        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)

            if current == target:
                break
            else:
                possible_directions = self._get_direction_to_move(current)

                for direction in possible_directions:
                    next_cell = current + direction

                    if next_cell.x >= 0 and next_cell.x < len(grid[0]):
                        if next_cell.y >= 0 and next_cell.y < len(grid):
                            if next_cell not in visited:
                                queue.append(next_cell)
                                path.append(
                                    {'Current': current, 'Next': next_cell, 'Direction': direction})

        shortest = [target]

        while position != target:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest = step

        return shortest

    def _get_direction_to_move(self, g_position=None):
        _pos = g_position if g_position is not None else self.g_position
        prospective_direction = [VEC_2(1, 0), VEC_2(-1, 0),
                                 VEC_2(0, 1), VEC_2(0, -1)]
        r_direction = []

        for direction in prospective_direction:
            if self._can_move(position=_pos, direction=direction):
                r_direction.append(direction)

        return r_direction

    def _get_distance(self, pos_1, pos_2):
        return math.sqrt((pos_2.x - pos_1.x)**2 + (pos_2.y - pos_1.y)**2)

    def _can_move(self, position=None, direction=None):
        pos = position if position is not None else self.g_position
        direct = direction if direction is not None else self.direction

        if VEC_2(pos + direct) in self.game.map_objects['walls']:
            return False
        return True
