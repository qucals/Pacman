import pygame
import constants
import sys
import label
import pacman

from collections import defaultdict

WIDTH = constants.CELL_WIDTH
HEIGHT = constants.CELL_HEIGHT
TOP_BUFFER = constants.TOP_BUTTON_BUFFER

MAP_WIDTH = constants.MAP_WIDTH
MAP_HEIGHT = constants.MAP_HEIGHT

SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT


class Game(object):
    def __init__(self):
        super().__init__()

        # display constants
        self.size_display = constants.DISPLAY_SIZE
        self.size_map = (MAP_WIDTH, MAP_HEIGHT)

        # Current level
        self.number_level = 0
        self.map_objects = constants.MAPS_WALLS[self.number_level]

        # images constants
        self.background_image = pygame.image.load(
            constants.MAPS[self.number_level])
        self.background_image = pygame.transform.scale(
            self.background_image, self.size_map)

        # FPS configuration
        self.clock = pygame.time.Clock()

        # boolean constants
        self.game_over = False

        # init game
        pygame.init()
        pygame.display.set_caption(constants.GAME_NAME)

        self.screen = pygame.display.set_mode(self.size_display)

        # keybildings
        # TODO: Learn to use these keybildings
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)

        # set default values
        self.set_default_values()
        self.init_window_elemets()

        self.launch_sound = False

        # Start game
        self.run()

    def run(self):
        while not self.game_over:
            self.screen.fill([0, 0, 0])

            self.screen.blit(self.background_image, (TOP_BUFFER // 2,
                                                     TOP_BUFFER // 2))

            self.handle_events()
            self.update_objects()
            self.check_win()
            self.draw()

            pygame.display.update()

            self.clock.tick(constants.FPS)

    def check_win(self):
        if self.scores == 288 and not self.launch_sound:
            self.launch_sound = True
            pygame.mixer.music.load(constants.WIN_SOUND)
            pygame.mixer.music.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.move(constants.VEC_2(
                        0, -1))
                if event.key == pygame.K_DOWN:
                    self.pacman.move(constants.VEC_2(
                        0, constants.SPEED_OBJECT))
                if event.key == pygame.K_RIGHT:
                    self.pacman.move(constants.VEC_2(
                        constants.SPEED_OBJECT, 0))
                if event.key == pygame.K_LEFT:
                    self.pacman.move(
                        constants.VEC_2(-1, 0))

    def draw(self):
        self.draw_grid()
        self.draw_coins()
        self.draw_objects()
        self.draw_text()

    def draw_grid(self):
        GRAY = ((127, 127, 127))

        for x in range(SCREEN_WIDTH // WIDTH):
            pygame.draw.line(self.background_image, GRAY,
                             (x * WIDTH, 0), (x * WIDTH, SCREEN_HEIGHT))
        for x in range(SCREEN_HEIGHT // HEIGHT):
            pygame.draw.line(self.background_image, GRAY,
                             (0, x * HEIGHT), (SCREEN_WIDTH, x * HEIGHT))

    def draw_coins(self):
        for coin in self.map_objects['coins']:
            pygame.draw.circle(self.screen, constants.COIN_COLOUR,
                               (int(coin.x * WIDTH) + WIDTH // 2 + TOP_BUFFER // 2,
                                int(coin.y * HEIGHT) + HEIGHT // 2 + TOP_BUFFER // 2), 2)

    def update_objects(self):
        for object in self.objects:
            object.update()

    def draw_objects(self):
        for object in self.objects:
            object.draw(self.screen)

    def draw_text(self):
        POSITION_TEXT_SCORE = [30, 2]
        WHITE = ((255, 255, 255))
        text_score = 'CURRENT SCORE: {score}'.format(score=self.scores)

        score = label.Label(POSITION_TEXT_SCORE, text_score,
                            constants.MAIN_FONT, constants.MAIN_SIZE_FONT,
                            WHITE)
        score.draw(self.screen)

    def set_default_values(self):
        self.objects = []
        self.scores = 0
        self.count_lifes = 3

    def init_window_elemets(self):
        self.pacman = pacman.Pacman(constants.PACMAN_START_POSITION, self)
        self.objects.append(self.pacman)

    def load_walls(self):
        pass

    def quit_game(self):
        self.game_over = True
        pygame.quit()
        sys.exit()
