from classes.coord import Coord
from develeoppement_tools.debug import printimage
from image_processing.filter import binnaryze_image, add_black_baxkground_image
from image_processing.image_to_text import imaget_to_text_digit
from ui_events.window_events import screenshot_screen


def get_coordinates() -> Coord:
    coordinates_screenshot = screenshot_screen(20, 72, 80, 28, True,"test.png")
    coordinates_screenshot = coordinates_screenshot.resize((1280,448))
    binarized_coordinates_screenshot = binnaryze_image(coordinates_screenshot)
    binarized_coordinates_screenshot_with_background = add_black_baxkground_image(3000,3000,binarized_coordinates_screenshot)
    printimage(binarized_coordinates_screenshot_with_background)
    print(imaget_to_text_digit(binarized_coordinates_screenshot_with_background))
    return Coord(0,0)
