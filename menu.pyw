import webbrowser
from collections import namedtuple
from random import randint

import pygame

import game
import sound

pygame.init()
pygame.mixer.init(buffer=16)

# размер окна
size = [1280, 720]
window = pygame.display.set_mode(size)
# задайте имя
pygame.display.set_caption("Pong-Ping menu")

screen = pygame.Surface(size)

font = pygame.font.Font("AtariClassic-Regular.ttf", 36)

player_count = 1


def check_touch(cords, block_cords, block_size):
    """checks whether the coordinate is within other coordinates"""
    if cords[0] in range(block_cords[0], (block_cords[0] + block_size[0] + 1)) \
            and cords[1] in range(block_cords[1], (block_cords[1] + block_size[1] + 1)):
        return True
    return False


def get_player_count():
    return player_count


Button = namedtuple("Button", ["surface", "size", "cords", "text", "action"])

button_play = Button(surface=pygame.Surface([400, 100]), size=[400, 100], cords=[440, 260],
                     text=["Play", [440 + 130, 260 + 30]],
                     action=f"game.start_game(get_player_count())")
button_exit = Button(surface=pygame.Surface([400, 100]), size=[400, 100], cords=[440, 380],
                     text=["Exit", [440 + 130, 380 + 30]],
                     action="running_menu = False")
button_volume = Button(surface=pygame.Surface([250, 100]), size=[250, 100], cords=[20, 600],
                       text=["+Sound+", [19, 630]],
                       action="""if button.text[0]=='+Sound+':
                                    sound.set_volume(0)
                                    button.text[0]='-Sound-'
                                \nelse:
                                    sound.set_volume(1)
                                    button.text[0]='+Sound+'""")
button_turn_player_count = Button(surface=pygame.Surface([100, 100]), size=[100, 100], cords=[1160, 600],
                                  text=["1P", [1175, 630]],
                                  action="""if button.text[0]=='1P':
                                        player_count = 2
                                        button.text[0] = '2P'
                                    \nelif button.text[0]=='2P':
                                        player_count = 0
                                        button.text[0] = 'AI'
                                    \nelse:
                                        player_count = 1
                                        button.text[0] = '1P'""")

buttons_list = (button_play, button_exit, button_volume, button_turn_player_count)

running_menu = True
while running_menu:

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    screen.fill([144, 238, 144])

    # ссылка на создателя
    if check_touch(pygame.mouse.get_pos(), [0, 0], [230, 50]):
        screen.blit(pygame.font.Font("AtariClassic-Regular.ttf", 16).render("Creator:", 1, (0, 0, 0)), (0, 0))
        screen.blit(pygame.font.Font("AtariClassic-Regular.ttf", 24).render("SergeLeon", 1, (
            randint(0, 255), randint(0, 255), randint(0, 255))), (0, 20))
        if pygame.mouse.get_pressed()[0]:
            webbrowser.open("https://github.com/SergeLeon", new=2)

    screen.blit(pygame.font.Font("AtariClassic-Regular.ttf", 64).render("Pong-Ping", 1, (0, 0, 0)), (353, 100))

    for button in buttons_list:
        if check_touch(pygame.mouse.get_pos(), button.cords, button.size):
            button.surface.fill([0, 0, 0])
            screen.blit(button.surface, button.cords)
            screen.blit(font.render(button.text[0], 1, [100, 100, 100]), button.text[1])
            if pygame.mouse.get_pressed()[0]:
                sound.play_button_press_sound()
                exec(button.action)
        else:
            button.surface.fill([100, 100, 100])
            screen.blit(button.surface, button.cords)
            screen.blit(font.render(button.text[0], 1, (0, 0, 0)), button.text[1])

    window.blit(screen, [0, 0])
    pygame.display.flip()
    pygame.time.delay(100)
