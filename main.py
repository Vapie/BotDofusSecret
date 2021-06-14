import os

import pyautogui as pyautogui
from image_processing.image_to_text import *
from classes.coord import Coord
from classes.bot import Bot
from develeoppement_tools.debug import print_image
from ui_elements.notif_elements import Notifier
from classes.hints import Direction
from ui_events.game_events import get_coordinates, click_to_move, goto_coordinates, read_coord_start, read_indice, \
    is_subitem_in_rectangle, get_hint_direction, click_zaap_havre_sac, click_hint_flag, process_hunt, phorreur_hunt
from ui_events.window_events import resize_window, move_window, screenshot_screen


def setup():
    current_dofus_version = "2.59.10.11"
    resize_window("Dofus " + current_dofus_version, 1500, 950)
    move_window("Dofus " + current_dofus_version, 0, 0)
    pyautogui.click(50, 50)

if __name__ == "__main__":

    setup()
    print(read_indice(4))
    process_hunt()

    #click_zaap_havre_sac()
    #print_image(screenshot_screen(1425,320,30,22,True,"valkidate.png"))
    #print(range(1,1))
    #click_zaap_havre_sac(Coord(-27,-36))
    #mybot = Bot()
    #phorreur_hunt(Direction.RIGHT)










