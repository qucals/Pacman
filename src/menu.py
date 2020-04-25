import pygame
import constants
import game
import label
import resources
import music

VEC_2 = constants.VEC_2


class Menu:
    """
    Class of the menu of the game
    """

    def __init__(self):
        # display constants
        self.size_display = constants.DISPLAY_SIZE

        # init game
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(constants.GAME_NAME)

        self.screen = pygame.display.set_mode(self.size_display)
        self.game = None
        self.quit_station = False

        self.current_object = 0
        self.objects = []

        self.SPACES_TEXT = 60
        self.TOP_BUFFER = 200
        self.CENTER_OF_SCREEN = constants.SCREEN_WIDTH//2

        self.background_image = resources.BACKGROUND_IMAGE_MENU_LOADED

        self.mixer = music.Music()

    def start(self):
        """
        Start working of the menu
        """

        while not self.quit_station:
            self.mixer.menu_sound()

            self.update()
            self.draw()
            self.handler_events()

            if not self.quit_station:
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
        """
        Draw all menu's objects
        """

        self.screen.blit(self.background_image, (0, 0))
        self._draw_text_objects()

    def update(self):
        """
        Update menu's objects
        """
        self._update_text_objects()

    def run(self):
        """
        Start playing the game
        """

        if self.game is None:
            self.restart()
        elif not self.game.game_pause:
            self.restart()

        self.game.run()

    def quit(self):
        """
        Quit from the game
        """

        self.quit_station = True
        if self.game is not None:
            self.game.quit_game()
        pygame.quit()

    def restart(self):
        """
        Restart of game's elements
        """

        if self.game is not None:
            del self.game
        self.game = game.Game(self.screen, self.mixer)

    def _define_action(self):
        """
        Define the program's action after pressed the button
        """

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
        """
        Check the game is running

        Returns:
            bool -- The game station
        """        
        
        if self.game is None:
            return False
        elif self.game.game_over:
            return False
        return True
