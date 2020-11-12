from random import randint

import pygame.mixer

pygame.mixer.init(buffer=8)

sound_bounce1 = pygame.mixer.Sound(f"sounds\\bounce\\bounce1.wav")
sound_bounce2 = pygame.mixer.Sound(f"sounds\\bounce\\bounce2.wav")
sound_bounce3 = pygame.mixer.Sound(f"sounds\\bounce\\bounce3.wav")
sound_bounce4 = pygame.mixer.Sound(f"sounds\\bounce\\bounce4.wav")
sound_bounce5 = pygame.mixer.Sound(f"sounds\\bounce\\bounce5.wav")
sound_death = pygame.mixer.Sound(f"sounds\\death.wav")
sound_button_press = pygame.mixer.Sound(f"sounds\\button1.wav")

sounds_list = [sound_death, sound_bounce1, sound_bounce2, sound_bounce3, sound_bounce4, sound_bounce5,
               sound_button_press]


def set_volume(volume):
    for sound in sounds_list:
        sound.set_volume(volume)


def play_bounce_sound():
    eval(f"sound_bounce{randint(1, 5)}.play()")


def play_death_sound():
    sound_death.play()


def play_button_press_sound():
    sound_button_press.play()


set_volume(1)