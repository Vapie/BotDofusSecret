from ui_events.game_events import get_coordinates
from ui_events.window_events import resize_window, move_window


def setup():
    current_dofus_version = "2.59.9.10"
    resize_window("Dofus " + current_dofus_version, 1280, 950)
    move_window("Dofus " + current_dofus_version, 0, 0)

if __name__ == "__main__":
    setup()
    get_coordinates()










