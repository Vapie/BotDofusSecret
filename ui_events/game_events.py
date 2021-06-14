import os
import random
import time

import pyautogui as pyautogui
from PIL import ImageFilter

from classes.coord import Coord
from classes.hints import Direction, HintList
from develeoppement_tools.debug import print_image
from image_processing.filter import binnaryze_image, add_black_baxkground_image
from image_processing.image_to_text import image_to_text_digit, image_to_text_fr
from ui_events.window_events import screenshot_screen

zaaps_coordinates = [Coord(-27,-36),
                     Coord(-1,13),
                     Coord(-2,0),
                     Coord(5,-18),
                     Coord(1,-32),
                     Coord(-32,-56),
                     Coord(-26,35),
                     Coord(-16,1),
                     Coord(-5,-23),
                     Coord(-20,-20)]


def get_coordinates() -> Coord:
    coordinates_screenshot = screenshot_screen(20, 72, 120, 28, False)
    coord_array = image_to_text_digit(coordinates_screenshot).split(",")

    return Coord(int(coord_array[0]),int(coord_array[1]))

def goto_coordinates(window_width: int,window_height: int,goal_coord:Coord) -> None:
    current_coordinate = get_coordinates()
    while(current_coordinate.x != goal_coord.x or current_coordinate.y != goal_coord.y):
        if goal_coord.x > current_coordinate.x:
            click_to_move(window_width,window_height,Direction.RIGHT)
        elif goal_coord.y > current_coordinate.y:
            click_to_move(window_width, window_height, Direction.DOWN)
        elif goal_coord.x < current_coordinate.x:
            click_to_move(window_width,window_height,Direction.LEFT)
        elif goal_coord.y < current_coordinate.y:
            click_to_move(window_width,window_height,Direction.UP)
        time.sleep(random.randint(6,8))
        current_coordinate = get_coordinates()

def click_to_move(window_width: int,window_height: int,direction: Direction) -> None:
        click_humanizer_offset = random.randint(-5,5)
        width_rand_offset = random.randint(250,window_width-250) +click_humanizer_offset
        height_rand_offset = random.randint(400,window_height-250) +click_humanizer_offset
        if direction == Direction.UP:
            pyautogui.click(width_rand_offset, 40+click_humanizer_offset)
        elif direction == Direction.DOWN :
            pyautogui.click(width_rand_offset, window_height - 120 + click_humanizer_offset)
        elif direction == Direction.RIGHT:
            pyautogui.click(window_width - 200 + click_humanizer_offset, height_rand_offset)
        elif direction == Direction.LEFT:
            pyautogui.click(200 + click_humanizer_offset, height_rand_offset)

def get_hint_direction(index_hint: int) -> Direction:
    offset =  index_hint * 26
    if  is_subitem_in_rectangle(1200,148+offset,40,40,'./screenshots/direction/Up.png'):
        return Direction.UP
    if  is_subitem_in_rectangle(1200,148+offset,40,40,'./screenshots/direction/Down.png'):
        return Direction.DOWN
    if  is_subitem_in_rectangle(1200,148+offset,40,40,'./screenshots/direction/Left.png'):
        return Direction.LEFT
    if  is_subitem_in_rectangle(1200,148+offset,40,40,'./screenshots/direction/Right.png') or is_subitem_in_rectangle(1200,148+offset,40,40,'./screenshots/direction/Right2.png'):
        return Direction.RIGHT
    #TODO error

def is_subitem_in_rectangle(x:int,y:int,width:int,height:int,path,confidence = 0.9):
    for pos in pyautogui.locateAllOnScreen(path, confidence=confidence):
        if (pos.left > x and (pos.height + pos.top) < (y+height) and pos.top > y and (pos.width + pos.left) < (x + width) ):
            return True
    return False

def click_zaap_havre_sac(coord: Coord):
    pyautogui.write('h')
    time.sleep(1)
    pyautogui.click(400, 400)
    time.sleep(1)
    pyautogui.click(500, 300)
    for i in range(zaaps_coordinates.index(coord)):
        time.sleep(0.5)
        pyautogui.press("down")
    pyautogui.press("enter")

def click_hint_flag(index_hint: int):
    offset = index_hint * 26
    pyautogui.click(1460, 168+offset)
    pyautogui.click(1, 1)

def goto_hunt_start():
    start_coord = read_coord_start()
    best_coord = get_coordinates()
    best_distance = start_coord.distance(best_coord)
    for zaap_coordinate in zaaps_coordinates:
        print(start_coord.distance(zaap_coordinate))
        if start_coord.distance(zaap_coordinate)<best_distance:
            best_distance = start_coord.distance(zaap_coordinate)
            best_coord = zaap_coordinate
    if best_coord != get_coordinates():
        print("zaap")
        click_zaap_havre_sac(best_coord)
        time.sleep(2)
    print(best_distance)
    goto_coordinates(1500, 950, start_coord)

def phorreur_hunt(hint_direction: Direction):
    for screen in range(10):
        click_to_move(1500,950,hint_direction)
        time.sleep(3)
        path ='./screenshots/phorreurs/'
        for sample_image in os.listdir(path):
            if is_subitem_in_rectangle(0, 0, 2000, 2000, path + sample_image,0.7):
                print(sample_image)
                return True

    return False
    #TODO handle error and forward-backward

def get_new_hunt():
    click_zaap_havre_sac(Coord(-27,-36))
    time.sleep(1)
    click_to_move(1500,950,Direction.RIGHT)
    time.sleep(6)
    click_to_move(1500,950,Direction.RIGHT)
    time.sleep(6)
    pyautogui.click(500,500)
    time.sleep(6)
    pyautogui.click(700, 500)
    time.sleep(6)
    pyautogui.click(1150, 450)
    time.sleep(6)
    pyautogui.click(800, 450)
    time.sleep(6)
    pyautogui.click(220, 750)
    time.sleep(6)
    pyautogui.click(220, 750)
    time.sleep(6)

def process_hunt():
    #get a hunt
    if not is_hunt_on_screen():
        print("new hunt")
        get_new_hunt()
    count = 0
    goto_hunt_start()
    while(not is_fight_button_on_screen()):
        while(is_unchecked_flag_on_screen()):
            hint_direction = get_hint_direction(count)
            hint = read_indice(count)
            start_etape_coord = get_coordinates()
            if "Phorreur" in  hint:
                phorreur_hunt(hint_direction)
            else:
                goto_coordinates(1500,950,HintList.from_url_parameters(start_etape_coord,hint_direction,0).get_nearest_hint(hint).coord)
            click_hint_flag(count)
            count = 1 + count
            time.sleep(2)
        click_validate()
        count=0
    print("fight")

def is_fight_button_on_screen() -> bool:
    return is_subitem_in_rectangle(0, 0, 2000, 2000, './screenshots/fight.png')

def is_hunt_on_screen() -> bool:
    return is_subitem_in_rectangle(0, 0, 2000, 2000, './screenshots/hunt.png')

def is_unchecked_flag_on_screen() -> bool:
    return is_subitem_in_rectangle(0, 0, 2000, 2000, './screenshots/flag.png')

def read_indice(index_hint: int) -> str:
    offset = index_hint * 26
    coordinates_screenshot = screenshot_screen(1230, 153+offset, 225, 26, False)
    binarized_coordinates_screenshot = binnaryze_image(coordinates_screenshot)
    return image_to_text_fr(binarized_coordinates_screenshot)

def read_coord_start() -> Coord:
    coordinates_screenshot = screenshot_screen(1230, 128, 140, 28, False)
    coord_array = image_to_text_digit(coordinates_screenshot).split(",")
    return Coord(int(coord_array[0]),int(coord_array[1]))

def click_validate():
    box = pyautogui.locateOnScreen('./screenshots/validate.png', confidence=0.9)
    pyautogui.click(box.left + 5, box.top + 5)
    pyautogui.click(1, 1)