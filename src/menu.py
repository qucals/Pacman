import pygame
import constants
import game
import label

VEC_2 = constants.VEC_2


class Menu:
    def __init__(self):
        # display constants
        self.size_display = constants.DISPLAY_SIZE

        # init game
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(constants.GAME_NAME)

        self.screen = pygame.display.set_mode(self.size_display)
        self.game = None

        self.current_object = 0
        self.objects = []

        self.SPACES_TEXT = 60
        self.TOP_BUFFER = 200
        self.CENTER_OF_SCREEN = constants.SCREEN_WIDTH//2

    def start(self):
        while True:
            self.update()
            self.draw()
            self.handler_events()

            pygame.display.update()

    def handler_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.current_object != 0:
                        self.current_object -= 1
                elif event.key == pygame.K_DOWN:
                    if self.current_object != len(self.objects) - 1:
                        self.current_object += 1
                elif event.key == pygame.K_RETURN:
                    self._define_action()
            elif event.type == pygame.QUIT:
                self.quit()

    def draw(self):
        self.screen.fill([0, 0, 0])
        self._draw_text_objects()

    def update(self):
        self._update_text_objects()

    def run(self):
        self.restart()
        self.game.run()

    def quit(self):
        if self.game is not None:
            self.game.quit_game()
        pygame.quit()

    def _define_action(self):
        text = self.objects[self.current_object].text

        if text == 'START':
            self.run()
        elif text == 'EXIT':
            self.quit()

    def _update_text_objects(self):
        objects = []
        texts = ['START', 'EXIT']
        spaces_text = self.TOP_BUFFER

        for index, text in enumerate(texts):
            spaces_text += self.SPACES_TEXT

            if index == self.current_object:
                colour = constants.SELECTED_TEXT_COLOUR
            else:
                colour = constants.DEFAULT_TEXT_COLOUR

            text = label.Label(VEC_2(self.CENTER_OF_SCREEN, spaces_text), text,
                               constants.MAIN_FONT, constants.MAIN_SIZE_FONT,
                               colour)
            objects.append(text)

        self.objects = objects

    def _draw_text_objects(self):
        for object in self.objects:
            object.draw(self.screen)

        if self._is_running():
            self._draw_text_pause()

    def _draw_text_pause(self):
        text = label.Label(VEC_2(self.CENTER_OF_SCREEN, 200), 'PAUSE',
                           constants.MAIN_FONT, constants.MAIN_SIZE_FONT,
                           constants.PAUSE_TEXT_COLOUR)
        text.draw(self.screen)

    def _is_running(self):
        if self.game is None:
            return False
        elif self.game.game_over:
            return False
        return True

    def restart(self):
        if self.game is not None:
            del self.game
        self.game = game.Game(self.screen)
