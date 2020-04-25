import pygame
import constants


class Music:
    def __init__(self):
        pass

    def menu_sound(self):
        pass

    def secret_sound(self):
        pass

    def enter_sound(self):
        pass

    def killed_pacman(self):
        pass

    def play_sound(self):
        pass

    def stop_sound(self):
        pass

# class Music:
#     def __init__(self):
#         self.sounds = {
#             'secret': constants.SECRET_SOUND_PATH,
#             'enter': constants.ENTER_SOUND_PATH,
#             'menu': constants.MENU_SOUND_PATH,
#             'playing': constants.PLAYING_SOUND_PATH,
#             'first_death': constants.FIRST_DEATH_SOUND_PATH,
#             'second_death': constants.SECOND_DEATH_SOUND_PATH,
#             'third_death': constants.THIRD_DEATH_SOUND_PATH
#         }

#         self.is_playing = False
#         self.is_sound_background = False

#         pygame.mixer.music.set_volume(0.05)
#         pygame.mixer.music.set_endevent(constants.SONG_END)

#     def menu_sound(self):
#         if not self.is_sound_background:
#             pygame.mixer.music.load(self.sounds['menu'])
#             self.play_sound()
#             self.is_sound_background = True

#     def secret_sound(self):
#         pygame.mixer.music.load(self.sounds['secret'])
#         self.play_sound()

#     def playing_sound(self):
#         if not self.is_sound_background:
#             pygame.mixer.music.load(self.sounds['playing'])
#             self.play_sound()
#             self.is_sound_background = True

#     def enter_sound(self):
#         pygame.mixer.music.load(self.sounds['enter'])
#         self.play_sound()

#     def killed_pacman(self, current_count_life):
#         if current_count_life == 2:
#             pygame.mixer.music.load(self.sounds['first_death'])
#         elif current_count_life == 1:
#             pygame.mixer.music.load(self.sounds['second_death'])
#         elif current_count_life == 0:
#             pygame.mixer.music.load(self.sounds['third_death'])
#         self.play_sound()

#     def play_sound(self, repeating=0):
#         if self.is_playing:
#             self.stop_sound()
#         pygame.mixer.music.play(repeating)
#         self.is_playing = True

#     def stop_sound(self):
#         if self.is_playing:
#             if self.is_sound_background:
#                 self.is_sound_background = False

#             pygame.mixer.music.stop()
#             self.is_playing = False
