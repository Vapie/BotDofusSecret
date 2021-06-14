from PIL import Image
import colorsys


def threshold_pixel(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255., g / 255., b / 255.)
    return 1 if l > .55 else 0
    # return 1 if r > 127 and g > 127 and b > 127 else 0


def binnaryze_image(img):
    pixels = img.load()
    width, height = img.size
    # Create a new blank monochrome image.
    output_img = Image.new('1', (width, height), 0)
    output_pixels = output_img.load()

    for i in range(width):
        for j in range(height):
            output_pixels[i, j] = threshold_pixel(*pixels[i, j])
    return output_img

def reduce_image_size():

    pass



def add_black_baxkground_image(width,height,image):
    img = Image.new("RGB", (width, height), (0, 0, 0))
    img.paste(image, (int(width/4),int(height/2)))
    return img