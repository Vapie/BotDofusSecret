from PIL import Image


def get_fighting_arena_as_array(image:Image):
    array = []
    for line in range(28):
        array.append([])
    return array